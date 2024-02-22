from wpilib import DigitalInput
from utils.singleton import Singleton
#from utils import constants, faults
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
    
    # Mechanical #
    PLANETARY_GEAR_3TO1 = 2.89
    PLANETARY_GEAR_4TO1 = 3.61
    PLANETARY_GEAR_5TO1 = 5.23


class NoteState:
    ApproachingNote = "DrivingTowards"  # ^ ctrl - intake-transfer motors on
    DockingTransfer = "EntersTransfer"  # ^ 1st optical sensor triggers once
    ExitingTransfer = "ExitedTransfer"  # ^ 2nd optical sensor triggers once (1st does trigger second time)
    StoppingForward = "HaltingForward"  # turn off all motors (intake, transfer)
    ReversingAction = "ReverseActions"  # reverse transfer motors [at slow speed]
    StoppingReverse = "HaltingReverse"  # stop transfer motors from reversing
    ShooterPrepared = "ShooterPrepped"  # the system is at rest awaiting drivers to commence shooting
    AimingActivated = "ShooterReadied"  # ^ ctrl - shooter motors on, pick up to speed
    TransferNudging = "NudgeNoteShoot"  # ^ ctrl - transfer on, nudges note, shooter remains on
    PropelSucceeded = "ShotSuccessful"  # ^ given by amp Δ or time-based cancel?
    NoteJourneyDone = "TrackCompleted"  # power off transfer + shooter
    DefaultEmpty = "DefaultEmptied"     # normal driving around state


class Intake(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.INTAKE1_SPARK_MAX_ID, name="Intake1")
        self.motor1.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

    def setVelRPS(self, rps, aff=0.0):
        if Constants.USE_AFF:
            aff = self.getEstAFF(rps)
        self.motor1.setVelRPS(rps, aff)

    def getEstAFF(self, velocityRPS):
        return 0.12 * velocityRPS + 0.10


class Transfer(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.TRANSFER1_SPARK_MAX_ID, name="Transfer1")
        self.motor2 = WrapperedSparkMax(canID=Constants.TRANSFER2_SPARK_MAX_ID, name="Transfer2")
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
        self.sensor1 = DigitalInput(4)  #5
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

        self.intakeCmd = False
        self.aimingCmd = False
        self.propelCmd = False


    def switch(self, state):
        self.currentState = state

    def update(self):
        self.debug.print("note", self.optical.sensor1.get())
        if self.currentState != self.prevState:
            self.debug.print("note", f"switching from {self.prevState} to {self.currentState}")
            self.prevState = self.currentState
        match self.currentState:
            case NoteState.DefaultEmpty:
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
                if self.intakeCmd:
                    self.switch(NoteState.ApproachingNote)
            case NoteState.ApproachingNote:
                self.intake.setVelRPS(Constants.INTAKE_VEL_RPS)
                self.transfer.setVelRPS(Constants.TRANSFER_FORWARD_VEL_RPS)
                if not self.optical.sensor1.get():
                    self.switch(NoteState.DockingTransfer)
            case NoteState.DockingTransfer:
                if not self.optical.sensor2.get():
                    self.switch(NoteState.ExitingTransfer)
            case NoteState.ExitingTransfer:
                self.switch(NoteState.StoppingForward)
            case NoteState.StoppingForward:
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                speed = 0.5 * (self.transfer.motor1.getVelRPS() + self.transfer.motor1.getVelRPS())
                if speed < 1.0:
                    self.switch(NoteState.ReversingAction)
            case NoteState.ReversingAction:
                self.transfer.setVelRPS(Constants.TRANSFER_REVERSE_VEL_RPS)
            case NoteState.StoppingReverse:
                self.transfer.setVelRPS(0)
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
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
            case _:
                self.debug.print("error", "error with state machine; no value found")
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                self.shooter.setVelRPS(0)
