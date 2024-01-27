from wpimath.geometry import Pose2d
from wpilib import DriverStation
from AutoSequencerV2.modeList import ModeList
from AutoSequencerV2.builtInModes.doNothingMode import DoNothingMode
from AutoSequencerV2.builtInCtrl.caliCtrl import CaliCtrl
from AutoSequencerV2.builtInCtrl.xboxCtrl import XboxCtrl
from AutoSequencerV2.builtInModes.waitMode import WaitMode
from AutoSequencerV2.sequentialCommandGroup import SequentialCommandGroup
from utils.singleton import Singleton
from utils.allianceTransformUtils import onRed


class TeleConditions(metaclass=Singleton):
    """Top-level implementation of the AutoSequencer"""

    def __init__(self):
        # Have different delay modes for delaying the start of autonomous
        self.ctrlModeList = ModeList("Ctrl")
        self.ctrlModeList.addMode(XboxCtrl())
        self.ctrlModeList.addMode(CaliCtrl())

        self.topLevelCmdGroup = SequentialCommandGroup()
        self.startPose = Pose2d()

        # Alliance changes require us to re-plan autonomous
        # This variable is used to help track when alliance changes
        self._prevOnRed = onRed()
        self.veloTest = False

        self.updateMode(force=True)  # Ensure we load the teleop conditions at least once.


    # Call this periodically while disabled to keep the dashboard updated
    # and, when things change, re-init modes
    def updateMode(self, force=False):
        ctrlChanged = self.ctrlModeList.updateMode()
        if ctrlChanged or force:
            ctrlMode = self.ctrlModeList.getCurMode()
            self.topLevelCmdGroup = ctrlMode.getCmdGroup()
            if ctrlMode.getName() == "Testing Controls":
                self.veloTest = True
            else:
                self.veloTest = False
            print(
                f"[Tele] New Modes Selected:  {ctrlMode.getName()}"
            )

    # Call this once during autonmous init to init the current command sequence

    def end(self):
        self.topLevelCmdGroup.end(True)
        print("[Auto] Sequencer Stopped")

    def getCtrlModeList(self):
        return self.ctrlModeList.getNames()

    def getCtrlModeNTTableName(self):
        return self.ctrlModeList.getModeTopicBase()

    def getStartingPose(self):
        return self.startPose
