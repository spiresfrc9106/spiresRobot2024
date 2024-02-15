from AutoSequencerV2.modeList import ModeList
#from AutoSequencerV2.smartDashboardModeList import SmartDashboardModeList
from AutoSequencerV2.builtInModes.doNothingMode import DoNothingMode
from AutoSequencerV2.builtInModes.waitMode import WaitMode
from AutoSequencerV2.builtInCtrl.caliCtrl import CaliCtrl
from AutoSequencerV2.builtInCtrl.xboxCtrl import XboxCtrl
from Autonomous.modes.driveOut import DriveOut

# pylint: disable=R0801

def makeCtrlModeList():
    # We are putting the autonomous main mode list on the SmartDashboard
    ctrlModeList = ModeList("Ctrl")
    ctrlModeList.addMode(XboxCtrl())
    ctrlModeList.addMode(CaliCtrl())
    return ctrlModeList

def makeDelayModeList():
    # We are putting the autonomous delay list on the WebServer
    delayModeList = ModeList("Delay")
    delayModeList.addMode(WaitMode(0.0))
    delayModeList.addMode(WaitMode(3.0))
    delayModeList.addMode(WaitMode(6.0))
    delayModeList.addMode(WaitMode(9.0))
    return delayModeList

def makeMainModeList():
    # We are putting the autonomous main mode list on the WebServer
    mainModeList = ModeList("Main")
    mainModeList.addMode(DoNothingMode())
    mainModeList.addMode(DriveOut())
    return mainModeList
