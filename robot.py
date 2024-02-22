import sys
import gc
import wpilib
from Autonomous.modes.driveOut import DriveOut
from robotConfig import webserverConstructorOrNone
from robotConfig import dashboardOrNone
from humanInterface.driverInterface import DriverInterface
from humanInterface.ledControl import LEDControl
from drivetrain.drivetrainControl import DrivetrainControl
# from drivetrain.drivetrainTrajectoryControl import DrivetrainTrajectoryControl
from utils.segmentTimeTracker import SegmentTimeTracker
from utils.signalLogging import SignalWrangler
from utils.calibration import CalibrationWrangler
from utils.faults import FaultWrangler
from utils.crashLogger import CrashLogger
from utils.rioMonitor import RIOMonitor
from utils.rioMonitor import DiskStats, RUN_PERIODIC_LOOP
from utils.singleton import destroyAllSingletonInstances
from AutoSequencerV2.autoSequencer import AutoSequencer
# from AutoSequencerV2.teleopConditions import TeleConditions
# from pieceMaster.gamePieceCtrl import GamePieceCtrl
from debugMaster.debug import Debug
from noteMaster.noteHandler import NoteHandler

class MyRobot(wpilib.TimedRobot):
    #########################################################
    ## Common init/update for all modes
    def robotInit(self):
        # Since we're defining a bunch of new things here, tell pylint
        # to ignore these instantiations in a method.
        # pylint: disable=attribute-defined-outside-init
        remoteRIODebugSupport()

        self.crashLogger = CrashLogger()
        wpilib.LiveWindow.disableAllTelemetry()

        self.stt = SegmentTimeTracker()
        # self.stt.doOptionalPerhapsMarks = True # Uncomment this line to turn on optional stt perhapsMark methods
        # self.stt.longLoopThresh = 0.020 # Uncomment this line adjust the stt logging time threshold in seconds
        #                                                                        1         2         3
        #                                                               12345678901234567890123456789012345
        self.markStartCrashName = self.stt.makePaddedMarkName("start-crashLogger")
        self.markCrashName = self.stt.makePaddedMarkName("crashLogger")
        self.markResetGyroName = self.stt.makePaddedMarkName("driveTrain.resetGyro")
        self.markDriveTrainName = self.stt.makePaddedMarkName("driveTrain.update")
        self.markSignalWranglerName = self.stt.makePaddedMarkName("SignalWrangler().publishPeriodic")
        self.markCalibrationWranglerName = self.stt.makePaddedMarkName("CalibrationWrangler().update")
        self.markFautWranglerName = self.stt.makePaddedMarkName("FaultWrangler().update()")
        self.webserver = webserverConstructorOrNone()

        self.driveTrain = DrivetrainControl()
        # self.trajectoryCtrl = DrivetrainTrajectoryControl()

        self.dInt = DriverInterface()

        self.ledCtrl = LEDControl()

        self.autoSequencer = AutoSequencer()
        self.autoSequencer.addMode(DriveOut())
        # self.autoSequencer.addMode(DrivePathCircle())

        self.dashboard = dashboardOrNone()

        # self.caliVelX = 0.0
        # self.caliVelY = 0.0
        # self.caliVelT = 0.0

        self.diskStats = DiskStats()
        self.diskStats.update()
        # self.rioMonitor = None
        self.rioMonitor = RIOMonitor(
            runStyle=RUN_PERIODIC_LOOP,
            enableDiskUpdates=False
        )

        print(f"before:0:{len(gc.get_objects(generation=0))}")
        print(f"before:1:{len(gc.get_objects(generation=1))}")
        print(f"before:2:{len(gc.get_objects(generation=2))}")
        gc.freeze()
        print(f"after:0:{len(gc.get_objects(generation=0))}")
        print(f"after:1:{len(gc.get_objects(generation=1))}")
        print(f"after:2:{len(gc.get_objects(generation=2))}")

        self.noteHandler = NoteHandler()
        #self.teleConditions = TeleConditions()
        #self.pieceCtrl = GamePieceCtrl()

        self.dbg = Debug()
        self.dbg.toPrint.update({'velState': False})
        self.dbg.toPrint.update({'sparkUpdates': False})
        self.dbg.toPrint.update({'hi': False})
        self.dbg.toPrint.update({'test': False})
        self.dbg.toPrint.update({'note': True})
        self.dbg.toPrint.update({'error': True})

        # Uncomment this and simulate to update the code
        # dependencies graph
        # from codeStructureReportGen import reportGen
        # reportGen.generate(self)


    def robotPeriodic(self):
        gc.disable()
        self.stt.start()

        self.stt.perhapsMark(self.markStartCrashName)
        self.crashLogger.update()
        self.stt.perhapsMark(self.markCrashName)

        if self.dInt.getGyroResetCmd():
            self.driveTrain.resetGyro()
        self.stt.perhapsMark(self.markResetGyroName)

        self.driveTrain.update()
        self.stt.perhapsMark(self.markDriveTrainName)
        self.ledCtrl.update()

        self.noteHandler.update()

        SignalWrangler().publishPeriodic()
        self.stt.perhapsMark(self.markSignalWranglerName)
        CalibrationWrangler().update()
        self.stt.perhapsMark(self.markCalibrationWranglerName)

        FaultWrangler().update()
        self.stt.perhapsMark(self.markFautWranglerName)
        if self.rioMonitor is not None:
            self.rioMonitor.updateFromPerioidLoop()
        self.stt.mark("rioMonitor.updateFromPerioidLoop()_")
        # print(f"before:{gc.get_stats()}")
        gc.enable()
        # gc.collect(generation=0)
        # self.stt.mark("gc.collect(0)______________________")
        # gc.collect(generation=1)
        # self.stt.mark("gc.collect(1)______________________")
        # gc.collect()
        self.stt.mark("gc.collect()_______________________")
        gc.disable()
        # print(f"after:{gc.get_stats()}")
        # print(
        #    f"after:0:{len(gc.get_objects(generation=0)):5} "
        #    f"1:{len(gc.get_objects(generation=1)):5} "
        #    f"2:{len(gc.get_objects(generation=2)):5}"
        # )

        self.stt.end()

    #########################################################
    ## Autonomous-Specific init and update
    def autonomousInit(self):
        # self.pieceCtrl.update(False)

        # Start up the autonomous sequencer
        self.autoSequencer.initiaize()

        # Use the autonomous rouines starting pose to init the pose estimator
        self.driveTrain.poseEst.setKnownPose(self.autoSequencer.getStartingPose())

        self.ledCtrl.setSpeakerAutoAlignActive(True)

    def autonomousPeriodic(self):
        self.autoSequencer.update()
        # self.pieceCtrl.update(False)

    def autonomousExit(self):
        self.autoSequencer.end()

    #########################################################
    ## Teleop-Specific init and update
    def teleopInit(self):
        # self.pieceCtrl.update(False)
        pass

    def teleopPeriodic(self):
        self.dbg.print("robot", "running game mode")
        self.dbg.print("hi", self.dInt.getVxCmd())
        # self.pieceCtrl.update(False)
        self.driveTrain.setCmdFieldRelative(self.dInt.getVxCmd(), self.dInt.getVyCmd(), self.dInt.getVtCmd())
        if True: #self.dInt.getIntakeActive():
            self.noteHandler.intakeCmd = True
        else:
            self.noteHandler.intakeCmd = False


    #########################################################
    ## Disabled-Specific init and update
    def disabledPeriodic(self):
        self.driveTrain.trajCtrl.updateCals()
        #self.teleConditions.updateMode()
        self.autoSequencer.updateMode()

    #########################################################
    ## Test-Specific init and update
    def testInit(self):
        self.dbg.print("robot", "test mode initiated")

    def testPeriodic(self):
        self.dbg.print("robot", "running test mode")
        # self.pieceCtrl.update(True)
        # self.driveTrain.setModuleState("FR", self.teleConditions.getWheelControl("FR", "velocity"),
        #                                self.teleConditions.getWheelControl("FR", "angle"))
        # self.driveTrain.setModuleState("FL", self.teleConditions.getWheelControl("FL", "velocity"),
        #                                self.teleConditions.getWheelControl("FL", "angle"))
        # self.driveTrain.setModuleState("BR", self.teleConditions.getWheelControl("BR", "velocity"),
        #                                self.teleConditions.getWheelControl("BR", "angle"))
        # self.driveTrain.setModuleState("BL", self.teleConditions.getWheelControl("BL", "velocity"),
        #                                self.teleConditions.getWheelControl("BL", "angle"))

    def testExit(self):
        # self.pieceCtrl.update(False)
        pass

    #########################################################
    ## Cleanup
    def endCompetition(self):
        if hasattr(self, 'rioMonitor') and self.rioMonitor is not None:
            self.rioMonitor.stopThreads()
        destroyAllSingletonInstances()
        super().endCompetition()


def remoteRIODebugSupport():
    if __debug__ and "run" in sys.argv:
        print("Starting Remote Debug Support....")
        try:
            import debugpy  # pylint: disable=import-outside-toplevel
        except ModuleNotFoundError:
            pass
        else:
            debugpy.listen(("0.0.0.0", 5678))
            debugpy.wait_for_client()