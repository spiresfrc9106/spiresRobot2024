#Constants we may need
#Just starting with the minimum stuff we need
#The math conversions are under units.py

FIELD_LENGTH_FT = 54.0

"""
    This is mostly the old java stuff we used, the drivetrain is under DrivetrainPhysical

    //////////////////////////////////////////////////////////////////
    // Electrical
    //////////////////////////////////////////////////////////////////

    // PWM Bank
    public static final int LED_MODE_PORT = 0;
    public static final int LED_STRIP_PORT = 1;
    static public final int CLAW_INTAKE = 2;
    //static public final int UNUSED = 3;
    //static public final int UNUSED = 4;
    //static public final int UNUSED = 5;
    //static public final int UNUSED = 6;
    //static public final int UNUSED = 7;
    //static public final int UNUSED = 8;
    //static public final int UNUSED = 9;

    // DIO Bank
    static public final int FL_AZMTH_ENC_IDX = 0; 
    static public final int FR_AZMTH_ENC_IDX = 1;
    static public final int BL_AZMTH_ENC_IDX = 2;
    static public final int BR_AZMTH_ENC_IDX = 3;
    static public final int ARM_BOOM_ENC_IDX = 4;
    static public final int ARM_STICK_ENC_IDX = 5;
    static public final int FAULT_LED_OUT_IDX = 6;
    static public final int HEARTBEAT_LED_OUT_IDX = 7;
    //static public final int UNUSED = 8;
    //static public final int UNUSED = 9;

    // Analog Bank
    static public final int PRESSURE_SENSOR_ANALOG = 0;
    //static public final int UNUSED = 1;
    //static public final int UNUSED = 2;
    //static public final int UNUSED = 3;

    // CAN Bus Addresses - Motors
    //static public final int RESERVED_DO_NOT_USE = 0; // default for most stuff
    //static public final int RESERVED_DO_NOT_USE = 1; // Rev Power Distribution Hub
    static public final int FL_WHEEL_MOTOR_CANID = 2;
    static public final int FL_AZMTH_MOTOR_CANID = 3;
    static public final int FR_WHEEL_MOTOR_CANID = 4;
    static public final int FR_AZMTH_MOTOR_CANID = 5;
    static public final int BL_WHEEL_MOTOR_CANID = 6;
    static public final int BL_AZMTH_MOTOR_CANID = 7;
    static public final int BR_WHEEL_MOTOR_CANID = 8;
    static public final int BR_AZMTH_MOTOR_CANID = 9;
    static public final int ARM_BOOM_MOTOR_CANID = 10;
    static public final int ARM_STICK_MOTOR_CANID = 11;
    static public final int GAMEPIECE_DIST_SENSOR_CANID = 12;
    //static public final int UNUSED = 13;
    //static public final int UNUSED = 14;
    //static public final int UNUSED = 15;
    //static public final int UNUSED = 16;
    //static public final int UNUSED = 17;

    // Pneumatics Hub
    static public final int CLAW_SOLENOID = 0;
    static public final int ARM_BOOM_BRAKE_SOLENOID = 1;
    //static public final int UNUSED = 2;
    //static public final int UNUSED = 3;
    //static public final int UNUSED = 4;
    //static public final int UNUSED = 5;
    //static public final int UNUSED = 6;
    //static public final int UNUSED = 7;
    //static public final int UNUSED = 8;
    //static public final int UNUSED = 9; 

    // PDP Channels - for current measurement
    static public final int CUBE_BLOWER_CURRENT_CHANNEL = 0;
    static public final int BOOM_CURRENT_CHANNEL = 1;
    static public final int STICK_CURRENT_CHANNEL = 2;
	static public final int LEFT_INTAKE_CURRENT_CHANNEL = 3;
    static public final int RIGHT_INTAKE_CURRENT_CHANNEL = 4;
    static public final int FL_WHEEL_CURRENT_CHANNEL = 5;
    static public final int FL_AZMTH_CURRENT_CHANNEL = 6;
    static public final int FR_WHEEL_CURRENT_CHANNEL = 7;
    static public final int FR_AZMTH_CURRENT_CHANNEL = 8;
    static public final int BL_WHEEL_CURRENT_CHANNEL = 9;
    static public final int BL_AZMTH_CURRENT_CHANNEL = 10;
    static public final int BR_WHEEL_CURRENT_CHANNEL = 11;
    static public final int BR_AZMTH_CURRENT_CHANNEL = 12;
    //static public final int UNUSED = 13;
    //static public final int UNUSED = 14;
    //static public final int UNUSED = 15;
    //static public final int UNUSED = 16;
    //static public final int UNUSED = 17;
    //static public final int UNUSED = 18;
    //static public final int UNUSED = 19;
    

    //////////////////////////////////////////////////////////////////
    // Nominal Sample Times
    //////////////////////////////////////////////////////////////////
    public static final double Ts = 0.02;
    public static final double SIM_SAMPLE_RATE_SEC = 0.001;

    //////////////////////////////////////////////////////////////////
    // Field Dimensions
    //////////////////////////////////////////////////////////////////
    static public final double FIELD_WIDTH_M = Units.feetToMeters(27.0);
    static public final double FIELD_LENGTH_M = Units.feetToMeters(54.0);
    static public final Translation2d MAX_ROBOT_TRANSLATION = new Translation2d(FIELD_LENGTH_M, FIELD_WIDTH_M);
    static public final Translation2d MIN_ROBOT_TRANSLATION = new Translation2d(0.0,0.0);
    // Assumed starting location of the robot. Auto routines will pick their own location and update this.
    public static final Pose2d DFLT_START_POSE = new Pose2d(3, 3, new Rotation2d(0));


    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ////  Derived Constants
    //// - You can reference how these are calculated, but shouldn't
    ////   have to change them
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////

    
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // HELPER ORGANIZATION CONSTANTS
    static public final int FL = 0; // Front Left Module Index
    static public final int FR = 1; // Front Right Module Index
    static public final int BL = 2; // Back Left Module Index
    static public final int BR = 3; // Back Right Module Index
    static public final int NUM_MODULES = 4;

    // Internal objects used to track where the modules are at relative to
    // the center of the robot, and all the implications that spacing has.
    static public final List<Translation2d> robotToModuleTL = Arrays.asList(
        new Translation2d( Constants.WHEEL_BASE_HALF_WIDTH_M,  Constants.WHEEL_BASE_HALF_WIDTH_M),
        new Translation2d( Constants.WHEEL_BASE_HALF_WIDTH_M, -Constants.WHEEL_BASE_HALF_WIDTH_M),
        new Translation2d(-Constants.WHEEL_BASE_HALF_WIDTH_M,  Constants.WHEEL_BASE_HALF_WIDTH_M),
        new Translation2d(-Constants.WHEEL_BASE_HALF_WIDTH_M, -Constants.WHEEL_BASE_HALF_WIDTH_M)
    );

    static public final List<Transform2d> robotToModuleTF = Arrays.asList(
        new Transform2d(robotToModuleTL.get(FL), new Rotation2d(0.0)),
        new Transform2d(robotToModuleTL.get(FR), new Rotation2d(0.0)),
        new Transform2d(robotToModuleTL.get(BL), new Rotation2d(0.0)),
        new Transform2d(robotToModuleTL.get(BR), new Rotation2d(0.0))
    );

    static public final SwerveDriveKinematics m_kinematics = new SwerveDriveKinematics(
        robotToModuleTL.get(FL), 
        robotToModuleTL.get(FR), 
        robotToModuleTL.get(BL), 
        robotToModuleTL.get(BR)
    );
   
}
"""