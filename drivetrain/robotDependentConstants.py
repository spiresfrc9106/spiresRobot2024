class RobotDependentConstants:
    def __init__(self):
        self.robotConstants = {
            '2023': {
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": (-110+180),
                "FR_OFFSET": (-54),
                "BL_OFFSET": (-59+180),
                "BR_OFFSET": (75),
                "GYRO": "NAVX", # "NAVX", # "ADIS16470_IMU",
            },
            '2023sim': {
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
                "GYRO": "NAVX", # "ADIS16470_IMU",
            },
            '2024': {
                "WIDTH": 22.5,
                "LENGTH": 26.5,
                "FL_OFFSET": (265-180), # todo unverified guess at adjustment changing to INVERT_WHEEL_MOTOR=False
                "FR_OFFSET": 57,
                "BL_OFFSET": (487-180), # todo unverified guess at adjustment changing to INVERT_WHEEL_MOTOR=False
                "BR_OFFSET": 209,
                "GYRO": "NAVX",
            },
            '2024sim': {
                "WIDTH": 22.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
                "GYRO": "NAVX",
            }
        }

    def get(self):
        return self.robotConstants
