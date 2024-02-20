from utils.singleton import Singleton
#from utils import constants, faults
from wrappers.wrapperedSparkMax import WrapperedSparkMax


class Constants:

    # Electrical #
    INTAKE1_SPARK_MAX_ID = 11
    TRANSFER1_SPARK_MAX_ID = 12
    TRANSFER2_SPARK_MAX_ID = 13
    SHOOTER1_SPARK_MAX_ID = 14
    SHOOTER2_SPARK_MAX_ID = 15

    # Physical #
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


class Transfer(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.TRANSFER1_SPARK_MAX_ID, name="Transfer1")
        self.motor2 = WrapperedSparkMax(canID=Constants.TRANSFER2_SPARK_MAX_ID, name="Transfer2")


class Shooter(metaclass=Singleton):
    def __init__(self):
        self.motor1 = WrapperedSparkMax(canID=Constants.SHOOTER1_SPARK_MAX_ID, name="Shooter1")
        self.motor2 = WrapperedSparkMax(canID=Constants.SHOOTER2_SPARK_MAX_ID, name="Shooter2")


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        # initiate motors, etc

        self.intake = Intake()
        self.transfer = Transfer()
        self.shooter = Shooter()

        self.current_state = NoteState.DefaultEmpty

    def update(self):
        match self.current_state:
            case NoteState.ApproachingNote:
                pass
            case NoteState.DockingTransfer:
                pass
            case NoteState.ExitingTransfer:
                pass
            case NoteState.StoppingForward:
                pass
            case NoteState.ReversingAction:
                pass
            case NoteState.StoppingReverse:
                pass
            case NoteState.ShooterPrepared:
                pass
            case NoteState.AimingActivated:
                pass
            case NoteState.TransferNudging:
                pass
            case NoteState.PropelSucceeded:
                pass
            case NoteState.DefaultEmpty:
                pass
            case _:
                pass

