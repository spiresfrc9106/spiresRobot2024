from AutoSequencerV2.smartDashboardModeList import SmartDashboardModeList
from AutoSequencerV2.builtInModes.doNothingMode import DoNothingMode
from AutoSequencerV2.builtInModes.waitMode import WaitMode
from AutoSequencerV2.builtInCtrl.caliCtrl import CaliCtrl
from AutoSequencerV2.builtInCtrl.xboxCtrl import XboxCtrl
from Autonomous.modes.driveOut import DriveOut

# pylint: disable=R0801


def makeCtrlModeList():
    # We are putting the autonomous main mode list on the SmartDashboard
    ctrlModeList = SmartDashboardModeList("Ctrl")
    ctrlModeList.addMode(XboxCtrl())
    ctrlModeList.addMode(CaliCtrl())
    ctrlModeList.listIsComplete()
    return ctrlModeList

def makeDelayModeList():
    # We are putting the autonomous delay mode list on the SmartDashboard
    delayModeList = SmartDashboardModeList("Delay")
    delayModeList.addMode(WaitMode(0.0))
    delayModeList.addMode(WaitMode(3.0))
    delayModeList.addMode(WaitMode(6.0))
    delayModeList.addMode(WaitMode(9.0))
    delayModeList.listIsComplete()
    return delayModeList

def makeMainModeList():
    # We are putting the autonomous main mode list on the SmartDashboard
    mainModeList = SmartDashboardModeList("Main")
    mainModeList.addMode(DoNothingMode())
    mainModeList.addMode(DriveOut())
    mainModeList.listIsComplete()
    return mainModeList