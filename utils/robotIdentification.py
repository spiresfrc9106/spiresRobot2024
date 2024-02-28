#The goal of this file is to identify which robot is currently running the code.
#The constants between practice and main robots may be different. 
from enum import Enum
import wpilib
#from utils.signalLogging import log
from utils.singleton import Singleton
RobotTypes = Enum('RobotTypes', ['Main','Practice','TestBoard'])

class RobotIdentification(metaclass=Singleton):

    def __init__(self):
        self.roboControl = wpilib.RobotController
        self.robotType = RobotTypes.Main
        self.serialFault = False    
        self.robotTypeNumber = 0
        print(f"roborio SerialNumber={self.roboControl.getSerialNumber()}")
        
    def configureValue(self):

        self.serialFault = False

        if self.roboControl.getSerialNumber() == "03134d41": #the L3
            self.robotType = RobotTypes.Main 
            self.robotTypeNumber = 1
        elif self.roboControl.getSerialNumber() == "03064e3f":  #the L2
            self.robotType = RobotTypes.Practice
            self.robotTypeNumber = 2
        elif self.roboControl.getSerialNumber() == "0316b37c":  
            #Test to see if the RoboRio serial number is our testboard's serial number.
            self.robotType = RobotTypes.TestBoard
            self.robotTypeNumber = 3
        else:
            #If the Robo Rio's serial number is not equal to any of our known serial numbers, 
            #assume we are the main robot
            self.robotType = RobotTypes.Main
            self.serialFault = True
            self.robotTypeNumber = 0
                
        #I don't know why the logs aren't working. But it's printing so I give up. 
            
    def getRobotType(self):
        return self.robotType 
    
    def getRobotSerialNumber(self):
        return self.roboControl.getSerialNumber()
    
    def getSerialFaulted(self):
        return self.serialFault
    
    def getRobotTypeNumber(self):
        return self.robotTypeNumber