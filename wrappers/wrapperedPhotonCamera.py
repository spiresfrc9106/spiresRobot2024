import wpilib
from wpimath.units import feetToMeters
from photonlibpy.photonCamera import PhotonCamera, VisionLEDMode, setVersionCheckEnabled
from utils.fieldTagLayout import FieldTagLayout
from utils.faults import Fault


class CameraPoseObservation:
    def __init__(self, time, estFieldPose, trustworthiness=1.0):
        self.time = time
        self.estFieldPose = estFieldPose
        self.trustworthiness = trustworthiness  # TODO - not used yet

#

class WrapperedPhotonCamera:
    def __init__(self, camName, robotToCam):
        setVersionCheckEnabled(False)

        self.cam = PhotonCamera(camName)

        self.disconFault = Fault(f"Camera {camName} not sending data")
        self.timeoutSec = 1.0
        self.poseEstimates = []
        self.robotToCam = robotToCam

    def update(self, prevEstPose):
        # Test Only
        if wpilib.DriverStation.isTest():
            self.cam.setLEDMode(VisionLEDMode.kBlink)
        elif wpilib.DriverStation.isAutonomous():
            self.cam.setLEDMode(VisionLEDMode.kOn)
        else:
            self.cam.setLEDMode(VisionLEDMode.kOff)

        if wpilib.DriverStation.isAutonomous():
            self.cam.takeInputSnapshot()
            self.cam.takeOutputSnapshot()

        # Grab whatever the camera last reported for observations in a camera frame
        # Note: Results simply report "I processed a frame". There may be 0 or more targets seen in a frame
        res = self.cam.getLatestResult()
        obsTime = res.getTimestamp()

        # Update our disconnected fault if we haven't seen anything from the camera
        self.disconFault.set(
            (wpilib.Timer.getFPGATimestamp() - obsTime) > self.timeoutSec
        )
        self.poseEstimates = []

        # Process each target.
        # Each target has multiple solutions for where you could have been at on the field
        # when you observed it
        # (https://docs.wpilib.org/en/stable/docs/software/vision-processing/
        # apriltag/apriltag-intro.html#d-to-3d-ambiguity)
        # We want to select the best possible pose per target
        # We should also filter out targets that are too far away, and poses which
        # don't make sense.
        for target in res.getTargets():
            # Transform both poses to on-field poses
            tgtID = target.getFiducialId()
            if tgtID >= 0:
                # Only handle valid ID's
                tagFieldPose = FieldTagLayout().lookup(tgtID)
                if tagFieldPose is not None:
                    # Only handle known tags
                    poseCandidates = []
                    poseCandidates.append(
                        self._toFieldPose(tagFieldPose, target.getBestCameraToTarget())
                    )
                    poseCandidates.append(
                        self._toFieldPose(
                            tagFieldPose, target.getAlternateCameraToTarget()
                        )
                    )

                    # Filter candidates in this frame to only the valid ones
                    filteredCandidates = []
                    for candidate in poseCandidates:
                        onField = self._poseIsOnField(candidate)
                        # Add other filter conditions here
                        if onField:
                            filteredCandidates.append(candidate)

                    # Pick the candidate closest to the last estimate
                    bestCandidate = None
                    bestCandidateDist = 99999999.0
                    for candidate in filteredCandidates:
                        delta = (candidate - prevEstPose).getTranslation().getNorm()
                        if delta < bestCandidateDist:
                            # This candidate is better, use it
                            bestCandidate = candidate
                            bestCandidateDist = delta

                    # Finally, add our best candidate the list of pose observations
                    if bestCandidate is not None:
                        self.poseEstimates.append(
                            CameraPoseObservation(obsTime, bestCandidate)
                        )

    def getPoseEstimates(self):
        return self.poseEstimates

    def _toFieldPose(self, tgtPose, camToTarget):
        camPose = tgtPose.transformBy(camToTarget.inverse())
        return camPose.transformBy(self.robotToCam.inverse()).toPose2d()

    # Returns true of a pose is on the field, false if it's outside of the field perimieter
    def _poseIsOnField(self, pose):
        trans = pose.getTranslation()
        x = trans.getX()
        y = trans.getY()
        inY = 0.0 <= y <= feetToMeters(27.0)
        inX = 0.0 <= x <= feetToMeters(54.0)
        return inX and inY
