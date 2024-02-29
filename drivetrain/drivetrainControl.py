from wpimath.kinematics import ChassisSpeeds
from wpimath.geometry import Pose2d, Rotation2d

from utils.singleton import Singleton
from utils.allianceTransformUtils import onRed
from utils.segmentTimeTracker import SegmentTimeTracker

from drivetrain.poseEstimation.drivetrainPoseEstimator import DrivetrainPoseEstimator
from drivetrain.swerveModuleControl import SwerveModuleControl
from drivetrain.swerveModuleGainSet import SwerveModuleGainSet
from drivetrain.drivetrainTrajectoryControl import DrivetrainTrajectoryControl
from drivetrain.drivetrainPhysical import MAX_FWD_REV_SPEED_MPS
from drivetrain.drivetrainPhysical import FL_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import FR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BL_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import BR_ENCODER_MOUNT_OFFSET_RAD
from drivetrain.drivetrainPhysical import FL_INVERT_WHEEL_MOTOR
from drivetrain.drivetrainPhysical import FR_INVERT_WHEEL_MOTOR
from drivetrain.drivetrainPhysical import BL_INVERT_WHEEL_MOTOR
from drivetrain.drivetrainPhysical import BR_INVERT_WHEEL_MOTOR
from drivetrain.drivetrainPhysical import INVERT_AZMTH_MOTOR
from drivetrain.drivetrainPhysical import INVERT_AZMTH_ENCODER
from drivetrain.drivetrainPhysical import kinematics


class DrivetrainControl(metaclass=Singleton):
    """
    Top-level control class for controlling a swerve drivetrain
    """
    def __init__(self):
        self.stt = SegmentTimeTracker()
        #                                                                          1         2         3
        #                                                                 12345678901234567890123456789012345
        self.markDesModStatesName          = self.stt.makePaddedMarkName("desModStates")
        self.markDesaturateWheelSpeedsName = self.stt.makePaddedMarkName("desaturateWheelSpeeds")
        self.markSendToModulesName         = self.stt.makePaddedMarkName("SendCommandsToModuleAndUpdate")
        self.markPoseEstUpdateName         = self.stt.makePaddedMarkName("poseEst.update")
        self.markGainsHasChangedName       = self.stt.makePaddedMarkName("gains.hasChanged")
        self.modules = []
        self.modules.append(SwerveModuleControl("FL", 2, 3, 0,
            FL_ENCODER_MOUNT_OFFSET_RAD, FL_INVERT_WHEEL_MOTOR, INVERT_AZMTH_MOTOR, INVERT_AZMTH_ENCODER))
        self.modules.append(SwerveModuleControl("FR", 4, 5, 1,
            FR_ENCODER_MOUNT_OFFSET_RAD, FR_INVERT_WHEEL_MOTOR, INVERT_AZMTH_MOTOR, INVERT_AZMTH_ENCODER))
        self.modules.append(SwerveModuleControl("BL", 6, 7, 2,
            BL_ENCODER_MOUNT_OFFSET_RAD, BL_INVERT_WHEEL_MOTOR, INVERT_AZMTH_MOTOR, INVERT_AZMTH_ENCODER))
        self.modules.append(SwerveModuleControl("BR", 8, 9, 3,
            BR_ENCODER_MOUNT_OFFSET_RAD, BR_INVERT_WHEEL_MOTOR, INVERT_AZMTH_MOTOR, INVERT_AZMTH_ENCODER))
        self.desChSpd = ChassisSpeeds()
        self.curDesPose = Pose2d()

        self.gains = SwerveModuleGainSet()

        self.poseEst = DrivetrainPoseEstimator(self.getModulePositions())

        self.trajCtrl = DrivetrainTrajectoryControl()

        self._updateAllCals()

    def setCmdFieldRelative(self, velX, velY, velT):
        """Send commands to the robot for motion relative to the field

        Args:
            velX (float): Desired speed in the field's X direction, in meters per second
            velY (float): Desired speed in the field's Y axis, in th meters per second
            velT (float): Desired rotational speed in the field's reference frame, in radians per second
        """
        tmp = ChassisSpeeds.fromFieldRelativeSpeeds(
            velX, velY, velT, self.poseEst.getCurEstPose().rotation()
        )
        self.desChSpd = ChassisSpeeds.discretize(tmp.vx, tmp.vy, tmp.omega, 0.02)
        self.poseEst.telemetry.setDesiredPose(self.poseEst.getCurEstPose())

    def setCmdRobotRelative(self, velX, velY, velT):
        """Send commands to the robot for motion relative to its own reference frame

        Args:
            velX (float): Desired speed in the robot's X direction, in meters per second
            velY (float): Desired speed in the robot's Y axis, in th meters per second
            velT (float): Desired rotational speed in the robot's reference frame, in radians per second
        """
        self.desChSpd = ChassisSpeeds.discretize(velX, velY, velT, 0.02)
        self.poseEst.telemetry.setDesiredPose(self.poseEst.getCurEstPose())

    def setCmdTrajectory(self, cmd):
        """Send commands to the robot for motion as a part of following a trajectory

        Args:
            cmd (PathPlannerState): PathPlanner trajectory sample for the current time
        """
        tmp = self.trajCtrl.update(cmd, self.poseEst.getCurEstPose())
        self.desChSpd = ChassisSpeeds.discretize(tmp.vx, tmp.vy, tmp.omega, 0.02)
        self.poseEst.telemetry.setDesiredPose(cmd.getPose())

    def update(self):
        """
        Main periodic update, should be called every 20ms
        """


        # Given the current desired chassis speeds, convert to module states
        desModStates = kinematics.toSwerveModuleStates(self.desChSpd)
        self.stt.perhapsMark(self.markDesModStatesName)

        # Scale back commands if one corner of the robot is going too fast
        kinematics.desaturateWheelSpeeds(desModStates, MAX_FWD_REV_SPEED_MPS)
        self.stt.perhapsMark(self.markDesaturateWheelSpeedsName)

        # Send commands to modules and update
        for idx, module in enumerate(self.modules):
            module.setDesiredState(desModStates[idx])
            module.update()
        self.stt.perhapsMark(self.markSendToModulesName)

        # Update the estimate of our pose
        self.poseEst.update(self.getModulePositions(), self.getModuleSpeeds())
        self.stt.perhapsMark(self.markPoseEstUpdateName)

        # Update calibration values if they've changed
        if self.gains.hasChanged():
            self._updateAllCals()
        self.stt.perhapsMark(self.markGainsHasChangedName)

    def _updateAllCals(self):
        # Helper function - updates all calibration on request
        for module in self.modules:
            module.setClosedLoopGains(self.gains)

    def getModulePositions(self):
        """
        Returns:
            Tuple of the actual module positions (as read from sensors)
        """
        return tuple(mod.getActualPosition() for mod in self.modules)

    def getModuleSpeeds(self):
        """
        Returns:
            Tuple of the actual module speeds (as read from sensors)
        """
        return tuple(mod.getActualState() for mod in self.modules)

    def resetGyro(self):
        # Update pose estimator to think we're at the same translation,
        # but aligned facing downfield
        curTranslation = self.poseEst.getCurEstPose().translation()
        newGyroRotation = Rotation2d.fromDegrees(180.0) if(onRed()) else Rotation2d.fromDegrees(0.0)
        #try: newGyroRotation = Rotation2d.fromDegrees(0.0) if(onRed()) else Rotation2d.fromDegrees(180.0)
        newPose = Pose2d(curTranslation, newGyroRotation)
        self.poseEst.setKnownPose(newPose)

    def getCurEstPose(self) -> Pose2d:
        # Return the current best-guess at our pose on the field.
        return self.poseEst.getCurEstPose()
