from wpilib import XboxController
# from wpilib import Joystick
from wpimath import applyDeadband
from wpimath.filter import SlewRateLimiter
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_STRAFE_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_ROTATE_SPEED_RAD_PER_SEC
from drivetrain.drivetrainPhysical import MAX_ROTATE_ACCEL_RAD_PER_SEC_2
from drivetrain.drivetrainPhysical import MAX_TRANSLATE_ACCEL_MPS2
from utils.faults import Fault
from utils.signalLogging import log
from utils.allianceTransformUtils import onRed
from utils.singleton import Singleton

class DriverInterface(metaclass=Singleton):
    """Class to gather input from the driver of the robot"""

    def __init__(self):
        driveIdx = 0
        self.drive = XboxController(driveIdx)

        aimerIdx = 1
        self.aimer = XboxController(aimerIdx)
        # self.aimer = Joystick(0)

        self.velXCmd = 0
        self.velYCmd = 0
        self.velTCmd = 0
        self.initIntake = False
        self.gyroResetCmd = False
        self.connectedFault = Fault(f"Driver XBox Controller ({driveIdx}) Unplugged")
        self.velXSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velYSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velTSlewRateLimiter = SlewRateLimiter(
            rateLimit=MAX_ROTATE_ACCEL_RAD_PER_SEC_2
        )



    def update(self):
        """Main update - call this once every 20ms"""

        if self.drive.isConnected():
            # Only attempt to read from the joystick if it's plugged in

            # Convert from joystic sign/axis conventions to robot velocity conventions
            vXJoyRaw = -1.0 * self.drive.getLeftY()
            vYJoyRaw = -1.0 * self.drive.getLeftX()
            vTJoyRaw = -1.0 * self.drive.getRightX()

            # Apply deadband to make sure letting go of the joystick actually stops the bot
            vXJoy = applyDeadband(vXJoyRaw, 0.15)
            vYJoy = applyDeadband(vYJoyRaw, 0.15)
            vTJoy = applyDeadband(vTJoyRaw, 0.15)

            # Normally robot goes half speed - unlock full speed on
            # sprint command being active
            sprintMult = 1.0 if (self.drive.getRightBumper()) else 0.5

            # Convert joystick fractions into physical units of velocity
            velXCmdRaw = vXJoy * MAX_FWD_REV_SPEED_MPS * sprintMult
            velYCmdRaw = vYJoy * MAX_STRAFE_SPEED_MPS * sprintMult
            velTCmdRaw = vTJoy * MAX_ROTATE_SPEED_RAD_PER_SEC

            # Slew-rate limit the velocity units to not change faster than
            # the robot can physically accomplish
            self.velXCmd = self.velXSlewRateLimiter.calculate(velXCmdRaw)
            self.velYCmd = self.velYSlewRateLimiter.calculate(velYCmdRaw)
            self.velTCmd = self.velTSlewRateLimiter.calculate(velTCmdRaw)

            # Adjust the commands if we're on the opposite side of the feild
            if onRed():
                self.velXCmd *= -1
                self.velYCmd *= -1

            
            self.gyroResetCmd = self.drive.getAButtonPressed()

            self.connectedFault.setNoFault()
        else:
            # If the joystick is unplugged, pick safe-state commands and raise a fault
            self.velXCmd = 0.0
            self.velYCmd = 0.0
            self.velTCmd = 0.0
            self.gyroResetCmd = False
            self.connectedFault.setFaulted()

        if self.aimer.isConnected():
            self.initIntake = self.aimer.getYButtonPressed()
        else:
            self.initIntake = False

        log("DI FwdRev Cmd", self.velXCmd, "mps")
        log("DI Strafe Cmd", self.velYCmd, "mps")
        log("DI Rotate Cmd", self.velTCmd, "radPerSec")
        log("DI connected", self.drive.isConnected(), "bool")

    def getVxCmd(self):
        """
        Returns:
            float: Driver's current vX (downfield/upfield, or fwd/rev) command in meters per second
        """
        return self.velXCmd

    def getVyCmd(self):
        """
        Returns:
            float: Driver's current vY (side-to-side or strafe) command in meters per second
        """
        return self.velYCmd

    def getVtCmd(self):
        """
        Returns:
            float: Driver's current vT (rotation) command in radians per second
        """
        return self.velTCmd

    def getIntakeActive(self):
        return self.initIntake

    def getGyroResetCmd(self):
        """_summary_

        Returns:
            boolean: True if the driver wants to reset the gyro, false otherwise
        """
        return self.gyroResetCmd
