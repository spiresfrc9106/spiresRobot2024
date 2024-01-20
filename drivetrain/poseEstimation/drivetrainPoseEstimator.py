import random
import wpilib
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Rotation2d, Twist2d
from drivetrain.drivetrainPhysical import kinematics
from drivetrain.drivetrainPhysical import wrapperedGyro
from drivetrain.poseEstimation.drivetrainPoseTelemetry import DrivetrainPoseTelemetry
from utils.faults import Fault
from utils.signalLogging import log


class DrivetrainPoseEstimator():
    """Wrapper class for all sensors and logic responsible for estimating where the robot is on the field
    """
    def __init__(self, initialModuleStates):
        self.curEstPose = Pose2d()
        self.curDesPose = Pose2d()
        self.gyro = wrapperedGyro()
        self.gyroDisconFault = Fault("Gyro Disconnected")

        #self.cam = WrapperedPhotonCamera("TEST_CAM", Transform3d())
        self.camTargetsVisible = False

        self.poseEst = SwerveDrive4PoseEstimator(
            kinematics, self.gyro.getRotation2d(), initialModuleStates, self.curEstPose
        )
        self.lastModulePositions = initialModuleStates
        self.curRawGyroAngle = Rotation2d()
        self.telemetry = DrivetrainPoseTelemetry()

        self._simPose = Pose2d()

    def setKnownPose(self, knownPose):
        """Reset the robot's estimated pose to some specific position. This is useful if we know with certanty
        we are at some specific spot (Ex: start of autonomous)

        Args:
            knownPose (Pose2d): The pose we know we're at
        """
        if wpilib.TimedRobot.isSimulation():
            self._simPose = knownPose
            self.curRawGyroAngle = knownPose.rotation()

        self.poseEst.resetPosition(
            self.curRawGyroAngle, self.lastModulePositions, knownPose
        )


    def update(self, curModulePositions, curModuleSpeeds):
        """Periodic update, call this every 20ms.

        Args:
            curModulePositions (list[SwerveModuleState]): current module angle
            and wheel positions as read in from swerve module sensors
        """

        # Add any vision observations to the pose estimate
        #self.cam.update(self.curEstPose)
        self.camTargetsVisible = False
        #for observation in self.cam.getPoseEstimates():
        #    self.poseEst.addVisionMeasurement(observation.estFieldPose, observation.time)
        #    self.camTargetsVisible = True
        log("PE Vision Targets Seen", self.camTargetsVisible, "bool")

        # Read the gyro angle
        self.gyroDisconFault.set(not self.gyro.isConnected())
        if wpilib.TimedRobot.isSimulation():
            # Simulate an angel based on (simulated) motor speeds with some noise
            chSpds = kinematics.toChassisSpeeds(curModuleSpeeds)
            self._simPose = self._simPose.exp(
                Twist2d(chSpds.vx * 0.02, chSpds.vy * 0.02, chSpds.omega * 0.02)
            )
            noise = Rotation2d.fromDegrees(random.uniform(-1.25, 1.25))
            self.curRawGyroAngle = self._simPose.rotation() + noise
        else:
            # Use real hardware
            self.curRawGyroAngle = self.gyro.getRotation2d()

        # Update the WPILib Pose Estimate
        self.poseEst.update(self.curRawGyroAngle, curModulePositions)
        self.curEstPose = self.poseEst.getEstimatedPosition()

        # Record the estimate to telemetry/logging
        log("PE Gyro Angle", self.curRawGyroAngle.degrees(), "deg")
        self.telemetry.update(self.curEstPose)

        # Remember the module positions for next loop
        self.lastModulePositions = curModulePositions

    def getCurEstPose(self):
        """
        Returns:
            Pose2d: The most recent estimate of where the robot is at
        """
        return self.curEstPose
