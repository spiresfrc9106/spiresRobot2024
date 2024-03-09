import typing
from wpilib.interfaces import GenericHID

from debugMaster.debug import Debug


class GenericXboxController(GenericHID):
    '''
    This class allows us to swap between XBox 360 and XBox One X Controls easily

    Always default to XBox360 for safety
    '''
    class XBox360Mapping:
        # Sticks and Triggers
        kLeftTrigger: typing.ClassVar[int] = 2
        kLeftX: typing.ClassVar[int] = 0
        kLeftY: typing.ClassVar[int] = 1
        kRightTrigger: typing.ClassVar[int] = 3
        kRightX: typing.ClassVar[int] = 4
        kRightY: typing.ClassVar[int] = 5
        # Buttons
        kA: typing.ClassVar[int] = 1
        kB: typing.ClassVar[int] = 2
        kBack: typing.ClassVar[int] = 7
        kLeftBumper: typing.ClassVar[int] = 5
        kLeftStick: typing.ClassVar[int] = 9
        kRightBumper: typing.ClassVar[int] = 6
        kRightStick: typing.ClassVar[int] = 10
        kStart: typing.ClassVar[int] = 8
        kX: typing.ClassVar[int] = 3
        kY: typing.ClassVar[int] = 4
    class XboxOneXMapping:
        # Sticks and Triggers
        kLeftTrigger: typing.ClassVar[int] = 4
        kLeftX: typing.ClassVar[int] = 0
        kLeftY: typing.ClassVar[int] = 1
        kRightTrigger: typing.ClassVar[int] = 3
        kRightX: typing.ClassVar[int] = 2
        kRightY: typing.ClassVar[int] = 5
        # Buttons
        kA: typing.ClassVar[int] = 1
        kB: typing.ClassVar[int] = 2
        kLeftBumper: typing.ClassVar[int] = 7
        kRightBumper: typing.ClassVar[int] = 8
        kX: typing.ClassVar[int] = 4
        kY: typing.ClassVar[int] = 5

    def __init__(self, port: int):
        super().__init__(port)
        self.mapping = None
        self.setControllerMapping()

    def update(self):
        if self.mapping is None:
            self.setControllerMapping()

    def setControllerMapping(self):
        if super().isConnected():
            if (super().getType() == GenericHID.HIDType.kHIDJoystick and
                super().getName() == "Xbox Wireless Controller"):
                self.mapping = self.XboxOneXMapping()
            else:
                self.mapping = self.XBox360Mapping()

    def getControllerMapping(self):
        if self.mapping is not None:
            return self.mapping
        else:
            return self.XBox360Mapping()

    def resetControllerMapping(self):
        self.mapping = None
    
    def getAButton(self):
        return super().getRawButton(self.getControllerMapping().kA)
    def getAButtonPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kA)
    def getAButtonReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kA)

    def getBButton(self):
        return super().getRawButton(self.getControllerMapping().kB)
    def getBButtonPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kB)
    def getBButtonReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kB)

    def getXButton(self):
        return super().getRawButton(self.getControllerMapping().kX)
    def getXButtonPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kX)
    def getXButtonReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kX)

    def getYButton(self):
        return super().getRawButton(self.getControllerMapping().kY)
    def getYButtonPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kY)
    def getYButtonReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kY)

    def getLeftBumper(self):
        return super().getRawButton(self.getControllerMapping().kLeftBumper)
    def getLeftBumperPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kLeftBumper)
    def getLeftBumperReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kLeftBumper)

    def getRightBumper(self):
        return super().getRawButton(self.getControllerMapping().kRightBumper)
    def getRightBumperPressed(self):
        return super().getRawButtonPressed(self.getControllerMapping().kRightBumper)
    def getRightBumperReleased(self):
        return super().getRawButtonReleased(self.getControllerMapping().kRightBumper)

    def getLeftX(self):
        return super().getRawAxis(self.getControllerMapping().kLeftX)
    def getLeftY(self):
        return super().getRawAxis(self.getControllerMapping().kLeftY)

    def getRightX(self):
        return super().getRawAxis(self.getControllerMapping().kRightX)
    def getRightY(self):
        return super().getRawAxis(self.getControllerMapping().kRightY)
