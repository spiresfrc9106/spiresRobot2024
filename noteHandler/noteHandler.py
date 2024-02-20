from utils.singleton import Singleton
#from utils import constants, faults

from wrappers.wrapperedSparkMax import WrapperedSparkMax


class NoteStateMachine:

    def __init__(self):
        self.initial_state = "idle"
        self.current_state = self.initial_state
        self.initState_transition_endState = {
            "idle": {
                "initiateIntake": "intaking"
            },
            "intaking": {
                "noteEnteredTransfer": "enteringTransfer",
                "cancelIntake": "idle"
            },
            "enteringTransfer": {
                "noteExitedTransfer": "exitingTransfer"
            },
            "exitingTransfer": {
                "noteInRightSpot": "readyToShoot",
                "noteNeedsAdjustment": "reverseTransferAdjustment"
            },
            "reverseTransferAdjustment": {
                "noteInRightSpot": "readyToShoot"
            },
            "readyToShoot": {
                "shooterTriggered": "preppingShooter"
            },
            "preppingShooter": {
                "shooterReady": "shooting"
            },
            "shooting": {
                "noteShot": "idle"
            }
        }

    def transition(self, transition):
        if transition in self.initState_transition_endState[self.current_state]:
            self.current_state = self.initState_transition_endState[self.current_state][transition]
        else:
            raise Exception(f'Invalid transition from {self.current_state} with transtion {transition}')


class NoteHandler(metaclass=Singleton):
    def __init__(self):
        self.stateMachine = NoteStateMachine()
        # initiate motors, etc
        self.motor = WrapperedSparkMax()

    def update(self):
        self.stateMachine.transition("initiateIntake")
