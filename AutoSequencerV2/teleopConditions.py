from wpimath.geometry import Pose2d
#from wpilib import DriverStation
#from wpimath.controller import PIDController
#from wpimath.kinematics import ChassisSpeeds
from utils.calibration import Calibration
from utils.singleton import Singleton
from utils.allianceTransformUtils import onRed
#from utils.signalLogging import log
#from utils.mathUtils import limit
#from AutoSequencerV2.builtInModes.doNothingMode import DoNothingMode
#from AutoSequencerV2.builtInModes.waitMode import WaitMode
from AutoSequencerV2.modeList import ModeList
from AutoSequencerV2.builtInCtrl.caliCtrl import CaliCtrl
from AutoSequencerV2.builtInCtrl.xboxCtrl import XboxCtrl
from AutoSequencerV2.sequentialCommandGroup import SequentialCommandGroup
from debugMaster.debug import Debug


class Wheel:
    def __init__(self, velocity, angle):
        self.velocity = velocity
        self.angle = angle

class TeleConditions(metaclass=Singleton):
    """Top-level implementation of the AutoSequencer"""

    def __init__(self):

        self.wheelFL = Wheel(Calibration("Wheel FL Velocity", 0.0), Calibration("Wheel FL Angle", 0.0))
        self.wheelFR = Wheel(Calibration("Wheel FR Velocity", 0.0), Calibration("Wheel FR Angle", 0.0))
        self.wheelBL = Wheel(Calibration("Wheel BL Velocity", 0.0), Calibration("Wheel BL Angle", 0.0))
        self.wheelBR = Wheel(Calibration("Wheel BR Velocity", 0.0), Calibration("Wheel BR Angle", 0.0))

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
        self.updateCount = 0

        self.updateMode(force=True)  # Ensure we load the teleop conditions at least once.


    # Call this periodically while disabled to keep the dashboard updated
    # and, when things change, re-init modes
    def updateMode(self, force=False):
        self.updateCount = self.updateCount+1
        Debug().print('velState', f"in TeleConditions.updateMode {self.updateCount}")
        ctrlChanged = self.ctrlModeList.updateMode()
        if ctrlChanged or force:
            ctrlMode = self.ctrlModeList.getCurMode()
            self.topLevelCmdGroup = ctrlMode.getCmdGroup()
            if ctrlMode.getName() == "Testing Controls":
                self.veloTest = True
            else:
                self.veloTest = False
            Debug().print('velState', f"veloTest={self.veloTest}")
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

    def getWheelControl(self, name, item):
        wheel = getattr(self, 'wheel' + name, None)
        if wheel:
            temp = getattr(wheel, item, None)
            return temp.get()
        else:
            return 0.0
