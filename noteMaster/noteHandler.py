from wpilib import DigitalInput
from debugMaster.debug import Debug
from utils.singleton import Singleton
from utils.units import (
    in2m,
)
#from utils import constants, faults
from wrappers.wrapperedSparkMax import WrapperedSparkMax

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
    INTAKE1_SPARK_MAX_ID = 13
    TRANSFER1_SPARK_MAX_ID = 11
    TRANSFER2_SPARK_MAX_ID = 12
    SHOOTER1_SPARK_MAX_ID = 19
    SHOOTER2_SPARK_MAX_ID = 20
    
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


class NoteState:
    ApproachingNote = "ApproachingNote"  # ^ ctrl - intake-transfer motors on
    DockingTransfer = "DockingTransfer"  # ^ 1st optical sensor triggers once
    ExitingTransfer = "ExitingTransfer"  # ^ 2nd optical sensor triggers once (1st does trigger second time)
    StoppingForward = "StoppingForward"  # turn off all motors (intake, transfer)
    ReversingAction = "ReversingAction"  # reverse transfer motors [at slow speed]
    StoppingReverse = "StoppingReverse"  # stop transfer motors from reversing
    ShooterPrepared = "ShooterPrepared"  # the system is at rest awaiting drivers to commence shooting
    AimingActivated = "AimingActivated"  # ^ ctrl - shooter motors on, pick up to speed
    TransferNudging = "TransferNudging"  # ^ ctrl - transfer on, nudges note, shooter remains on
    PropelSucceeded = "PropelSucceeded"  # ^ given by amp Δ or time-based cancel?
    NoteJourneyDone = "NoteJourneyDone"  # power off transfer + shooter
    DefaultEmpty = "DefaultEmpty"     # normal driving around state


class Intake(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.INTAKE1_SPARK_MAX_ID,
                                        name="Intake1", brakeMode=True, curLimitA=6)
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps):
        aff = 0.0
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10


class Transfer(metaclass=Singleton):
    def __init__(self):
        invertMotor1 = True
        self.motor1 = WrapperedSparkMax(canID=Constants.TRANSFER1_SPARK_MAX_ID,
                                        name="Transfer1", brakeMode=True, curLimitA=6)
        self.motor2 = WrapperedSparkMax(canID=Constants.TRANSFER2_SPARK_MAX_ID,
                                        name="Transfer2", brakeMode=True, curLimitA=6)
        self.motor1.setInverted(invertMotor1)
        self.motor2.setInverted(not invertMotor1)
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motor2.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps):
        aff = 0.0
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)
        self.motor2.setVelRPS(rps, aff)
        self.motor1.getVelRPS()
        self.motor1.getAppliedOutput()
        self.motor2.getVelRPS()
        self.motor2.getAppliedOutput()
    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10


class Shooter(metaclass=Singleton):
    def __init__(self):
        invertMotors = False
        self.motor1 = WrapperedSparkMax(canID=Constants.SHOOTER1_SPARK_MAX_ID, name="Shooter1")
        self.motor2 = WrapperedSparkMax(canID=Constants.SHOOTER2_SPARK_MAX_ID, name="Shooter2")
        self.motor1.setInverted(invertMotors)
        self.motor1.setInverted(invertMotors)
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motor2.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps):
        aff=0.0
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)
        self.motor2.setVelRPS(rps, aff)
        self.motor1.getVelRPS()
        self.motor1.getAppliedOutput()
        self.motor2.getVelRPS()
        self.motor2.getAppliedOutput()

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10


class Optical(metaclass=Singleton):
    def __init__(self):
        self.sensor1 = DigitalInput(5)
        self.sensor2 = DigitalInput(6)


# class NoteStateMachine:
#     def __init__(self):
#         self.initial_state = "idle"
#         self.current_state = self.initial_state
#         self.initState_transition_endState = {
#             "idle": {
#                 "initiateIntake": "drivingTowards"
#             },
#             "drivingTowards": {
#                 "opticalTrue1": "enteringTransfer",
#                 "cancelIntake": "idle"
#             },
#             "enteringTransfer": {
#                 "opticalTrue2": "exitingTransfer"
#             },
#             "exitingTransfer": {
#                 "noteInRightSpot": "readyToShoot",
#                 "noteNeedsAdjustment": "reverseTransferAdjustment"
#             },
#             "reverseTransferAdjustment": {
#                 "noteInRightSpot": "shooterLoaded"
#             },
#             "shooterLoaded": {
#                 "shooterStart": "startingShooter"
#             },
#             "startingShooter": {
#                 "shooterReady": "awaitingTrigger"
#             },
#             "awaitingTrigger": {
#                 "triggerPressed": "pushingNote"
#             },
#             "pushingNote": {
#                 "noteReleased": "systemReset"
#             },
#             "systemReset": {
#                 "motorsStopped": "idle"
#             },
#         }


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        # initiate motors, etc

        self.intake = Intake()
        self.transfer = Transfer()
        self.shooter = Shooter()
        self.optical = Optical()
        self.debug = Debug()

        self.prevState = NoteState.DefaultEmpty
        self.currentState = NoteState.DefaultEmpty

        #self.intakeCmd = False
        self.aimingCmd = False
        self.propelCmd = False
        self.intakVelFactor = 0.0
        self.shootVelVactor = 0.0

    def setVelocityFactors(self, intakeVelFactor: float, shootVelFactor: float):
        self.intakVelFactor = intakeVelFactor
        self.shootVelVactor = shootVelFactor


    def runIntake(self):
        return abs(self.intakVelFactor)>0

    def runShooter(self):
        return abs(self.shootVelVactor)>0


    def scaledTransferVelocityRps(self):
        return self.intakVelFactor * Constants.EXP_TRANSFER_MOTOR_RPS

    def scaledShooterVelocityRps(self):
        maxVelocityRpm = 5000.0
        maxVelocityRps = maxVelocityRpm / 60.0
        return self.shootVelVactor * maxVelocityRps

    def setIntakeVelocity(self):
        self.intake.setVelRPS(0.0) #TODO fix me up

    def zeroIntakeVelocity(self):
        self.intake.setVelRPS(0)

    def setTransferVelocity(self):
        self.transfer.setVelRPS(self.scaledTransferVelocityRps())

    def zeroTransferVelocity(self):
        self.transfer.setVelRPS(0)

    def setShooterVelocity(self):
        self.shooter.setVelRPS(self.scaledShooterVelocityRps())

    def zeroShooterVelocity(self):
        self.shooter.setVelRPS(0)

    def switch(self, state):
        self.currentState = state

    def update(self):
        #self.debug.print("note", f"Optical Sensor1:{self.optical.sensor1.get()}")
        if self.currentState != self.prevState:
            self.debug.print("note", f"switching from {self.prevState} to {self.currentState}")
            self.prevState = self.currentState
        match self.currentState:
            case NoteState.DefaultEmpty:
                self.zeroIntakeVelocity()
                self.zeroTransferVelocity()
                self.zeroShooterVelocity()
                if self.runIntake() or self.runShooter():
                    self.switch(NoteState.ApproachingNote)
            case NoteState.ApproachingNote:
                self.intake.setVelRPS(Constants.INTAKE_VEL_RPS)
                self.setTransferVelocity()
                self.setShooterVelocity()
                if not (self.runIntake() or self.runShooter()):
                    self.switch(NoteState.DefaultEmpty)
                #if not self.optical.sensor1.get():
                #        self.switch(NoteState.DockingTransfer)
            case NoteState.DockingTransfer:
                if not self.optical.sensor2.get():
                    self.switch(NoteState.ExitingTransfer)
            case NoteState.ExitingTransfer:
                self.switch(NoteState.StoppingForward)
            case NoteState.StoppingForward:
                self.zeroIntakeVelocity()
                self.zeroTransferVelocity()
                speed = 0.5 * (self.transfer.motor1.getVelRPS() + self.transfer.motor1.getVelRPS())
                if speed < 1.0:
                    self.switch(NoteState.ReversingAction)
            case NoteState.ReversingAction:
                self.transfer.setVelRPS(Constants.TRANSFER_REVERSE_VEL_RPS)
            case NoteState.StoppingReverse:
                self.zeroTransferVelocity()
            case NoteState.ShooterPrepared:
                if self.aimingCmd:
                    self.switch(NoteState.AimingActivated)
            case NoteState.AimingActivated:
                self.shooter.setVelRPS(Constants.SHOOTER_VEL_RPS)
                if self.propelCmd:
                    self.switch(NoteState.TransferNudging)
            case NoteState.TransferNudging:
                self.transfer.setVelRPS(Constants.TRANSFER_NUDGING_VEL_RPS)
                # @yavin need some sort of auto-driven functionality to wait until shooting success
            case NoteState.PropelSucceeded:
                self.zeroIntakeVelocity()
                self.zeroTransferVelocity()
                self.zeroShooterVelocity()
            case _:
                self.debug.print("error", "error with state machine; no value found")
                self.zeroIntakeVelocity()
                self.zeroTransferVelocity()
                self.zeroShooterVelocity()