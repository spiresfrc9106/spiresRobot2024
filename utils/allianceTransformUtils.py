import wpilib
from wpimath.geometry import Pose2d, Rotation2d, Transform2d, Translation2d
from jormungandr.choreoTrajectory import ChoreoTrajectoryState
from utils.constants import FIELD_LENGTH_FT
from utils.units import ft2m

"""
 Utilities to help transform from blue alliance to red if needed
 We went rogue and chose a coordinate system where the origin is always in the 
 bottom left on the blue alliance
"""

def onRed():
    return wpilib.DriverStation.getAlliance() == wpilib._wpilib.DriverStation.Alliance.kRed # pylint: disable=protected-access
        
def transformX(givenM):
    if onRed():
        return (ft2m(FIELD_LENGTH_FT) - givenM)
    else:
        return givenM

def transform(givenObject):
    # pylint: disable=too-many-return-statements
    # pylint: disable=too-many-branches
    if isinstance(givenObject,Rotation2d):
        if onRed():
            return (Rotation2d.fromDegrees(180) - givenObject)
        else: 
            return givenObject

    elif isinstance(givenObject,Translation2d):
        if onRed():
            return Translation2d(transformX(givenObject.X()), givenObject.Y())
        else:
            return givenObject

    elif isinstance(givenObject,Transform2d):
        if onRed():
            trans = transform(givenObject.translation())
            rot = transform(givenObject.rotation())
            return Transform2d(trans, rot)
        else:
            return givenObject

    elif isinstance(givenObject,Pose2d):
        if onRed():
            trans = transform(givenObject.translation())
            rot = transform(givenObject.rotation())
            return Pose2d(trans, rot)
        else:
            return givenObject

    elif isinstance(givenObject,ChoreoTrajectoryState):
        if onRed():
            return givenObject.flipped()
        else:
            return givenObject

    raise TypeError("transform function received unknown type")
