from wpilib import DigitalInput
from utils.singleton import Singleton
from utils.units import in2m
from wrappers.wrapperedSparkMax import WrapperedSparkMax
from debugMaster.debug import Debug


class Constants:
    USE_AFF = True
    SPEED_FACTOR = 1

    # Speed Control #
    INTAKE_VEL_RPS = 3.75 * SPEED_FACTOR
    TRANSFER_FORWARD_VEL_RPS = 3.75 * SPEED_FACTOR
    TRANSFER_REVERSE_VEL_RPS = -1 * 0.75 * SPEED_FACTOR
    SHOOTER_VEL_RPS = 50 * SPEED_FACTOR
    TRANSFER_NUDGING_VEL_RPS = 1 * SPEED_FACTOR

    # Electrical #
    INTAKE1_SPARK_MAX_ID = 11
    TRANSFER1_SPARK_MAX_ID = 12
    TRANSFER2_SPARK_MAX_ID = 13
    SHOOTER1_SPARK_MAX_ID = 14
    SHOOTER2_SPARK_MAX_ID = 15
    OPTICAL_SENSOR_1_DIO_CHANNEL=5
    OPTICAL_SENSOR_2_DIO_CHANNEL=6
    
    # Mechanical #
    UPLANETARY_3TO1 = 2.89
    UPLANETARY_4TO1 = 3.61
    UPLANETARY_5TO1 = 5.23

    TRANSFER_GEAR_ON_UPLANETARY = 26
    TRANSFER_GEAR_ON_SQUISHY = 42

    TRANSFER_REDUCTION = 10*UPLANETARY_4TO1 * UPLANETARY_5TO1 * TRANSFER_GEAR_ON_SQUISHY / TRANSFER_GEAR_ON_UPLANETARY
    SQUISH_FACTOR = 0.8
    TRANSFER_SQUISHY_CIRC_M = SQUISH_FACTOR*in2m(1.0)*2.0*3.14

    TRANSFER_MPS_PER_RPS = TRANSFER_SQUISHY_CIRC_M / TRANSFER_REDUCTION

    EXP_TRANSFER_INTAKE_MPS = 0.01

    EXP_TRANSFER_MOTOR_RPS = EXP_TRANSFER_INTAKE_MPS / TRANSFER_MPS_PER_RPS

class Intake(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.INTAKE1_SPARK_MAX_ID, 
                                        name="Intake1", brakeMode=True, curLimitA=6)
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps, aff=0.0):
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10

class Transfer(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.TRANSFER1_SPARK_MAX_ID,
                                        name="Transfer1", brakeMode=True, curLimitA=6)
        self.motor2 = WrapperedSparkMax(canID=Constants.TRANSFER2_SPARK_MAX_ID,
                                        name="Transfer2", brakeMode=True, curLimitA=6)
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motor2.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps, aff=0.0):
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)
        self.motor2.setVelRPS(rps, aff)

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10

class Shooter(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.SHOOTER1_SPARK_MAX_ID, name="Shooter1")
        self.motor2 = WrapperedSparkMax(canID=Constants.SHOOTER2_SPARK_MAX_ID, name="Shooter2")
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motor2.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps, aff=0.0):
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)
        self.motor2.setVelRPS(rps, aff)

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10


class Optical(metaclass=Singleton):
    def __init__(self):
        self.sensor1 = DigitalInput(Constants.OPTICAL_SENSOR_1_DIO_CHANNEL)
        self.sensor2 = DigitalInput(Constants.OPTICAL_SENSOR_2_DIO_CHANNEL)


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        self.intake = Intake()
        self.transfer = Transfer()
        self.shooter = Shooter()
        self.optical = Optical()
        self.debug = Debug()

        self.currentState = "idle"

        self.intakeStartCmd = False # Start intake roller
        self.shootCmd = False # Prep shooter and fire
        self.cancelHandlingCmd = False # DANGER: Reset entire process (also temporarily used post-shot)

        self.manualNoteHandlerControls = True # Bypass state-machine, test with joysticks, debugging only
        self.manualIntakeVelFactor = 0.0
        self.manualTransferVelFactor = 0.0
        self.manualShooterVelFactor = 0.0

    def setIntakeStartCmd(self, value: bool):
        self.intakeStartCmd = value
    def setShootCmd(self, value: bool):
        self.shootCmd = value
    def setCancelHandlingCmd(self, value: bool):
        self.cancelHandlingCmd = value

    def setManualIntakeVelFactor(self, value: float):
        self.manualIntakeVelFactor = value
    def setManualTransferVelFactor(self, value: float):
        self.manualTransferVelFactor = value
    def setManualShooterVelFactor(self, value: float):
        self.manualShooterVelFactor = value

    def scaledIntakeVelocityRps(self):
        # TODO: This makes the assumption that intake and transfer have the same conversion factor
        return self.manualIntakeVelFactor * Constants.EXP_TRANSFER_MOTOR_RPS
    def scaledTransferVelocityRps(self):
        return self.manualTransferVelFactor * Constants.EXP_TRANSFER_MOTOR_RPS
    def scaledShooterVelocityRps(self):
        maxVelocityRpm = 5000.0
        maxVelocityRps = maxVelocityRpm / 60.0
        return self.manualShooterVelFactor * maxVelocityRps

    def logMotorValues(self):
        motors = [self.intake.motor1, self.transfer.motor1, self.transfer.motor2, self.shooter.motor1, self.shooter.motor2]
        for motor in motors:
            motor.getVelRPS()
            motor.getAppliedOutput()

    def update(self):
        self.logMotorValues()

        if self.manualNoteHandlerControls:
            self.intake.setVelRPS(self.scaledIntakeVelocityRps())
            self.transfer.setVelRPS(self.scaledTransferVelocityRps())
            self.shooter.setVelRPS(self.scaledShooterVelocityRps())
            return

        if self.cancelHandlingCmd:
            self.currentState = "idle"

        match self.currentState:
            case "idle":
                self.cancelHandlingCmd = False
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
                if self.intakeStartCmd:
                    self.currentState = "intakeActive"
            case "intakeActive":
                self.intakeStartCmd = False
                self.intake.setVelRPS(Constants.INTAKE_VEL_RPS)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
                if self.optical.sensor1.get():
                    self.currentState = "transferForward"
            case "transferForward":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(Constants.TRANSFER_FORWARD_VEL_RPS)
                self.shooter.setVelRPS(0)
                # this transition assumes that we will not miss a sensor reading
                if self.optical.sensor2.get():
                    self.currentState = "transferForwardComplete"
            case "transferForwardComplete":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
                # TODO: validate this threshold
                if self.transfer.motor1.getVelRPS() < Constants.TRANSFER_FORWARD_VEL_RPS * 0.1:
                    if self.optical.sensor2.get():
                        self.currentState = "readyToShoot"
                    else:
                        self.currentState = "transferRevAdjust"
            case "transferRevAdjust":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(Constants.TRANSFER_REVERSE_VEL_RPS)
                self.shooter.setVelRPS(0)
                # this transition assumes that we will not miss a sensor reading
                # We could also maybe make the adjustment based on a known rotation of the transfer motor
                if self.optical.sensor2.get():
                    self.currentState = "readyToShoot"
            case "readyToShoot":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
                if self.shootCmd:
                    self.currentState = "warmupShooter"
            case "warmupShooter":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(Constants.SHOOTER_VEL_RPS)
                # TODO: validate this threshold 
                if self.shooter.motor1.getVelRPS() > Constants.SHOOTER_VEL_RPS * 0.95:
                    self.currentState = "shooting"
            case "shooting":
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(Constants.TRANSFER_NUDGING_VEL_RPS)
                self.shooter.setVelRPS(Constants.SHOOTER_VEL_RPS)
                if self.cancelHandlingCmd:
                    self.currentState = "idle"
            case _:
                self.debug.print("error", f"Unexpected state in Note Handler: {self.currentState}")
                self.currentState = "idle"
