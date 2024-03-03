from utils.singleton import Singleton
from utils.units import RPM2RadPerSec
from wrappers.wrapperedSparkMax import WrapperedSparkMax
from wpimath.system.plant import DCMotor

CLIMB_REVS_PER_INCH = 18.92 / 7.84
# This is some back of the napkin math to ensure
# that it takes no more than 1.5s to zero out.
# I have low confidence that it is correct :/

# rate * time = distance
# rate = distance / time
# vel_in_per_s = 12 in / 1.5 s

ZERO_OUT_VEL_INCH_PER_S = 12 / 1.5

ZERO_OUT_REV_PER_S = ZERO_OUT_VEL_INCH_PER_S * CLIMB_REVS_PER_INCH
ZERO_OUT_RPM = ZERO_OUT_REV_PER_S * 60
ZERO_OUT_RAD_PER_SEC = RPM2RadPerSec(ZERO_OUT_RPM)

CLIMB_SPEED_FUDGE_FACTOR = 0.03
MAX_CLIMB_SPEED_RAD_PER_SEC = DCMotor.NEO(1).freeSpeed * CLIMB_SPEED_FUDGE_FACTOR


class ClimberMotorControl():
    def __init__(self, name: str, inverted: bool, canID: int):
        self.hasZeroed = "yes"  # xyzzy

        # TODO: this spark max can id should be moved to a constants file
        self.motor = WrapperedSparkMax(canID, f"_climber{name}", brakeMode=True, curLimitA=5)
        self.motor.setInverted(inverted)
        self.motor.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.count = 0
        self.velCmdRadPerS = 0

        def update(self):
            if self.hasZeroed == "no":
                self.hasZeroed = "enteringZeroing"
            elif self.hasZeroed == "enteringZeroing":
                self.motor.setVelCmd(-ZERO_OUT_RAD_PER_SEC)
                self.hasZeroed = "zeroing"
                self.count = 0
                self.velCmdRadPerS = 0
            elif self.hasZeroed == "zeroing":
                if self.motor.getMotorVelocityRadPerSec() > -ZERO_OUT_RAD_PER_SEC * 0.05:
                    if self.count >= 25:
                        self.count = 0
                        self.motor.setVoltage(0.0)
                        self.hasZeroed = "yes"
                    else:
                        self.count += 1
            elif self.hasZeroed == "yes":
                self.motor.setVelCmd(self.velCmdRadPerS)
            else:
                self.motor.setVoltage(0.0)
                self.velCmdRadPerS = 0
                # todo we shouldn't get here.

        def setVelCmdRadPerS(self, velCmdRadPerS):
          self.velCmdRadPerS = velCmdRadPerS


class ClimberControl(metaclass=Singleton):
    def __init__(self):
        # For initial tests, it might be easiest to set this to "yes"
        # And use joysticks to ensure other factors are correct
        # Then test out the zeroing
        self.hasZeroed = "yes"  # xyzzy

        # TODO: this spark max can id should be moved to a constants file
        self.motorLeft = ClimberMotorControl(name='left', inverted=False, )

          WrapperedSparkMax(16, "_climberLeft", brakeMode=True, curLimitA=5)
        self.motorRight = WrapperedSparkMax(14, "_climberRight", brakeMode=True, curLimitA=5)
        self.motorLeft.setInverted(False)
        self.motorRight.setInverted(False)
        self.motorLeft.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.motorRight.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

        self.climbCmd = 0.0

    def update(self):
        pass

    def setClimbCmd(self, cmd):
        self.climbCmd = cmd

    def resetHasZeroed(self):
        self.hasZeroed = "no"
