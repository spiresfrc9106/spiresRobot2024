import wpilib

from utils.signalLogging import log
from utils.singleton import Singleton
from utils.timingHist import GeometricMean

# Utilties for tracking how long certain chunks of code take
# including logging overall loop execution time
class SegmentTimeTracker(metaclass=Singleton):
    def __init__(self):
        self.longLoopThresh = 0.030
        self.markNamePadLen = 35
        self.doOptionalPerhapsMarks = False
        self.minLoopsToEnableTracking = 10
        self.minLoopPeriodToEnableTracking = 0.015
        self.tracer = wpilib.Tracer()
        self.loopStartTime = wpilib.Timer.getFPGATimestamp()
        self.loopEndTime = wpilib.Timer.getFPGATimestamp()
        self.prevLoopStartTime = self.loopStartTime
        self.curPeriod = 0
        self.smoothLoopDurationMs = GeometricMean(pointsToKeep=500)
        self.curLoopExecDur = 0
        self.numOverRuns = 0
        self.numLoops = 0
        self.numLoopsMod = self.numLoops
        self.trackingEnabled = False

    def start(self):
        self.tracer.clearEpochs()
        self.prevLoopStartTime = self.loopStartTime
        self.loopStartTime = wpilib.Timer.getFPGATimestamp()
        self.curPeriod = self.loopStartTime - self.prevLoopStartTime
        log("LoopPeriod", self.curPeriod * 1000.0, "ms")
        if self.numLoops >= self.minLoopsToEnableTracking and self.curPeriod >= self.minLoopPeriodToEnableTracking:
            self.trackingEnabled = True

    def makePaddedMarkName(self, name):
        """
        A convience function to make all of the wpilib.Tracer() names the
        same length so that when the printEpochs() method lists the times
        for each epoch, they are column aligned so that one can more 
        quickly find the long epochs.
        """

        """
        An example:
        python -m netconsole 172.22.11.2
        [...snip...]
        [27.62] Warning at PrintEpochs: Warning:        poseEst.update_____________________: 0.001014s
        [27.62]         SignalWrangler().publishPeriodic___: 0.002510s
        [27.62]         markUpdateActualStateName.FL_______: 0.000128s
        [27.62]         markUpdateActualStateName.BR_______: 0.000172s
        [27.62]         CalibrationWrangler().update_______: 0.002518s
        [27.63]         optimizedDesiredState.BL___________: 0.000078s
        [27.63]         markUpdateActualStateName.FR_______: 0.000105s
        [27.63]         optimizedDesiredState.FL___________: 0.000104s
        [27.63]         FaultWrangler().update()___________: 0.000175s
        [27.63]         optimizedDesiredState.BR___________: 0.000078s
        [27.63]         optimizedDesiredState.FR___________: 0.000081s
        [27.63]         SendCommandsToModuleAndUpdate______: 0.000025s
        [27.63]         azmthEnc.update.BL_________________: 0.000095s
        [27.63]         driveTrain.update__________________: 0.000023s
        [27.63]         desModStates_______________________: 0.000093s
        [27.63]         start-crashLogger__________________: 0.000085s
        [27.63]         azmthEnc.update.FL_________________: 0.000121s
        [27.63]         updateTelemetry().BL_______________: 0.000145s
        [27.63]         desaturateWheelSpeeds______________: 0.000084s
        [27.63]         azmthEnc.update.BR_________________: 0.000090s
        [27.63]         updateTelemetry().FL_______________: 0.000161s
        [27.63]         azmthEnc.update.FR_________________: 0.000100s
        [27.63]         updateTelemetry().BR_______________: 0.000160s
        [27.63]         updateTelemetry().FR_______________: 0.000142s
        [27.63]         wheelMotor.setVelCmd.BL____________: 0.000131s
        [27.63]         wheelMotor.setVelCmd.FL____________: 0.000163s
        [27.63]         wheelMotor.setVelCmd.BR____________: 0.000128s
        [27.63]         azmthMotor.setVoltage.BL___________: 0.000110s
        [27.63]         gains.hasChanged___________________: 0.000037s
        [27.63]         wheelMotor.setVelCmd.FR____________: 0.000137s
        [27.63]         azmthMotor.setVoltage.FL___________: 0.000127s
        [27.63]         azmthMotor.setVoltage.BR___________: 0.000103s
        [27.63]         crashLogger________________________: 0.000034s
        [27.63]         driveTrain.resetGyro_______________: 0.000021s
        [27.63]         azmthMotor.setVoltage.FR___________: 0.000109s
        [27.63]         markUpdateActualStateName.BL_______: 0.000105s
        """
        if len(name)>self.markNamePadLen:
            name = name[:self.markNamePadLen]
        elif len(name)<self.markNamePadLen:
            name = name.ljust(self.markNamePadLen, '_')
        return name
        
    def mark(self, name):
        if self.trackingEnabled:
            self.tracer.addEpoch(name)

    def perhapsMark(self, name):
        if self.trackingEnabled and self.doOptionalPerhapsMarks:
            self.mark(name)

    def end(self):
        self.loopEndTime = wpilib.Timer.getFPGATimestamp()
        self.curLoopExecDur = self.loopEndTime - self.loopStartTime
        self.numLoops += 1
        self.numLoopsMod = (self.numLoopsMod + 1) % 50
        if self.trackingEnabled:
            loopDurationMs = self.curLoopExecDur * 1000.0
            if(self.curLoopExecDur > self.longLoopThresh):
                self.numOverRuns += 1
                self.tracer.printEpochs()
            self.smoothLoopDurationMs.append(loopDurationMs)
            log("LoopDuration", loopDurationMs, "ms")
            log("LoopOverRunCount", self.numOverRuns, "count")

        # Logging loopEndTime helps when aligning events in graphed plots with netconsole messages by time stamps.
        log("LoopEndTime", self.loopEndTime*1000.0, "ms")
        log("LoopCount", self.numLoops, "count")
        log("LoopCountMod", self.numLoopsMod, "count")
        if self.trackingEnabled:
            log("LoopDurationSmooth", self.smoothLoopDurationMs.value, "ms")
