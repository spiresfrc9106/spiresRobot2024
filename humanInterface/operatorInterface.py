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

        # Only used for manual testing
        self.manualIntakeVelFactor = 0.0
        self.manualTransferVelFactor = 0.0
        self.manualShooterVelFactor = 0.0

    def update(self):
        """Main update - call this once every 20ms"""

        if self.ctrl.isConnected():
            self.startIntake = self.ctrl.getYButtonPressed()
            self.startShooter = self.ctrl.getAButtonPressed()
            self.cancelNoteHandling = self.ctrl.getBButtonPressed()

            # Intake = Left stick 
            # Transfer = Right stick 
            # Shooter = Left stick + right bumper
            intakeRaw = -1.0 * self.ctrl.getLeftY() if not self.ctrl.getRightBumper() else 0.0
            transferRaw = -1.0 * self.ctrl.getRightY()
            shooterRaw = -1.0 * self.ctrl.getLeftY() if self.ctrl.getRightBumper() else 0.0
            self.manualIntakeVelFactor = applyDeadband(intakeRaw, 0.05)
            self.manualTransferVelFactor = applyDeadband(transferRaw, 0.05)
            self.manualShooterVelFactor = applyDeadband(shooterRaw, 0.05)

            self.climberCmd = self.ctrl.getRightBumper()

            self.connectedFault.setNoFault()
        else:
            self.startIntake = False
            self.startShooter = False
            self.cancelNoteHandling = False

            self.climberCmd = False

            self.manualIntakeVelFactor = 0.0
            self.manualTransferVelFactor = 0.0
            self.manualShooterVelFactor = 0.0

            self.connectedFault.setFaulted()

    def getStartIntakeCmd(self):
        return self.startIntake
    def getStartShooterCmd(self):
        return self.startShooter
    def getCancelNoteHandlingCmd(self):
        return self.cancelNoteHandling

    def getClimberCmd(self):
        return self.climberCmd

    def getManualIntakeVelocityFactory(self):
        return self.manualIntakeVelFactor
    def getManualTransferVelocityFactory(self):
        return self.manualTransferVelFactor
    def getManualShooterVelocityFactory(self):
        return self.manualShooterVelFactor