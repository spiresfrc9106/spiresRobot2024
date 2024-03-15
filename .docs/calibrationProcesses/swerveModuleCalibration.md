# Swerve Module Calibration

## Setup
- Place the robot on blocks so no wheels are contacting the ground
- Turn on the robot
- Connect your computer to the robot's network (WiFi or Ethernet)
- Open a code editor (PyCharm or VSCode)
- Open a terminal (the built-in PyCharm or VSCode terminal is fine)
- Open the FRC Driver Station
- Connect an XBox Controller to the Driver Station
- Open AdvantageScope and connect to the robot (File > Connect to robot)

## Zero-out Calibrations
1. Checkout the correct git branch. Don't know which branch to use? Run `robotpy deploy-info` in the terminal for the currently deployed version.
2. Open `drivetrain/robotDependentConstants.py` in the editor. Find the configuration for the relevant robot. Set the configuration for `FL_OFFSET`, `FR_OFFSET`, `BL_OFFSET`, and `BR_OFFSET`. Set all these values to 0. Save the file.
3. Deploy these changes to the robot with `robotpy deploy --skip-tests`
4. Enable teleoperation mode from the driver station and see that the wheels reset to the wrong default positions. Disable teleop.

## Determine Initial Offsets
1. In AdvantageScope find `SmartDashboard/DtModule_FL_azmthAct`. Draf it to the "Left Axis" area. Do the same for `SmartDashboard/DtModule_FR_azmthAct`, `SmartDashboard/DtModule_BL_azmthAct`, and `SmartDashboard/DtModule_BR_azmthAct`.
2. Use a swerve module square to align the front left wheel with the chassis. Ensure that the square fits snuggly all the way around. There is a notch in the wheel hole for the geared side of the wheel.
3. Find the current reading for the FL wheel in AdvantageScope. Update `FL_OFFSET` in `robotDependentConstants.py` with this value.
4. Remove the swerve module square.
5. Is the wheel facing forward and backward? Good skip the next step.
6. Is the wheel facing side to side? Then add 90 to the previously set value (e.g. `FL_OFFSET: 74.3+90`).
7. Repeat steps 2-6 for the other three wheels.

## Validate Configuration
1. Ensure your changes to `robotDependentConstants.py` have been saved. Re-deploy the code with `robotpy deploy --skip-tests`.
2. When the robot is ready, enable Teleoperation mode from the Driver Station. The wheels should reset to their default position (keep in mind that this may include being "toed in").
3. Press the A button to reset the gyro.
4. Drive forward slowly. The wheels should be facing perfectly forward and backward. They should all be turning the same direction.
5. Did some wheels turn the wrong direction? Add 180 to their respective offset configurations (e.g. `74.3+90+180`). Restart the Validate Configuration section.
6. Once all the wheels are driving forward and backward correctly, validate that strafe and rotate are behaving appropriately too.
