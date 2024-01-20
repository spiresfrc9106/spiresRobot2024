import wpilib

# A mode list is the set of autonomous modes that the drive team must pick from before a match
# Networktables is used to read the user's current selection
class SmartDashboardModeList():
    def __init__(self, name):
        self.modes = []
        self._name = name
        self.curModeIdx = 0 # default

        # This shows the user two options on the SmartDashboard
        self.desChooser = wpilib.SendableChooser()

        
    def addMode(self, modeIn):
        numOfModes = len(self.modes)
        if len(self.modes) == 0:
            self.desChooser.setDefaultOption(modeIn.getName(), numOfModes)
        else:
            self.desChooser.addOption(modeIn.getName(), numOfModes)
        self.modes.append(modeIn)
        #wpilib.SmartDashboard.putData(self.getDesModeTopicName(), self.desChooser)

    def updateMode(self, force=False):
        prevModeIdx = self.curModeIdx
        tmp = self.desChooser.getSelected()
        if(prevModeIdx != tmp or force):
            self.curModeIdx = tmp
            wpilib.SmartDashboard.putString(self.getCurModeTopicName(),self.modes[self.curModeIdx].getName())
        return prevModeIdx != self.curModeIdx # Return true if the selection has changed
        
    def getCurMode(self):
        #print(f"modeList.modes.len={len(self.modes)}, {self.curModeIdx}",flush=True)
        return self.modes[self.curModeIdx]
        
    def getNames(self):
        return [x.getName() for x in self.modes]
    
    def getDesModeTopicName(self): 
        return "des_" + self._name

    def getCurModeTopicName(self):
        return "cur_" + self._name
    
    def getModeTopicBase(self):
        return f"/SmartDashboard"

    def listIsComplete(self):
        wpilib.SmartDashboard.putData(self.getDesModeTopicName(), self.desChooser)
        wpilib.SmartDashboard.putString(self.getCurModeTopicName(), self.modes[self.curModeIdx].getName())
