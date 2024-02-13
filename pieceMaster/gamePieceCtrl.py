from utils.calibration import Calibration
from utils import constants, faults
from utils.units import RPM2RadPerSec, m2in
from wrappers.wrapperedSparkMax import WrapperedSparkMax

class GamePieceCtrl:
    def __init__(self):

        # self.INTAKE_L1_CANID = 10
        # self.INTAKE_L2_CANID = 17
        # self.INTAKE_L3_CANID = 18

        # self.TRANSFER_L1_CANID = 11
        self.TRANSFER_L2_CANID = 12

        # self.SHOOTER_L1_CANID = 13
        # self.SHOOTER_L2_CANID = 14
        # self.SHOOTER_R1_CANID = 15
        # self.SHOOTER_R2_CANID = 16

        # Intake Motor

        # # intakeL1
        # self.intakeL1 = WrapperedSparkMax(self.INTAKE_L1_CANID, "IntakeL1")
        # self.intakeL1.setPID(0.00005, 0, 0)
        # self.intakeL1.setVoltage(12)
        # #self.intakeL1.setInverted(True)
        # # intakeL2
        # self.intakeL2 = WrapperedSparkMax(self.INTAKE_L2_CANID, "IntakeL2")
        # self.intakeL2.setPID(0.00005, 0, 0)
        # self.intakeL2.setVoltage(12)
        # #self.intakeL2.setInverted(True)
        # # intakeL3
        # self.intakeL3 = WrapperedSparkMax(self.INTAKE_L3_CANID, "IntakeL3")
        # self.intakeL3.setPID(0.00005, 0, 0)
        # self.intakeL3.setVoltage(12)
        ##self.intakeL3.setInverted(True)
        #
        # Transfer Motors

        # # transferL1
        # self.transferL1 = WrapperedSparkMax(self.TRANSFER_L1_CANID, "TransferL1")
        # self.transferL1.setPID(0.0025, 0, 0)
        # self.transferL1.setVoltage(0.0)
        # #self.transferL1.setInverted(False)


        # transferL2
        self.transferL2 = WrapperedSparkMax(self.TRANSFER_L2_CANID, "TransferL2")
        self.transferL2.setPID(0.0026, 0, 0)
        #self.transferL2.setInverted(False)


        # Shooter Motors

        # # shooterL1
        # self.shooterL1 = WrapperedSparkMax(self.SHOOTER_L1_CANID, "ShooterL1")
        # self.shooterL1.setPID(0.00005, 0, 0)
        # self.shooterL1.setVoltage(12)
        # #self.shooterL1.setInverted(False)
        # # shooterR1
        # self.shooterR1 = WrapperedSparkMax(self.SHOOTER_R1_CANID, "ShooterR1")
        # self.shooterR1.setPID(0.00005, 0, 0)
        # self.shooterR1.setVoltage(12)
        # #self.shooterR1.setInverted(True)
        # # shooterL2
        # self.shooterL2 = WrapperedSparkMax(self.SHOOTER_L2_CANID, "ShooterL2")
        # self.shooterL2.setPID(0.00005, 0, 0)
        # self.shooterL2.setVoltage(12)
        # #self.shooterL2.setInverted(False)
        # # shooterR2
        # self.shooterR2 = WrapperedSparkMax(self.SHOOTER_R2_CANID, "ShooterR2")
        # self.shooterR2.setPID(0.00005, 0, 0)
        # self.shooterR2.setVoltage(12)
        # #self.shooterR2.setInverted(True)

        # Shooter Calibrations (PID Controller)
        #self.shooterkFCal = Calibration("ShooterkF", 0.00255, "V/RPM")
        #self.shooterkPCal = Calibration("ShooterkP", 0)

        self.intakeVelCal = Calibration("Wheel Intake Velocity", 0.0, "RPM")
        self.transferVelCal = Calibration("Wheel Transfer Velocity", 0.0, "RPM")
        self.shooterVelCal = Calibration("Wheel Shooter Velocity", 0.0, "RPM")

        self.intakeVel = 0.0
        self.transferVel = 0.0
        self.shooterVel = 0.0

    def activeIntake(self, desVel):
        temp = 2
        # self.intakeL1.setVelCmd(RPM2RadPerSec(desVel))
        # self.intakeL2.setVelCmd(RPM2RadPerSec(desVel))
        # self.intakeL3.setVelCmd(RPM2RadPerSec(desVel))

    def activeTransfer(self, desVel):
        if abs(desVel)>0:
            self.transferL2.setVelCmd(RPM2RadPerSec(desVel))
        else:
            self.transferL2.setVoltage(0.0)
        #self.transferL1.setVelCmd(RPM2RadPerSec(desVel))

    def activeShooter(self, desVel):
        temp = 2
        # self.shooterR1.setVelCmd(RPM2RadPerSec(desVel))
        # self.shooterL1.setVelCmd(RPM2RadPerSec(desVel))
        # self.shooterR2.setVelCmd(RPM2RadPerSec(desVel))
        # self.shooterL2.setVelCmd(RPM2RadPerSec(desVel))

    def update(self):
        # self.intakeVel = self.intakeVelCal.get()
        temp = self.transferVelCal.get()
        # self.shooterVel = self.shooterVelCal.get()
        self.activeTransfer(temp)
        # self.activeIntake(self.intakeVel)
        # self.activeShooter(self.shooterVel)
