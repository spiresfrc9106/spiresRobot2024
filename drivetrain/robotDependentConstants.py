class RobotDependentConstants:
    def __init__(self):
        self.robotConstants = {
            '2023': {
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": (-110+180),# TODO RMS trying backing out the INVERT_WHEEL_MOTOR and adding it to FL_OFFSET
                "FR_OFFSET": (-54),
                "BL_OFFSET": (-59+180), # TODO RMS trying backing out the INVERT_WHEEL_MOTOR and adding it to BL_OFFSET
                "BR_OFFSET": (75),
            },
            '2023sim': {
                "WIDTH": 16.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
            },
            '2024': {
                "WIDTH": 22.5,
                "LENGTH": 26.5,
                "FL_OFFSET": 265,
                "FR_OFFSET": 57,
                "BL_OFFSET": 487,
                "BR_OFFSET": 209,
            },
            '2024sim': {
                "WIDTH": 22.5,
                "LENGTH": 3*26.5,
                "FL_OFFSET": 0,
                "FR_OFFSET": 0,
                "BL_OFFSET": 0,
                "BR_OFFSET": 0,
            }
        }

    def get(self):
        return self.robotConstants
