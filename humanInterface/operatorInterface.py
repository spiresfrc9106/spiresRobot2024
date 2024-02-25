from wpilib import XboxController
from wpimath import applyDeadband
from utils.faults import Fault
from utils.signalLogging import log
from debugMaster.debug import Debug
class OperatorInterface:
    """Class to gather input from the driver of the robot"""

    def __init__(self):
        self.dbg = Debug()

        ctrlIdx = 1
        self.ctrl = XboxController(ctrlIdx)

        self.connectedFault = Fault(f"Operator XBox Controller ({ctrlIdx}) Unplugged")

        self.intakeVelocityFactor = 0.0
        self.shooterVelocityFactor = 0.0



    def update(self):
        """Main update - call this once every 20ms"""

        if self.ctrl.isConnected():
            # Only attempt to read from the joystick if it's plugged in

            # pylint: disable=R0801
            # Convert from joystic sign/axis conventions to robot velocity conventions
            intakeRaw = -1.0 * self.ctrl.getLeftY()
            shooterRaw = -1.0 * self.ctrl.getRightY()

            # Apply deadband to make sure letting go of the joystick actually stops the bot
            self.intakeVelocityFactor= applyDeadband(intakeRaw, 0.05)
            self.shooterVelocityFactor = applyDeadband(shooterRaw, 0.05)

            self.dbg.print("hi", f"oi:{self.intakeVelocityFactor=} {self.shooterVelocityFactor}")

            self.connectedFault.setNoFault()
        else:
            # If the joystick is unplugged, pick safe-state commands and raise a fault
            self.intakeVelocityFactor = 0.0
            self.shooterVelocityFactor = 0.0

        log("OI connected", self.ctrl.isConnected(), "bool")
