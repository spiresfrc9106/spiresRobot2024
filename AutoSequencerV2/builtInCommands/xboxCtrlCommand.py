from AutoSequencerV2.command import Command
from drivetrain.drivetrainTrajectoryControl import DrivetrainTrajectoryControl

class GameCtrl(Command):

    def __init__(self):
        self.trajCtrl = DrivetrainTrajectoryControl()

    def initialize(self):
        DrivetrainTrajectoryControl.veloTest = False

    def isDone(self):
        return False

    def getName(self):
        return f"Game Controllers"