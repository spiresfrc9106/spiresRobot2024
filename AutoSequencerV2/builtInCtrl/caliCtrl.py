from AutoSequencerV2.builtInCommands.caliCtrlCommand import TestCtrl
from AutoSequencerV2.mode import Mode


# A WaitMode is an autonomous mode where the robot just sits doing nothing for a specified duration.
class CaliCtrl(Mode):
    def __init__(self):
        # Build a reasonable name out of the specified duration
        Mode.__init__(self, f"Testing Controls")

    def getCmdGroup(self):
        return TestCtrl()
