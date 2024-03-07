from wpilib import XboxController, RobotBase
from wpimath import applyDeadband
from wpimath.filter import SlewRateLimiter
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_STRAFE_SPEED_MPS
from drivetrain.drivetrainPhysical import MAX_ROTATE_SPEED_RAD_PER_SEC
from drivetrain.drivetrainPhysical import MAX_ROTATE_ACCEL_RAD_PER_SEC_2
from drivetrain.drivetrainPhysical import MAX_TRANSLATE_ACCEL_MPS2
from humanInterface.simXboxController import SimXboxController
from utils.faults import Fault
from utils.signalLogging import log
from utils.allianceTransformUtils import onRed
from utils.units import rad2Deg
from . import DRIVER_CTRL_IDX

class DriverInterface:
    """Class to gather input from the driver of the robot"""

    def __init__(self):
        if not RobotBase.isSimulation():
            self.ctrl = XboxController(DRIVER_CTRL_IDX)
        else:
            self.ctrl = SimXboxController(DRIVER_CTRL_IDX)

        self.fieldRelative = True
        self.velXCmd = 0
        self.velYCmd = 0
        self.velTCmd = 0
        self.headingCmdDeg = None
        self.gyroResetCmd = False
        self.connectedFault = Fault(f"Driver XBox Controller ({DRIVER_CTRL_IDX}) Unplugged")

        self.velXSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velYSlewRateLimiter = SlewRateLimiter(rateLimit=MAX_TRANSLATE_ACCEL_MPS2)
        self.velTSlewRateLimiter = SlewRateLimiter(
            rateLimit=MAX_ROTATE_ACCEL_RAD_PER_SEC_2
        )

    def update(self):
        """Main update - call this once every 20ms"""

        if self.ctrl.isConnected():
            # Only attempt to read from the joystick if it's plugged in

            # Driver can select field relative or robot relative steering
            self.fieldRelative = not self.ctrl.getRightBumper()

            # Convert from joystic sign/axis conventions to robot velocity conventions
            vXJoyRaw = -1.0 * self.ctrl.getLeftY()
            vYJoyRaw = -1.0 * self.ctrl.getLeftX()
            vTJoyRaw =  -1.0 * self.ctrl.getRightX()

            dpadRaw = self.ctrl.getPOV() # up: 0, right: 90, down: 180, left: 270, unpressed: -1
            self.headingCmdDeg = 360 - dpadRaw if dpadRaw != -1 else None # up: 0, right: 270, down: 180, left: 90, unpressed: None

            # Apply deadband to make sure letting go of the joystick actually stops the bot
            vXJoy = applyDeadband(vXJoyRaw, 0.15)
            vYJoy = applyDeadband(vYJoyRaw, 0.15)
            vTJoy = applyDeadband(vTJoyRaw, 0.15)

            # Normally robot goes half speed - unlock full speed on
            # sprint command being active
            sprintMult = 1.0 if (self.ctrl.getLeftBumper()) else 0.5

            # Convert joystick fractions into physical units of velocity
            velXCmdRaw = vXJoy * MAX_FWD_REV_SPEED_MPS * sprintMult
            velYCmdRaw = vYJoy * MAX_STRAFE_SPEED_MPS * sprintMult
            velTCmdRaw = vTJoy * MAX_ROTATE_SPEED_RAD_PER_SEC * sprintMult

            # Slew-rate limit the velocity units to not change faster than
            # the robot can physically accomplish
            self.velXCmd = self.velXSlewRateLimiter.calculate(velXCmdRaw)
            self.velYCmd = self.velYSlewRateLimiter.calculate(velYCmdRaw)
            self.velTCmd = self.velTSlewRateLimiter.calculate(velTCmdRaw)

            # Adjust the commands if we're robot relative
            if onRed() or not self.fieldRelative:
                self.velXCmd *= -1
                self.velYCmd *= -1

            self.gyroResetCmd = self.ctrl.getAButtonPressed()

            self.connectedFault.setNoFault()
        else:
            # If the joystick is unplugged, pick safe-state commands and raise a fault
            self.fieldRelative = True
            self.velXCmd = 0.0
            self.velYCmd = 0.0
            self.velTCmd = 0.0
            self.headingCmdDeg = None
            self.gyroResetCmd = False
            self.connectedFault.setFaulted()

        log("DI fieldR Cmd", self.fieldRelative, "bool")
        log("DI FwdRev Cmd", self.velXCmd, "mps")
        log("DI Strafe Cmd", self.velYCmd, "mps")
        log("DI Rotate Cmd", rad2Deg(self.velTCmd), "degPerSec")
        log("DI Heading Cmd", self.headingCmdDeg, "deg")
        log("DI connected", self.ctrl.isConnected(), "bool")

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

    def getHeadingCmd(self):
        """
        Returns:
            int | None: Desired heading command in degrees or None to use vTCmd instead
        """
        return self.headingCmdDeg

    def getGyroResetCmd(self):
        """_summary_

        Returns:
            boolean: True if the driver wants to reset the gyro, false otherwise
        """
        return self.gyroResetCmd
