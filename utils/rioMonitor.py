import io
from threading import Thread
import time 
import subprocess
from wpilib import RobotController
from wpilib import RobotBase
import wpilib
from utils.faults import Fault
from utils.signalLogging import log
from utils.singleton import Singleton
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.timingHist import CodeTimer, CollectWallAndCpuTimeData, WindowedStats

class MemStats:
    __slots__ = 'log', 'fileStatsCollector', 'procStatsCollector'

    def __init__(self, givenLog):
        self.log = givenLog
        self.fileStatsCollector = CollectWallAndCpuTimeData(name="Mem File Stats", listFilter=WindowedStats())
        self.procStatsCollector = CollectWallAndCpuTimeData(name="Mem Proc Stats", listFilter=WindowedStats())
    def update(self):
        if (RobotBase.isReal()):
            memTotalStr = None
            memFreeStr = None

            with CodeTimer(collector=self.fileStatsCollector):
                # Read lines out of the special linux "meminfo" file
                with open("/proc/meminfo", 'r', encoding="utf-8") as file:
                    data = file.read()

            with CodeTimer(collector=self.procStatsCollector):
                lines = data.split('\n')
                for line in lines:
                    if line.startswith("MemTotal:"):
                        memTotalStr = line
                    elif (line.startswith("MemFree:")):
                        memFreeStr = line

                # If we found both lines, parse out the numbers we care about
                if (memTotalStr is not None and memFreeStr is not None):
                    memTotalParts = memTotalStr.split()
                    memFreeParts = memFreeStr.split()

                    try:
                        curTotalMem = float(memTotalParts[1])
                        curFreeMem = float(memFreeParts[1])
                    except ValueError:
                        return  # Skip this time if we couldn't parse out values

                    self.log("RIO Memory Usage", (1.0 - curFreeMem / curTotalMem) * 100.0, "pct")
            # self.log("RIO Memory Usage File Wall Time",
            #           self.fileStatsCollector.listFilter.q[-1].durationS*1000.0, "ms")
            # self.log("RIO Memory Usage File CPU Time",
            #           self.fileStatsCollector.listFilter.q[-1].cpuS*1000.0, "ms")
            # self.log("RIO Memory Usage Proc Wall Time",
            #           self.procStatsCollector.listFilter.q[-1].durationS*1000.0, "ms")
            # self.log("RIO Memory Usage Proc CPU Time",
            #           self.procStatsCollector.listFilter.q[-1].cpuS*1000.0, "ms")
            self.log("RIO Memory Usage Total CPU Time",
                     (self.procStatsCollector.listFilter.q[-1].cpuS +
                      self.fileStatsCollector.listFilter.q[-1].cpuS) * 1000.0,
                     "ms",
                     publishNt=False)

# pylint: disable=too-many-locals
class CpuStats:
    def __init__(self, givenLog):
        self.log = givenLog
        self.prevUserTime = 0
        self.prevNicedTime = 0
        self.prevSystemTime = 0
        self.prevIdleTime = 0
        self.fileStatsCollector = CollectWallAndCpuTimeData(name="Cpu File Stats", listFilter=WindowedStats())
        self.procStatsCollector = CollectWallAndCpuTimeData(name="Cpu Proc Stats", listFilter=WindowedStats())
    def update(self):
        if (RobotBase.isReal()):
            curUserTime = 0
            curNicedTime = 0
            curSystemTime = 0
            curIdleTime = 0
            loadLine = None

            with CodeTimer(collector=self.fileStatsCollector):
                # The /proc/stat file contains running totals
                # of how long the CPU spent doing different things
                with open("/proc/stat", 'r', encoding="utf-8") as file:
                    data = file.read()

            with CodeTimer(collector=self.procStatsCollector):
                lines = data.split('\n')
                for line in lines:
                    if line.startswith("cpu "):
                        loadLine = line
                        break

                if (loadLine is not None):
                    # Parse out the running totals
                    parts = loadLine.split(" ")
                    parts = [i for i in parts if i]  # Filter out empty strings
                    try:
                        curUserTime = float(parts[1])
                        curNicedTime = float(parts[2])
                        curSystemTime = float(parts[3])
                        curIdleTime = float(parts[4])
                    except ValueError:
                        return  # Skip this time if we couldn't parse out values

                    # Calculate how much those totals changed from last time
                    deltaUserTime = curUserTime - self.prevUserTime
                    deltaNicedTime = curNicedTime - self.prevNicedTime
                    deltaSystemTime = curSystemTime - self.prevSystemTime
                    deltaIdleTime = curIdleTime - self.prevIdleTime

                    # Add up how much time the CPU spent doing something useful
                    totalInUseTime = (deltaUserTime + deltaNicedTime + deltaSystemTime)

                    # Add up how much total time (in-use and idle together)
                    totalTime = totalInUseTime + deltaIdleTime

                    # Calculate and log  the Load Percent as percentage of
                    # total time that we were not idle
                    self.log("RIO CPU Load", totalInUseTime / totalTime * 100.0, "pct")

                    # Remember current stats for next time
                    self.prevUserTime = curUserTime
                    self.prevNicedTime = curNicedTime
                    self.prevSystemTime = curSystemTime
                    self.prevIdleTime = curIdleTime
            self.log("RIO CPU File Wall Time", self.fileStatsCollector.listFilter.q[-1].durationS*1000.0, "ms",
                     publishNt=False
            )
            self.log("RIO CPU File CPU Time", self.fileStatsCollector.listFilter.q[-1].cpuS*1000.0, "ms",
                     publishNt=False
            )
            self.log("RIO CPU Proc Wall Time", self.procStatsCollector.listFilter.q[-1].durationS*1000.0, "ms",
                     publishNt=False
            )
            self.log("RIO CPU Proc CPU Time", self.procStatsCollector.listFilter.q[-1].cpuS*1000.0, "ms",
                     publishNt=False
            )
            self.log("RIO CPU Total CPU Time",
                     (self.fileStatsCollector.listFilter.q[-1].cpuS +
                      self.procStatsCollector.listFilter.q[-1].cpuS) * 1000.0,
                     "ms",
                     publishNt=False)


class DiskStats:
    def __init__(self, givenLog=None, config=None):
        if givenLog is None:
            givenLog = log
        self.log = givenLog
        # TODO xyzzy mike was expanding this area
        if config is None:
            config = [
                {'mountPoint': '/', 'logLabel': 'RIO SD Card Disk Usage'},
                {'mountPoint': '/media', 'logLabel': 'RIO SD Card Disk Usage'},
            ]
        self.fileStatsCollector = CollectWallAndCpuTimeData(name="Disk File Stats", listFilter=WindowedStats())
        self.sdProcStatsCollector = CollectWallAndCpuTimeData(name="SD Disk Proc Stats", listFilter=WindowedStats())
        self.usbProcStatsCollector = CollectWallAndCpuTimeData(name="USB Disk Proc Stats", listFilter=WindowedStats())

    def update(self):
        if (RobotBase.isReal()):
            # Use the built-in `df` command to get info about disk usage
            with CodeTimer(collector=self.fileStatsCollector):
                result = subprocess.Popen( # pylint: disable=consider-using-with
                    (
                        "df",
                        #"/",
                        #"/media"
                    ), stdout=subprocess.PIPE)


            if (result.stdout is not None):
                with CodeTimer(collector=self.sdProcStatsCollector):
                    for line in io.TextIOWrapper(result.stdout,
                                                 encoding="utf-8"):  # abstract-class-instantiated: ignore
                        lineParts = line.split()
                        lineParts = [i for i in lineParts if i]
                        try:
                            mountDir = str(lineParts[5])
                            usedBytes = int(lineParts[2])
                            availBytes = int(lineParts[3])
                        except ValueError:
                            continue  # Skip this line if we couldn't parse values

                        pctUsed = usedBytes / float(usedBytes + availBytes) * 100.0
                        print(f"mountDir=>{mountDir}<=")
                        if (mountDir == "/"):
                            self.log("RIO SD Card Disk Usage", pctUsed, "pct")
                        elif (mountDir.startswith("/media")):
                            mountDir = mountDir.replace("/", "\\")
                            self.log(f"RIO USB {mountDir} Disk Usage", pctUsed, "pct")
                #self.log("RIO Disk File Wall Time", self.fileStatsCollector.listFilter.q[-1].durationS * 1000.0, "ms")
                #self.log("RIO Disk File CPU Time", self.fileStatsCollector.listFilter.q[-1].cpuS * 1000.0, "ms")
                #self.log("RIO Disk Proc Wall Time",
                # self.sdProcStatsCollector.listFilter.q[-1].durationS * 1000.0, "ms")
                #self.log("RIO Disk Proc CPU Time", self.sdProcStatsCollector.listFilter.q[-1].cpuS * 1000.0, "ms")
                #self.log("RIODiskTotalCPUTime",
                #         (self.fileStatsCollector.listFilter.q[-1].cpuS +
                #         self.sdProcStatsCollector.listFilter.q[-1].cpuS) * 1000.0, "ms")
                self.log("RIODisk1Wall2CPUTime",
                         (self.fileStatsCollector.listFilter.q[-1].durationS +
                          self.sdProcStatsCollector.listFilter.q[-1].cpuS) * 1000.0,
                         "ms",
                         publishNt=False
                         )






RUN_THREAD = 'runThreaded'
RUN_PERIODIC_LOOP = 'runPeriodicLoop'

# Records faults and runtime metrics for the roboRIO
class RIOMonitor(metaclass=Singleton):
    def __init__(self, runStyle=RUN_THREAD, enableDiskUpdates=True):

        self.railFault5v = Fault("RIO 5V (DIO) Rail Faulted")
        self.railFault3p3v = Fault("RIO 3.3V Rail Faulted")
        self.railFault6v = Fault("RIO 6V (PWM) Rail Faulted")

        self.runCmd = True
        self.runStyle = runStyle
        self.enableDiskUpdates = enableDiskUpdates
        
        nowS = wpilib.Timer.getFPGATimestamp()
        self.timeWhenLastFastUpdateS = nowS
        self.timeWhenLastSlowUpdateS = nowS

        self.stt = SegmentTimeTracker()

        if self.runStyle in (RUN_THREAD, RUN_PERIODIC_LOOP):
            self.memStats = MemStats(givenLog=log)
            self.cpuStats = CpuStats(givenLog=log)
            #self.diskStats = DiskStats(log=log)

        if self.runStyle==RUN_THREAD:
            self.thread1 = Thread(target=self._updateFast,daemon=True)
            self.thread2 = Thread(target=self._updateSlow,daemon=True)
            self.thread1.start()
            self.thread2.start()
            self.slowRioMonitorProcess = None


    def stopThreads(self):
        self.runCmd = False
        if self.runStyle==RUN_THREAD:
            self.thread1.join()
            self.thread2.join()
        
    # Things that should be recorded fairly quickly
    def _doFastUpdates(self):
        self._updateVoltages()
        self.timeWhenLastFastUpdateS = wpilib.Timer.getFPGATimestamp()

    def _updateFast(self):
        while(self.runCmd):
            self._doFastUpdates()
            time.sleep(0.02)

    # Things that don't have to be updated as fast
    def _doSlowUpdates(self):
        #              12345678901234567890123456789012345
        self.stt.mark("start-slow-updates_________________")
        if self.runStyle in (RUN_THREAD, RUN_PERIODIC_LOOP):
            self.memStats.update()
            self.cpuStats.update()
            #self.diskStats.update()

        self._updateCANStats()
        #              12345678901234567890123456789012345
        self.stt.mark("_updateCANStats____________________")
        self.timeWhenLastSlowUpdateS = wpilib.Timer.getFPGATimestamp()

    def _updateSlow(self):
        while(self.runCmd):
            self._doSlowUpdates()
            time.sleep(1.0)
            
    def updateFromPerioidLoop(self):
        if self.runStyle == RUN_PERIODIC_LOOP:

            nowS = wpilib.Timer.getFPGATimestamp()
            if nowS - self.timeWhenLastFastUpdateS > 0.015:
                self._doFastUpdates()

            if nowS - self.timeWhenLastSlowUpdateS > 0.995:
                self._doSlowUpdates()



    def _updateCANStats(self):
        status = RobotController.getCANStatus()
        log("RIO CAN Bus Usage", status.percentBusUtilization, "pct")
        log("RIO CAN Bus Err Count", status.txFullCount + 
                                     status.receiveErrorCount + 
                                     status.transmitErrorCount, 
                                     "count")
    def _updateVoltages(self):
        log("RIO Supply Voltage", RobotController.getInputVoltage(), "V")
        if(not RobotController.isBrownedOut()):
            self.railFault3p3v.set(not RobotController.getEnabled3V3())
            self.railFault5v.set(not RobotController.getEnabled5V())
            self.railFault6v.set(not RobotController.getEnabled6V())
