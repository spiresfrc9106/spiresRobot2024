import math
from wpilib import ADIS16470_IMU
from wpilib import SPI
from wpimath.units import inchesToMeters
from wpimath.system.plant import DCMotor
from wpimath.geometry import Translation2d
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.geometry import Rotation2d
import navx
from utils.units import lbsToKg
from utils.units import deg2Rad
from utils.units import in2m
from wrappers.wrapperedRevThroughBoreEncoder import WrapperedRevThroughBoreEncoder
from drivetrain.robotDependentConstants import RobotDependentConstants
from config import ROBOT_BUILD

from utils.singleton import Singleton




class wrapperedNavx(navx.AHRS):
    """
    Class to wrap a navx
    """
    def __init__(self):
        """
         5. __init__(self: navx._navx.AHRS,
            spi_port_id: wpilib._wpilib.SPI.Port, spi_bitrate: int, update_rate_hz: int) -> None

        :param port: SPI Port to use
        :type port: :class:`.SPI.Port`
        :param spi_bitrate: SPI bitrate (Maximum:  2,000,000)
        :param update_rate_hz: Custom Update Rate (Hz)
        """
        super().__init__(spi_port_id=SPI.Port.kMXP, spi_bitrate=1000000, update_rate_hz=50)


    def getYawAxis(self):
        curRawGyroAngleAsRotation2d = self.getRotation2d()
        return

    def _getGyroAngle(self):
        


class wrapperedAdis16470Imu(ADIS16470_IMU):

    def __init__(self):
        """
         5. __init__(self: navx._navx.AHRS,
            spi_port_id: wpilib._wpilib.SPI.Port, spi_bitrate: int, update_rate_hz: int) -> None

        :param port: SPI Port to use
        :type port: :class:`.SPI.Port`
        :param spi_bitrate: SPI bitrate (Maximum:  2,000,000)
        :param update_rate_hz: Custom Update Rate (Hz)
        """
        super().__init__()

    def _getGyroAngle(self):
        return Rotation2d().fromDegrees(self.getAngle(self.getYawAxis()))

class wrapperedGyro():
    """
     5. __init__(self: navx._navx.AHRS,
        spi_port_id: wpilib._wpilib.SPI.Port, spi_bitrate: int, update_rate_hz: int) -> None

    :param port: SPI Port to use
    :type port: :class:`.SPI.Port`
    :param spi_bitrate: SPI bitrate (Maximum:  2,000,000)
    :param update_rate_hz: Custom Update Rate (Hz)
    """
    if constants["GYRO"]=="NAVX":
        print(f'GYRO is {constants["GYRO"]}')
        result = navx.AHRS(spi_port_id=SPI.Port.kMXP, spi_bitrate=1000000, update_rate_hz=50)
    elif constants["GYRO"]=="ADIS16470_IMU":
        print(f'GYRO is {constants["GYRO"]}')
        result = ADIS16470_IMU()
    else:
        print(f'GYRO is {constants["GYRO"]}')
        result = NoGyro()
    return result


# Array of translations from robot's origin (center bottom, on floor) to the module's contact patch with the ground
robotToModuleTranslations = []
robotToModuleTranslations.append(
    Translation2d(WHEEL_BASE_HALF_LENGTH_M, WHEEL_BASE_HALF_WIDTH_M)
)
robotToModuleTranslations.append(
    Translation2d(WHEEL_BASE_HALF_LENGTH_M, -WHEEL_BASE_HALF_WIDTH_M)
)
robotToModuleTranslations.append(
    Translation2d(-WHEEL_BASE_HALF_LENGTH_M, WHEEL_BASE_HALF_WIDTH_M)
)
robotToModuleTranslations.append(
    Translation2d(-WHEEL_BASE_HALF_LENGTH_M, -WHEEL_BASE_HALF_WIDTH_M)
)

# WPILib Kinematics object
kinematics = SwerveDrive4Kinematics(
    robotToModuleTranslations[FL],
    robotToModuleTranslations[FR],
    robotToModuleTranslations[BL],
    robotToModuleTranslations[BR],
)