from wpilib import PWMMotorController


class LEDControl():

    def __init__(self):
        # Put any one-time init code here
        self.speakerAutoAlignActive = False
        self.noteInIntake = False
        self._noteInIntakePrev = False
        self._noteInIntakeCounter = 0
        self.ctrl = PWMMotorController("LEDCtrl", 9)
        self._SAMPLE_TIME = 0.02 # pylint: disable=invalid-name

    def update(self):
        pwmVal = 0.0 # default = off

        if(self.noteInIntake and not self._noteInIntakePrev):
            self._noteInIntakeCounter = int(1.0 / self._SAMPLE_TIME) # Set LED's to blink for 1 second

        if(self.speakerAutoAlignActive):
            pwmVal = 0.5 # Blue Solid
        elif(self._noteInIntakeCounter > 0):
            pwmVal = -0.35# Green Blink
            self._noteInIntakeCounter -= 1

        self.ctrl.set(pwmVal)


        self._noteInIntakePrev = self.noteInIntake

        

    
    def setSpeakerAutoAlignActive(self, isActive):
        self.speakerAutoAlignActive = isActive

    def setNoteInIntake(self, hasNote):
        self.noteInIntake = hasNote
