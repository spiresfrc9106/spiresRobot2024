import random

from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.controller import PIDController
from wpimath.kinematics import SwerveModuleState
from wpimath.kinematics import SwerveModulePosition
from wpimath.geometry import Rotation2d
import wpilib

from wrappers.wrapperedSparkMax import WrapperedSparkMax
from dashboardWidgets.swerveState import getAzmthDesTopicName, getAzmthActTopicName
from dashboardWidgets.swerveState import getSpeedDesTopicName, getSpeedActTopicName
from utils.calibration import Calibration
from utils.signalLogging import log
from utils.units import rad2Deg
from utils.faults import Fault
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.robotIdentification import RobotIdentification
from drivetrain.drivetrainPhysical import dtMotorRotToLinear
from drivetrain.drivetrainPhysical import dtLinearToMotorRot
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import wrapperedSwerveDriveAzmthEncoder

class SwerveModuleControl:
    """
    Control logic for one swerve drive module
    """

    def __init__(
        self,
        moduleName,
        wheelMotorCanID,
        azmthMotorCanID,
        azmthEncoderPortIdx,
        azmthOffset,
        invertWheel,
        invertAzmthMotor,
        invertAzmthEncoder
    ):
        """Instantiate one swerve drive module

        Args:
            moduleName (str): Name Prefix for the module (IE, "FL", or "BR"). For logging purposes mostly
            wheelMotorCanID (int): CAN Id for the wheel motor for this module
            azmthMotorCanID (int): CAN Id for the azimuth motor for this module
            azmthEncoderPortIdx (int): RIO Port for the azimuth absolute encoder for this module
            azmthOffset (float): Mounting offset of the azimuth encoder in Radians.
            invertWheel (bool): Inverts the drive direction of the wheel - needed since left/right sides are mirrored
            invertWheel (bool): Inverts the steering direction of the wheel - needed if motor is mounted upside
        """
        self.wheelCurLimitACal = Calibration(f'SwerveModule {moduleName} Current Limit', 25, "Amps", 0)
        self.wheelMotor = WrapperedSparkMax(
            wheelMotorCanID, moduleName + "_wheel", brakeMode=False, curLimitA=int(self.wheelCurLimitACal.get()))
        self.azmthMotor = WrapperedSparkMax(
            azmthMotorCanID, moduleName + "_azmth", True
        )

        self.azmthEnc = wrapperedSwerveDriveAzmthEncoder(
            azmthEncoderPortIdx, moduleName + "_azmthEnc", azmthOffset, invertAzmthEncoder
        )

        self.wheelMotor.setInverted(invertWheel)
        self.azmthMotor.setInverted(invertAzmthMotor)

        self.wheelMotorFF = SimpleMotorFeedforwardMeters(0, 0, 0)
        self.wheelMotorVoltageFF = 0

        self.desiredState = SwerveModuleState()
        self.optimizedDesiredState = SwerveModuleState()
        self.actualState = SwerveModuleState()
        self.actualPosition = SwerveModulePosition()

        self.azmthCtrl = PIDController(0, 0, 0)
        self.azmthCtrl.enableContinuousInput(-180.0, 180.0)

        self._prevMotorDesSpeed = 0

        self.moduleName = moduleName

        self.serialFault = Fault(f"Serial Number Unknown")
        self.rId = RobotIdentification()
        self.stt = SegmentTimeTracker()
        #                                                                         1         2         3
        #                                                                12345678901234567890123456789012345
        self.markAzmthEncUpdateName       = self.stt.makePaddedMarkName("azmthEnc.update." + self.moduleName)
        self.markOptimizedDesiredName     = self.stt.makePaddedMarkName("optimizedDesiredState." + self.moduleName)
        self.markAzmthMotorSetVoltageName = self.stt.makePaddedMarkName("azmthMotor.setVoltage." + self.moduleName)
        self.markWheelMotorSetVelCmdName  = self.stt.makePaddedMarkName("wheelMotor.setVelCmd." + self.moduleName)
        self.markUpdateActualStateName    = self.stt.makePaddedMarkName("markUpdateActualStateName." + self.moduleName)
        self.markUpdateTelemetryName      = self.stt.makePaddedMarkName("updateTelemetry()." + self.moduleName)

    def _updateTelemetry(self):
        """
        Helper function to put all relevant data to logs and dashboards for this module
        """
        log(
            getAzmthDesTopicName(self.moduleName),
            self.optimizedDesiredState.angle.degrees(),
            "deg",
        )
        log(
            getAzmthActTopicName(self.moduleName),
            self.actualState.angle.degrees(),
            "deg",
        )
        log(
            getSpeedDesTopicName(self.moduleName),
            self.optimizedDesiredState.speed / MAX_FWD_REV_SPEED_MPS,
            "frac",
        )
        log(
            getSpeedActTopicName(self.moduleName),
            (self.actualState.speed) / MAX_FWD_REV_SPEED_MPS,
            "frac",
        )
        log(
            f"Dt_{self.moduleName}_FF_V",
            self.wheelMotorVoltageFF,
            "V"
        )

        if self.rId.getSerialFaulted():
            self.serialFault.setFaulted()
        else:
            self.serialFault.setNoFault()

    def getActualPosition(self):
        """
        Returns:
            SwerveModulePosition: The position of the module (azmth and wheel) as measured by sensors
        """
        return self.actualPosition

    def getActualState(self):
        """
        Returns:
            SwerveModuleState: The state of the module (azmth and wheel) as measured by sensors
        """
        return self.actualState

    def getDesiredState(self):
        """
        Returns:
            SwerveModuleState: The commanded, desired state of the module (azmth and wheel)
        """
        return self.desiredState

    def setClosedLoopGains(self, gains):
        """Set feed-forward and closed loop gains for the module

        Args:
            gains (SwerveModuleGainSet): The gains for this module
        """
        self.wheelMotor.setPID(
            gains.wheelP.get(), gains.wheelI.get(), gains.wheelD.get()
        )
        self.wheelMotorFF = SimpleMotorFeedforwardMeters(
            gains.wheelS.get(), gains.wheelV.get(), gains.wheelA.get()
        )
        self.azmthCtrl.setPID(
            gains.azmthP.get(), gains.azmthI.get(), gains.azmthD.get()
        )

    def setDesiredState(self, desState):
        """Main command input - Call this to tell the module to go to a certian wheel speed and azimuth angle

        Args:
            desState (SwerveModuleState): The commanded state of the module
        """
        self.desiredState = desState

    def update(self):
        """Main update function, call every 20ms"""
        if self.wheelCurLimitACal.isChanged():
            self.wheelMotor.setSmartCurrentLimit(int(self.wheelCurLimitACal.get()))

        # Read from the azimuth angle sensor (encoder)
        self.azmthEnc.update()

        azmthAngleRad = self.azmthEnc.getAngleRad()
        azmthAngleRotation2d = Rotation2d(azmthAngleRad)
        self.stt.perhapsMark(self.markAzmthEncUpdateName)

        # Optimize our incoming swerve command to minimize motion
        self.optimizedDesiredState = SwerveModuleState.optimize(self.desiredState, 
                                                                azmthAngleRotation2d)
        self.stt.perhapsMark(self.markOptimizedDesiredName)
        # Use a PID controller to calculate the voltage for the azimuth motor
        self.azmthCtrl.setSetpoint(self.optimizedDesiredState.angle.degrees()) # type: ignore
        azmthVoltage = self.azmthCtrl.calculate(rad2Deg(azmthAngleRad))
        self.azmthMotor.setVoltage(azmthVoltage)
        self.stt.perhapsMark(self.markAzmthMotorSetVoltageName)

        # Send voltage and speed commands to the wheel motor
        
        motorDesSpd = dtLinearToMotorRot(self.optimizedDesiredState.speed)
        motorDesAccel = (motorDesSpd - self._prevMotorDesSpeed)/ 0.02
        self.wheelMotorVoltageFF = self.wheelMotorFF.calculate(motorDesSpd, motorDesAccel)
        self.wheelMotor.setVelCmd(motorDesSpd, self.wheelMotorVoltageFF)
        self.stt.perhapsMark(self.markWheelMotorSetVelCmdName)
        
        self._prevMotorDesSpeed = motorDesSpd # save for next loop

        if wpilib.TimedRobot.isSimulation():
            # Simulation - assume module is almost perfect but with some noise
            self.actualState.angle = (
                self.optimizedDesiredState.angle
                + Rotation2d.fromDegrees(random.uniform(-1, 1))
            )
            self.actualState.speed = self.optimizedDesiredState.speed + random.uniform(
                -0.1, 0.1
            )
            self.actualPosition.distance += self.actualState.speed * 0.02
            self.actualPosition.angle = self.actualState.angle
        else:
            # Real Robot
            # Update this module's actual state with measurements from the sensors
            self.actualState.angle = azmthAngleRotation2d
            self.actualState.speed = dtMotorRotToLinear(
                self.wheelMotor.getMotorVelocityRadPerSec()
            )
            self.actualPosition.distance = dtMotorRotToLinear(
                self.wheelMotor.getMotorPositionRad()
            )
            self.actualPosition.angle = self.actualState.angle
            self.stt.perhapsMark(self.markUpdateActualStateName)

        self._updateTelemetry()
        self.stt.perhapsMark(self.markUpdateTelemetryName)
