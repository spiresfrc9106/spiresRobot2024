import typing
from wpilib.interfaces import GenericHID

from debugMaster.debug import Debug

class XboxOneXController(GenericHID):
    '''
    This class is just a button and stick index remapping
    WPILib does not guarantee that controls will behave the same in sim
    '''
    kLeftTrigger: typing.ClassVar[int] = 4
    kLeftX: typing.ClassVar[int] = 0
    kLeftY: typing.ClassVar[int] = 1
    kRightTrigger: typing.ClassVar[int] = 3
    kRightX: typing.ClassVar[int] = 2
    kRightY: typing.ClassVar[int] = 5

    kA: typing.ClassVar[int] = 1
    kB: typing.ClassVar[int] = 2
    kLeftBumper: typing.ClassVar[int] = 7
    kRightBumper: typing.ClassVar[int] = 8
    kX: typing.ClassVar[int] = 4
    kY: typing.ClassVar[int] = 5

    def __init__(self, port: int):
        super().__init__(port)
        self.dbg = Debug()

    def getLeftY(self):
        return super().getRawAxis(self.kLeftY) * -1.0

    def getLeftX(self):
        return super().getRawAxis(self.kLeftX) * -1.0

    def getRightY(self):
        return super().getRawAxis(self.kRightY)

    def getRightX(self):
        return super().getRawAxis(self.kRightX)

    def getAButtonPressed(self):
        return super().getRawButtonPressed(self.kA)

    def getBButton(self):
        return super().getRawButton(self.kB)
    def getBButtonPressed(self):
        return super().getRawButtonPressed(self.kB)

    def getXButtonPressed(self):
        return super().getRawButtonPressed(self.kX)

    def getYButtonPressed(self):
        return super().getRawButtonPressed(self.kY)

    def getRightBumper(self):
        return super().getRawButton(self.kRightBumper)

    def getLeftBumper(self):
        return super().getRawButton(self.kLeftBumper)
