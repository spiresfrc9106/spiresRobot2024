from AutoSequencerV2.command import Command
from drivetrain.drivetrainTrajectoryControl import DrivetrainTrajectoryControl

class TestCtrl(Command):

    def __init__(self):
        self.trajCtrl = DrivetrainTrajectoryControl()

    def initialize(self):
        DrivetrainTrajectoryControl.veloTest = True

    def isDone(self):
        return False

    def getName(self):
        return f"Testing Controllers"
