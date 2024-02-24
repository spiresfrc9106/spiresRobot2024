from wpilib import ADIS16470_IMU
from wpilib import SPI
from wpimath.geometry import Rotation2d
import navx
from drivetrain.robotDependentConstants import RobotDependentConstants
from config import ROBOT_BUILD

constants = RobotDependentConstants().get()[ROBOT_BUILD]

class WrapperedNoGyro():
    def __init__(self):
        pass

    def getGyroAngleRotation2d(self):
        return Rotation2d(0.0)

    def isConnected(self):
        return False
class WrapperedNavx(navx.AHRS):
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

    def getGyroAngleRotation2d(self):
        return self.getRotation2d()



class WrapperedAdis16470Imu(ADIS16470_IMU):

    def getGyroAngleRotation2d(self):
        return Rotation2d().fromDegrees(self.getAngle(self.getYawAxis()))

def wrapperedGyro():
    result = None
    if constants["GYRO"]=="NAVX":
        print(f'GYRO is {constants["GYRO"]}')
        result = WrapperedNavx()
    elif constants["GYRO"]=="ADIS16470_IMU":
        print(f'GYRO is {constants["GYRO"]}')
        result = WrapperedAdis16470Imu()
    else:
        print(f'GYRO is {constants["GYRO"]}')
        result = WrapperedNoGyro()
    return result
