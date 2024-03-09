from wpimath.system.plant import DCMotor
from wrappers.wrapperedSparkMax import WrapperedSparkMax
from utils.singleton import Singleton
from utils.units import RPM2RadPerSec

CLIMB_REVS_PER_INCH = 18.92 / 7.84

# rate * time = distance
# rate = distance / time
# vel_in_per_s = 12 in / 1.5 s
# 1.5s was chosen arbitrarily, could be adjusted

ZERO_OUT_VEL_INCH_PER_S = 12 / 1.5

ZERO_OUT_REV_PER_S = ZERO_OUT_VEL_INCH_PER_S * CLIMB_REVS_PER_INCH
ZERO_OUT_RPM = ZERO_OUT_REV_PER_S * 60
ZERO_OUT_RAD_PER_SEC = RPM2RadPerSec(ZERO_OUT_RPM)

CLIMB_SPEED_FUDGE_FACTOR = 5.0 # TODO: this should be between 0 and 1
MAX_CLIMB_SPEED_RAD_PER_SEC = DCMotor.NEO(1).freeSpeed * CLIMB_SPEED_FUDGE_FACTOR


class ClimberMotorControl():
    def __init__(self, name: str, inverted: bool, canID: int):
        self.name = name
        # For initial tests, it might be easiest to set this to "yes"
        # And use joysticks to ensure other factors are correct
        # Then test out the zeroing
        self.hasZeroed = "yes"

        # TODO: this spark max can id should be moved to a constants file
        self.motor = WrapperedSparkMax(canID, f"_climber{name}", brakeMode=True, curLimitA=5)
        self.motor.setInverted(inverted)
        self.motor.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
        self.count = 0
        self.velCmdFraction = 0

    def changeHasZeroed(self, newState):
        if self.hasZeroed != newState:
            print(f"newStateClimberState={self.name}:{newState}")
            self.hasZeroed = newState

    def update(self):
        if self.hasZeroed == "no":
            self.changeHasZeroed("enteringZeroing")
        elif self.hasZeroed == "enteringZeroing":
            self.motor.setVelCmd(-ZERO_OUT_RAD_PER_SEC)
            self.changeHasZeroed("zeroing")
            self.count = 0
            self.velCmdFraction = 0.0
        elif self.hasZeroed == "zeroing":
            if self.motor.getMotorVelocityRadPerSec() > -ZERO_OUT_RAD_PER_SEC * 0.05:
                if self.count >= 25:
                    self.count = 0
                    self.motor.setVoltage(0.0)
                    self.changeHasZeroed("yes")
                else:
                    self.count += 1
        elif self.hasZeroed == "yes":
            finalVelCmdFraction = self.velCmdFraction
            if abs(finalVelCmdFraction) <= 0.01:
                finalVelCmdFraction = 0.0
            self.motor.setVelCmd(finalVelCmdFraction * MAX_CLIMB_SPEED_RAD_PER_SEC)
            if abs(finalVelCmdFraction) <= 0.01:
                self.motor.setVoltage(0.0)
        else:
            # todo we shouldn't get here.
            self.motor.setVoltage(0.0)
            self.velCmdFraction = 0
        self.motor.getVelRPS()
        self.motor.getAppliedOutput()

    def setVelCmdPercentage(self, velCmdPercentage):
        self.velCmdFraction = velCmdPercentage

    def resetHasZeroed(self):
        self.hasZeroed = "no"


class ClimberControl(metaclass=Singleton):
    def __init__(self):
        # TODO: this spark max can id should be moved to a constants file
        self.motorLeft = ClimberMotorControl(name='left', inverted=False, canID=16)
        self.motorRight = ClimberMotorControl(name='right', inverted=False, canID=14)
        self.climbCmdPercentage = 0.0

    def update(self):
        self.motorLeft.setVelCmdPercentage(self.climbCmdPercentage)
        self.motorRight.setVelCmdPercentage(self.climbCmdPercentage)
        self.motorLeft.update()
        self.motorRight.update()

    def setClimbCmdPercentage(self, cmd):
        self.climbCmdPercentage = cmd

    def resetHasZeroed(self):
        self.motorLeft.resetHasZeroed()
        self.motorRight.resetHasZeroed()
