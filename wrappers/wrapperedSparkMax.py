from rev import CANSparkMax, SparkMaxPIDController, REVLibError, CANSparkLowLevel
from utils.signalLogging import log
from utils.units import rev2Rad, radPerSec2RPM, RPM2RadPerSec
from utils.faults import Fault


## Wrappered Spark Max
# Wrappers REV's libraries to add the following functionality for spark max controllers:
# Grouped PID controller, Encoder, and motor controller objects
# Physical unit conversions into SI units (radians)
# Retry logic for initial configuration
# Fault handling for not crashing code if the motor controller is disconnected
# Fault annunciation logic to trigger warnings if a motor couldn't be configured

class WrapperedSparkMax:
    def __init__(self, canID, name, brakeMode=False):
        self.ctrl = CANSparkMax(canID, CANSparkLowLevel.MotorType.kBrushless)
        self.pidCtrl = self.ctrl.getPIDController()
        self.encoder = self.ctrl.getEncoder()
        self.name = name
        self.connected = False
        self.disconFault = Fault(f"Spark Max {name} ID {canID} disconnected")

        # Perform motor configuration, tracking errors and retrying until we have success
        retryCounter = 0
        while not self.connected and retryCounter < 10:
            retryCounter += 1
            errList = []
            errList.append(self.ctrl.restoreFactoryDefaults())
            mode = (
                CANSparkMax.IdleMode.kBrake
                if brakeMode
                else CANSparkMax.IdleMode.kCoast
            )
            errList.append(self.ctrl.setIdleMode(mode))
            errList.append(self.ctrl.setSmartCurrentLimit(40))
            # Status 0 = Motor output and Faults
            errList.append(
                self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus0, 20)
            )
            # Status 1 = Motor velocity & electrical data
            errList.append(
                self.ctrl.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus1, 60)
            )
            # Status 2 = Motor Position
            errList.append(
                self.ctrl.setPeriodicFramePeriod(
                    CANSparkMax.PeriodicFrame.kStatus2, 65500
                )
            )
            # Status 3 = Analog Sensor Input
            errList.append(
                self.ctrl.setPeriodicFramePeriod(
                    CANSparkMax.PeriodicFrame.kStatus3, 65500
                )
            )
            if any(x != REVLibError.kOk for x in errList):
                print(
                    f"Failure configuring Spark Max {name} CAN ID {canID}, retrying..."
                )
            else:
                self.connected = True

        self.disconFault.set(not self.connected)

    def setInverted(self, isInverted):
        if self.connected:
            self.ctrl.setInverted(isInverted)

    def setPID(self, kP, kI, kD):
        if self.connected:
            self.pidCtrl.setP(kP)
            self.pidCtrl.setI(kI)
            self.pidCtrl.setD(kD)

    def setVelCmd(self, velCmd, arbFF=0.0):
        """_summary_

        Args:
            velCmd (float): motor desired shaft velocity in radians per second
            arbFF (int, optional): _description_. Defaults to 0.
        """
        velCmdRPM = radPerSec2RPM(velCmd)

        if self.connected:
            self.pidCtrl.setReference(
                velCmdRPM,
                CANSparkMax.ControlType.kVelocity,
                0,
                arbFF,
                SparkMaxPIDController.ArbFFUnits.kVoltage,
            )

        log(self.name + "_desVel", velCmdRPM, "RPM")
        log(self.name + "_arbFF", arbFF, "V")
        self._logCurrent()

    def setVoltage(self, outputVoltageVolts):
        log(self.name + "_cmdVoltage", outputVoltageVolts, "V")
        if self.connected:
            self.ctrl.setVoltage(outputVoltageVolts)
            self._logCurrent()

    def _logCurrent(self):
        log(self.name + "_outputCurrent", self.ctrl.getOutputCurrent(), "A")

    def getMotorPositionRad(self):
        if self.connected:
            pos = rev2Rad(self.encoder.getPosition())
        else:
            pos = 0
        log(self.name + "_motorActPos", pos, "rad")
        return pos

    def getMotorVelocityRadPerSec(self):
        if self.connected:
            vel = self.encoder.getVelocity()
        else:
            vel = 0
        vel = vel/60
        log(self.name + "_motorActVel", vel, "RPS")
        return RPM2RadPerSec(vel)

    def getAppliedOutput(self):
        if self.connected:
            output = self.ctrl.getAppliedOutput()
        else:
            output = 0
        output = 12 * output
        log(self.name + "_estOutputV", output, "V")
        return output

    def setSmartCurrentLimit():
        # @yavin get to this
        pass