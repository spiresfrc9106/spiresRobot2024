import math

import wpilib

from wpimath.units import metersToFeet
from wpimath.trajectory import Trajectory
from wpimath.geometry import Pose2d
from utils.signalLogging import log
from utils.allianceTransformUtils import transform


class DrivetrainPoseTelemetry:
    """
    Helper class to wrapper sending all drivetrain Pose related information 
    to dashboards
    """

    def __init__(self):
        self.field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("DT Pose 2D", self.field)
        self.curTraj = Trajectory()
        self.desPose = Pose2d()

    def setDesiredPose(self, desPose):
        self.desPose = desPose

    def update(self, estPose):
        self.field.getRobotObject().setPose(estPose)
        self.field.getObject("desPose").setPose(self.desPose)
        self.field.getObject("desTraj").setTrajectory(self.curTraj)

        log("DT Pose Est X", metersToFeet(estPose.X()), "ft")
        log("DT Pose Est Y", metersToFeet(estPose.Y()), "ft")
        log("DT Pose Est T", estPose.rotation().degrees(), "deg")
        log("DT Pose Des X", metersToFeet(self.desPose.X()), "ft")
        log("DT Pose Des Y", metersToFeet(self.desPose.Y()), "ft")
        log("DT Pose Des T", self.desPose.rotation().degrees(), "deg")

    def setTrajectory(self, trajIn):
        """Display a specific trajectory on the robot Field2d

        Args:
            trajIn (PathPlannerTrajectory): The trajectory to display
        """
        # Transform choreo state list into useful trajectory for telemetry
        if trajIn is not None:
            stateList = []

            # For visual appearance and avoiding sending too much over NT,
            # make sure we only send a sampled subset of the positions
            sampTime = 0
            while sampTime < trajIn.getTotalTime():
                stateList.append(self._choreoToWPIState(transform(trajIn.sample(sampTime))))
                sampTime += 0.5

            # Make sure final pose is in the list
            stateList.append(self._choreoToWPIState(transform(trajIn.samples[-1])))

            self.curTraj = Trajectory(stateList)
        else:
            self.curTraj = Trajectory()

    # PathPlanner has a built in "to-wpilib" representation, but it doesn't
    # account for holonomic heading. Fix that.
    def _choreoToWPIState(self, inVal):
        return Trajectory.State(
            acceleration=0,
            pose=inVal.getPose(),
            t=inVal.timestamp,
            velocity=math.hypot(inVal.velocityX, inVal.velocityY),
        )
