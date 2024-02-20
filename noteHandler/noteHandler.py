from utils.singleton import Singleton
#from utils import constants, faults

from wrappers.wrapperedSparkMax import WrapperedSparkMax


class NoteSystem:
    stateApproachingNote = "DrivingTowards"
    stateDockingTransfer = "EntersTransfer"
    stateExitingTransfer = "ExitedTransfer"
    stateStoppingForward = "HaltingForward"
    stateReversingAction = "ReverseActions"
    stateStoppingReverse = "HaltingReverse"
    stateShooterPrepared = "ShooterPrepped"


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        # initiate motors, etc
        self.motor = WrapperedSparkMax()

        current_state = NoteSystem.stateApproachingNote4

        if current_state == NoteSystem.stateShooterPrepared

