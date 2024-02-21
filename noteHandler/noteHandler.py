from utils.singleton import Singleton
#from utils import constants, faults
from wrappers.wrapperedSparkMax import WrapperedSparkMax
from wpilib import DigitalInput


class Constants:

    # Electrical #
    INTAKE1_SPARK_MAX_ID = 11
    TRANSFER1_SPARK_MAX_ID = 12
    TRANSFER2_SPARK_MAX_ID = 13
    SHOOTER1_SPARK_MAX_ID = 14
    SHOOTER2_SPARK_MAX_ID = 15
    
    # Speed Control #
    INTAKE_VEL_RPS = 1
    TRANSFER_FORWARD_VEL_RPS = 1
    TRANSFER_REVERSE_VEL_RPS = -1
    SHOOTER_VEL_RPS = 1
    TRANSFER_NUDGING_VEL_RPS = 1
    
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

    def setVelRPS(self, rps):
        self.motor1.setVelRPS(rps)

class Transfer(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.TRANSFER1_SPARK_MAX_ID, name="Transfer1")
        self.motor2 = WrapperedSparkMax(canID=Constants.TRANSFER2_SPARK_MAX_ID, name="Transfer2")

    def setVelRPS(self, rps):
        self.motor1.setVelRPS(rps)
        self.motor2.setVelRPS(rps)


class Shooter(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.SHOOTER1_SPARK_MAX_ID, name="Shooter1")
        self.motor2 = WrapperedSparkMax(canID=Constants.SHOOTER2_SPARK_MAX_ID, name="Shooter2")

    def setVelRPS(self, rps):
        self.motor1.setVelRPS(rps)
        self.motor2.setVelRPS(rps)


class Optical(metaclass=Singleton):
    def __init__(self):
        self.sensor1 = DigitalInput(5)
        self.sensor2 = DigitalInput(6)



class NoteStateMachine:
    def __init__(self):
        self.initial_state = "idle"
        self.current_state = self.initial_state
        self.initState_transition_endState = {
            "idle": {
                "initiateIntake": "drivingTowards"
            },
            "drivingTowards": {
                "opticalTrue1": "enteringTransfer",
                "cancelIntake": "idle"
            },
            "enteringTransfer": {
                "opticalTrue2": "exitingTransfer"
            },
            "exitingTransfer": {
                "noteInRightSpot": "readyToShoot",
                "noteNeedsAdjustment": "reverseTransferAdjustment"
            },
            "reverseTransferAdjustment": {
                "noteInRightSpot": "shooterLoaded"
            },
            "shooterLoaded": {
                "shooterStart": "startingShooter"
            },
            "startingShooter": {
                "shooterReady": "awaitingTrigger"
            },
            "awaitingTrigger": {
                "triggerPressed": "pushingNote"
            },
            "pushingNote": {
                "noteReleased": "systemReset"
            },
            "systemReset": {
                "motorsStopped": "idle"
            },
        }


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        # initiate motors, etc

        self.intake = Intake()
        self.transfer = Transfer()
        self.shooter = Shooter()
        self.optical = Optical()

        self.current_state = NoteState.DefaultEmpty

    def update(self):
        match self.current_state:
            case NoteState.ApproachingNote:
                self.intake.setVelRPS(Constants.INTAKE_VEL_RPS)
                self.transfer.setVelRPS(Constants.TRANSFER_FORWARD_VEL_RPS)
                pass
            case NoteState.DockingTransfer:
                pass
            case NoteState.ExitingTransfer:
                pass
            case NoteState.StoppingForward:
                self.intake.setVelRPS(0)
                self.transfer.setVelRPS(0)
                pass
            case NoteState.ReversingAction:
                self.transfer.setVelRPS(Constants.TRANSFER_REVERSE_VEL_RPS)
                pass
            case NoteState.StoppingReverse:
                self.transfer.setVelRPS(0)
                pass
            case NoteState.ShooterPrepared:
                pass
            case NoteState.AimingActivated:
                self.shooter.setVelRPS(Constants.SHOOTER_VEL_RPS)
                pass
            case NoteState.TransferNudging:
                self.transfer.setVelRPS(Constants.TRANSFER_NUDGING_VEL_RPS)
                pass
            case NoteState.PropelSucceeded:
                pass
            case NoteState.DefaultEmpty:
                pass
            case _:
                pass

