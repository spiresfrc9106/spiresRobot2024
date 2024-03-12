
import timeit
import collections
import time
import statistics

class CollectedTimeRec():
    __slots__ = 'startedWallS', 'startCpuS', 'durationS', 'cpuS'
    startedWallS: float
    startCpuS: float
    durationS: float
    cpuS: float

    def __init__(self, startedWallS:float, startCpuS:float, durationS:float=None, cpuS:float=None):
        self.startedWallS = startedWallS
        self.startCpuS = startCpuS
        self.durationS = durationS
        self.cpuS = cpuS

# pylint: disable=invalid-name
class WindowedStats():

    def __init__(self, pointsToKeep=100):
        self.q = collections.deque(maxlen=pointsToKeep)

    def append(self, item:CollectedTimeRec):
        self.q.append(item)

    def smoothWallTimeS(self):
        return statistics.mean(self.getWallTimes())

    def smoothCpuTimeS(self):
        return statistics.mean(self.getCpuTimes())

    def getWallTimes(self):
        return (x.durationS for x in self.q)

    def getCpuTimes(self):
        return (x.cpuS for x in self.q)

class GeometricMean():

    def __init__(self, pointsToKeep):
        self.pointToKeep = pointsToKeep
        self.points = 0
        self.alpha = 0.0
        self.value = 0.0
        self.min = float('+inf')
        self.max = float('-inf')

    def append(self, givenValue):
        if self.points < self.pointToKeep:
            self.points = self.points + 1
            self.alpha = 1.0 / self.points
        self.value = self.alpha * givenValue + (1.0-self.alpha) * self.value
        self.min = min(self.min, givenValue)
        self.max = max(self.max, givenValue)


class GeometricMeanStats():

    def __init__(self, pointsToKeep=100):
        self.smoothWallTime = GeometricMean(pointsToKeep=pointsToKeep)
        self.smoothCpuTime = GeometricMean(pointsToKeep=pointsToKeep)

    def append(self, item:CollectedTimeRec):
        self.smoothWallTime.append(item.durationS)
        self.smoothCpuTime.append(item.cpuS)

    def smoothWallTimeS(self):
        return self.smoothWallTime.value

    def smoothWallTimeMaxS(self):
        return self.smoothWallTime.max

    def smoothWallTimeMinS(self):
        return self.smoothCpuTime.min

    def smoothCpuTimeS(self):
        return self.smoothCpuTime.value

    def smoothCpuTimeMaxS(self):
        return self.smoothCpuTime.max

    def smoothCpuTimeMinS(self):
        return self.smoothCpuTime.min


class CollectWallAndCpuTimeData():
    __slots__ = 'name', 'listFilter'

    def __init__(self, name:str, listFilter):
        self.name = " '" + name + "'" if name else ''
        self.listFilter = listFilter

    @classmethod
    def start(cls, startWallS, startCpuS):
        return CollectedTimeRec(
            startedWallS=startWallS,
            startCpuS=startCpuS
        )

    def finish(self, timeRec:CollectedTimeRec, finishWallS, finishCpuS):
        durationS = (finishWallS - timeRec.startedWallS)
        timeRec.durationS = durationS
        timeRec.cpuS = float(finishCpuS - timeRec.startCpuS)
        self.listFilter.append(timeRec)

    @classmethod
    def enter(cls):
        return cls.start(
            startWallS=timeit.default_timer(),
            startCpuS=time.process_time()
        )

    def exit(self, timeRec:CollectedTimeRec):
        self.finish(
            timeRec=timeRec,
            finishWallS=timeit.default_timer(),
            finishCpuS=time.process_time()
        )


# See: https://stackoverflow.com/questions/14452145/how-to-measure-time-taken-between-lines-of-code-in-python
# See: https://stackoverflow.com/questions/15176619/timing-the-cpu-time-of-a-python-program
class CodeTimer:
    __slots__ = 'collector', 'timeRec'
    collector: CollectWallAndCpuTimeData

    def __init__(self, collector:CollectWallAndCpuTimeData):
        self.collector = collector
        self.timeRec = None

    def __enter__(self):
        if self.collector is not None:
            self.timeRec = self.collector.enter()

    def __exit__(self, exc_type, exc_value, traceback): #pylint: disable=invalid-name
        if self.collector is not None:
            self.collector.exit(self.timeRec)
