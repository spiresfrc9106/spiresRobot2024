from wpimath.system.plant import DCMotor
from utils.singleton import Singleton
from utils.units import RPM2RadPerSec
from wrappers.wrapperedSparkMax import WrapperedSparkMax

CLIMB_REVS_PER_INCH = 18.92 / 7.84
# This is some back of the napkin math to ensure
# that it takes no more than 1.5s to zero out.
# I have low confidence that it is correct :/
ZERO_OUT_RAD_PER_SEC = RPM2RadPerSec(8 * 60 * CLIMB_REVS_PER_INCH)

CLIMB_SPEED_FUDGE_FACTOR = 0.95
MAX_CLIMB_SPEED_RAD_PER_SEC = DCMotor.NEO(1).freeSpeed * CLIMB_SPEED_FUDGE_FACTOR

class ClimberControl(metaclass=Singleton):
    def __init__(self):
        # For initial tests, it might be easiest to set this to "yes"
        # And use joysticks to ensure other factors are correct
        # Then test out the zeroing
        self.hasZeroed = "no"

        # TODO: this spark max can id should be moved to a constants file
        self.motorLeft = WrapperedSparkMax(16, "_climberLeft", brakeMode=True, curLimitA=5)
        self.motorRight = WrapperedSparkMax(14, "_climberRight", brakeMode=True, curLimitA=5)
        self.motorLeft.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motorRight.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

        self.climbCmd = 0.0

    def update(self):
        if self.hasZeroed == "no":
            self.motorLeft.setVelCmd(ZERO_OUT_RAD_PER_SEC)
            self.motorRight.setVelCmd(ZERO_OUT_RAD_PER_SEC)
            self.hasZeroed = "zeroing"
        elif self.hasZeroed == "zeroing":
            if self.motorLeft.getMotorVelocityRadPerSec() < ZERO_OUT_RAD_PER_SEC * 0.05:
                self.motorLeft.setVoltage(0.0)
                self.motorRight.setVoltage(0.0)
                self.hasZeroed = "yes"
            else:
                self.motorLeft.setVelCmd(ZERO_OUT_RAD_PER_SEC)
                self.motorRight.setVelCmd(ZERO_OUT_RAD_PER_SEC)
        else:
            if self.climbCmd > 0.0:
                self.motorLeft.setVelCmd(MAX_CLIMB_SPEED_RAD_PER_SEC * self.climbCmd)
                self.motorRight.setVelCmd(MAX_CLIMB_SPEED_RAD_PER_SEC * self.climbCmd)
            else:
                self.motorLeft.setVoltage(0.0)
                self.motorRight.setVoltage(0.0)

    def setClimbCmd(self, cmd):
        self.climbCmd = cmd

    def resetHasZeroed(self):
        self.hasZeroed = "no"
