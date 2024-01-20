# pylint: disable-all
import statistics
from utils.timingHist import *


def test_timingHist_topLevel():
    dut = CollectWallAndCpuTimeData(name='testy', listFilter=WindowedStats())
    for i in range(5):
        wact = CollectedTimeRec(
            startedWallS= i,
            startCpuS= i+10,
            durationS=i+30,
            cpuS=i+20)
        dut.listFilter.append(wact)
    assert len(list(dut.listFilter.getCpuTimes())) == 5
    assert len(list(dut.listFilter.getWallTimes())) == 5
    assert statistics.mean(dut.listFilter.getCpuTimes()) == 22
    assert statistics.mean(dut.listFilter.getWallTimes()) == 32


def test_timingHist_nextLevel():
    dut = CollectWallAndCpuTimeData(name='testy', listFilter=WindowedStats())
    for i in range(5):
        timeRec = dut.start(
            startWallS=i*1.0,
            startCpuS=i+10.0
        )
        dut.finish(
            timeRec = timeRec,
            finishWallS=i*1.0+10.0,
            finishCpuS=i+11.0
        )
    assert len(list(dut.listFilter.getCpuTimes())) == 5
    assert len(list(dut.listFilter.getWallTimes())) == 5
    m = statistics.mean(dut.listFilter.getCpuTimes())
    assert m>0.9999
    assert m<1.0001
    m = statistics.mean(dut.listFilter.getWallTimes())
    assert m>9.999
    assert m<10.001


def test_timingHist_thirdLevel():
        collector = CollectWallAndCpuTimeData(name="testy", listFilter=WindowedStats())
        for i in range(10):
            with CodeTimer(collector=collector):
                s = sum(range(1, 1000+i))
            print(f"sum={s}")
        assert len(list(collector.listFilter.getCpuTimes())) == 10
        assert len(list(collector.listFilter.getWallTimes())) == 10
        m = statistics.mean(collector.listFilter.getCpuTimes())
        print(f"mean cpuS={m}")
        m = statistics.mean(collector.listFilter.getWallTimes())
        print(f"mean wallS={m}")

