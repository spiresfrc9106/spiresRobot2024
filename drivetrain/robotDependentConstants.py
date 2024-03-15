class RobotDependentConstants:
    def __init__(self):
        self.robotConstants = {
            '2023': {
                "MAX_SWERVE_WHEEL_GEAR_RATIO": 5.50, # Base Low
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.08, # Base Medium
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 4.71, # Base High
                "SWERVE_WHEEL_DIAMETER_IN": 3.0,
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 169.2+90+180,
                "FR_OFFSET": -49.7,
                "BL_OFFSET": -56.2+180,
                "BR_OFFSET": -11.2-90+180,
                "GYRO": "NAVX", # "NAVX", # "ADIS16470_IMU",
            },
            '2023sim': {
                "MAX_SWERVE_WHEEL_GEAR_RATIO": 5.50, # Base Low
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.08, # Base Medium
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 4.71, # Base High
                "SWERVE_WHEEL_DIAMETER_IN": 3.0,
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
                "GYRO": "NAVX", # "ADIS16470_IMU",
            },
            '2024': {
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.50, # Base Low
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.08, # Base Medium
                "MAX_SWERVE_WHEEL_GEAR_RATIO": 4.71, # Base High
                "SWERVE_WHEEL_DIAMETER_IN": 3.0,
                "WIDTH": 22.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 177.4-90,
                "FR_OFFSET": 0.7,
                "BL_OFFSET": 125.4-180,
                "BR_OFFSET": 117.5-90-180,
                "GYRO": "ADIS16470_IMU",
            },
            '2024sim': {
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.50, # Base Low
                #"MAX_SWERVE_WHEEL_GEAR_RATIO": 5.08, # Base Medium
                "MAX_SWERVE_WHEEL_GEAR_RATIO": 4.71, # Base High
                "SWERVE_WHEEL_DIAMETER_IN": 3.0,
                "WIDTH": 22.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
                "GYRO": "ADIS16470_IMU",
            }
        }

    def get(self):
        return self.robotConstants
