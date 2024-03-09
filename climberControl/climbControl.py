from wrappers.wrapperedSparkMax import WrapperedSparkMax

class ClimberControl:
  # TODO: this implementation is unsafe because there is no
  #       shutoff or control other than input
  # TODO: this implementation assumes that the entire climber
  #       is controlled by a single spark max
    def __init__(self):
        # TODO: determine the actual spark max can id
        # TODO: this spark max can id should be moved to a constants file
        self.motor = WrapperedSparkMax(16, "_climber", curLimitA=15)
        self.cmdSpd = 0

    def setClimberSpeed(self, inputSpeedRPS):
        """Set climber speed to inputSpeed with a unit of rotations per second"""
        self.cmdSpd = inputSpeedRPS

    def update(self):
        self.motor.setVelRPS(self.cmdSpd)