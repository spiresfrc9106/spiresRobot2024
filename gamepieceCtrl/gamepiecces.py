from utils.calibration import Calibration
from utils import constants, faults
from utils.units import RPM2RadPerSec, m2in
from wrappers.wrapperedSparkMax import WrapperedSparkMax

class GamePieceCtrl:
    def __init__(self):

        self.INTAKE_L1_CANID = 10
        self.TRANSFER_L1_CANID = 11
        self.TRANSFER_L2_CANID = 12

        self.SHOOTER_L1_CANID = 13
        self.SHOOTER_L2_CANID = 14

        self.SHOOTER_R1_CANID = 15
        self.SHOOTER_R2_CANID = 16

        # Shooter Motors
        self.shooterL1 = WrapperedSparkMax(
            self.SHOOTER_L1_CANID, "ShooterL1"
        )
        self.shooterR1 = WrapperedSparkMax(
            self.SHOOTER_R1_CANID, "ShooterR1"
        )
        self.shooterL2 = WrapperedSparkMax(
            self.SHOOTER_L2_CANID, "ShooterL2"
        )
        self.shooterR2 = WrapperedSparkMax(
            self.SHOOTER_R2_CANID, "ShooterR2"
        )

        # Transfer Motors
        self.transferL1 = WrapperedSparkMax(self.TRANSFER_L1_CANID, "TransferL1")
        self.transferL2 = WrapperedSparkMax(self.TRANSFER_L2_CANID, "TransferL2")

        # Intake Motor
        self.intakeL1 = WrapperedSparkMax(self.INTAKE_L1_CANID, "IntakeL1")

        # Shooter Calibrations (PID Controller)
        #self.shooterkFCal = Calibration("ShooterkF", 0.00255, "V/RPM")
        #self.shooterkPCal = Calibration("ShooterkP", 0)

        self.intakeL1.setInverted(True)

        self.transferL1.setInverted(False)
        self.transferL2.setInverted(False)

        self.shooterL1.setInverted(False)
        self.shooterL2.setInverted(False)
        # The ones below are inverted
        self.shooterR1.setInverted(True)
        self.shooterR2.setInverted(True)

        self.intakeVelCal = Calibration("Wheel Intake Velocity", 0.0, "RPM")
        self.transferVelCal = Calibration("Wheel Transfer Velocity", 0.0, "RPM")
        self.shooterVelCal = Calibration("Wheel Shooter Velocity", 0.0, "RPM")

        self.intakeVel = 0.0
        self.transferVel = 0.0
        self.shooterVel = 0.0

    def activeIntake(self, desVel):
        self.intakeL1.setVelCmd(1.0)
        self.intakeL1.setVoltage(-1*RPM2RadPerSec(desVel))

    def activeTransfer(self, desVal):
        self.transferL1.setVelCmd(RPM2RadPerSec(desVal))
        self.transferL2.setVelCmd(RPM2RadPerSec(desVal))

    def activeShooter(self, desVel):
        self.shooterR1.setVelCmd(RPM2RadPerSec(desVel))
        self.shooterL1.setVelCmd(RPM2RadPerSec(desVel))
        self.shooterR2.setVelCmd(RPM2RadPerSec(desVel))
        self.shooterL2.setVelCmd(RPM2RadPerSec(desVel))

    def update(self):
        self.intakeVel = self.intakeVelCal.get()
        self.transferVel = self.transferVelCal.get()
        self.shooterVel = self.shooterVelCal.get()
        self.activeIntake(self.intakeVel)
        self.activeTransfer(self.transferVel)
        self.activeShooter(self.shooterVel)
