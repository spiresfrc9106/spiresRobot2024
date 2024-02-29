from utils.singleton import Singleton
from utils.units import deg2Rad, in2m
from wrappers.wrapperedSparkMax import WrapperedSparkMax
from wpimath.system.plant import DCMotor


CLIMB_SPEED_FUDGE_FACTOR = 0.95
# radians / sec
MAX_CLIMB_SPEED_RPS = DCMotor.NEO(1).freeSpeed * CLIMB_SPEED_FUDGE_FACTOR

class ClimberControl(metaclass=Singleton):
    def __init__(self):
      self.hasZeroed = False

      # TODO: this spark max can id should be moved to a constants file
      self.motorLeft = WrapperedSparkMax(16, "_climberLeft", brakeMode=True, curLimitA=5)
      self.motorRight = WrapperedSparkMax(14, "_climberRight", brakeMode=True, curLimitA=5)
      self.motorLeft.setPID(kP=1.5e-4, kI=0.0, kD=0.0)
      self.motorRight.setPID(kP=1.5e-4, kI=0.0, kD=0.0)

      self.climbCmd = 0.0

    def update(self):
      if not self.hasZeroed:
        # TODO: zero out climber
        pass
      else:
        if self.climbCmd > 0.0:
          self.motorLeft.setVelCmd(MAX_CLIMB_SPEED_RPS * self.climbCmd)
          self.motorRight.setVelCmd(MAX_CLIMB_SPEED_RPS * self.climbCmd)
        else:
          self.motorLeft.setVoltage(0.0)
          self.motorRight.setVoltage(0.0)

    def setClimbCmd(self, cmd):
      self.climbCmd = cmd

    def resetHasZeroed(self):
      self.hasZeroed = False
