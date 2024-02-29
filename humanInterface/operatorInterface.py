from wpilib import XboxController
from wpimath import applyDeadband
from utils.faults import Fault
from . import OPERATOR_CTRL_IDX

class OperatorInterface:
    """Class to gather input from the operator of the robot"""

    def __init__(self):
        self.ctrl = XboxController(OPERATOR_CTRL_IDX)

        self.connectedFault = Fault(f"Operator XBox Controller ({OPERATOR_CTRL_IDX}) Unplugged")

        self.startIntake = False
        self.startShooter = False
        self.cancelNoteHandling = False

        self.climberCmd = False

    def update(self):
        """Main update - call this once every 20ms"""

        if self.ctrl.isConnected():
            self.startIntake = self.ctrl.getYButtonPressed()
            self.startShooter = self.ctrl.getAButtonPressed()
            self.cancelNoteHandling = self.ctrl.getBButtonPressed()

            self.climberCmd = self.ctrl.getRightBumper()

            self.connectedFault.setNoFault()
        else:
            self.startIntake = False
            self.startShooter = False
            self.cancelNoteHandling = False

            self.climberCmd = False

            self.connectedFault.setFaulted()

    def getStartIntakeCmd(self):
        return self.startIntake
    def getStartShooterCmd(self):
        return self.startShooter
    def getCancelNoteHandlingCmd(self):
        return self.cancelNoteHandling

    def getClimberCmd(self):
        return self.climberCmd
