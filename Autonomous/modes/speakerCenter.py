from Autonomous.commands.drivePathCommand import DrivePathCommand
from AutoSequencerV2.mode import Mode
from utils.allianceTransformUtils import transform

# Just drives out of the starting zone. That's all. 
class SpeakerCenter(Mode):
    def __init__(self):
        Mode.__init__(self, f"Speaker Center")
        self.pathCmd = DrivePathCommand("SpeakerCenter")

    def getCmdGroup(self):
        # Just return the path command
        return self.pathCmd

    def getInitialDrivetrainPose(self):
        # Use the path command to specify the starting pose
        retVal = self.pathCmd.path.getInitialPose()
        return transform(retVal)
