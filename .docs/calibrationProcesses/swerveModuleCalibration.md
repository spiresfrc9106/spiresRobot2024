# Swerve Module Calibration

> [!CAUTION]
> This document is a work in progress, don't trust it too much :)

1. Turn on the robot and connect to its network.
2. Determine the currently deployed git branch with `robotpy deploy-info`. Checkout this branch `git checkout <BRANCH>`.
3. Open `robotDependentConstants.py`. Find the configuration for the relevant robot. Set the configuration for FLOffset, FROffset, BLOffset, and BROffset to 0. Save these changes.
4. Deploy the code with `robotpy deploy --skip-tests`
5. Open AdvantageScope and connect to the robot (File > Connect to Robot). Clear out any values currently on an axis or discrete fields section.
6. On the left side of AdvantageScope find SmartDashboard/FL_wheel_motorActPos and drag it to the "Left Axis" area. Do the same for FR_wheel_motorActPos, BL_wheel_motorActPos, and BR_wheel_motorActPos.
7. Use a Swerve Module square to align the front left wheel with the chassis. Ensure that the square fits snuggly all the way around. There is a notch in the wheel hole for the geared side of the wheel.
8. Find the current reading for the FL wheel in AdvantageScope. Update the FLOffset in `robotDependentConstants.py` with this value.
9. Remove the Swerve Module square.
10. Is the wheel facing forward and backward? Good, skip the next step.
11. Is the wheel facing side to side? Turn the wheel slightly as if you were going to align it foward and backward. Did the number go up? Then add 90 to the previous value. Did the number go down? Then subtract 90 from the previous value. (e.g. `FL_OFFSET: 74.3+90`).
12. Repeat steps 7-11 for the other 3 wheels.
13. Ensure your changes to `robotDependentConstants.py` have been saved. Re-deploy the code with `robotpy deploy --skip-tests`
14. When the robot is ready, enable TeleOp mode from the Driver Station, press the A button on the controller to reset the gyro, and drive forward slowly.
15. Do all the wheels turn in the forward direction? Good, you're done. Jump to step 17.
16. Did some wheels turn the wrong direction? Add 180 to their respective offset configs (e.g. `FL_OFFSET: 74.3+90+180`). Start again at step 13.
17. It's also valuable to check that the wheels are behaving when you strafe and rotate.