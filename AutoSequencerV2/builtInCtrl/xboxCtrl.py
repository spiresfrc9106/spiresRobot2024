from AutoSequencerV2.builtInCommands.xboxCtrlCommand import GameCtrl
from AutoSequencerV2.mode import Mode


# A DoNothingMode is an autonomous mode where the robot just sits doing nothing indefinitely
class XboxCtrl(Mode):
    def __init__(self):
        # Build a reasonable name out of the specified duration
        Mode.__init__(self, f"Game Controls")

    def getCmdGroup(self):
        return GameCtrl()
