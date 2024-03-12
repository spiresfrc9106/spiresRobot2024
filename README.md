# Spires 2024 - Team #9106

![Dev CI Status](https://github.com/spiresfrc9106/spiresRobot2024/actions/workflows/ci.yml/badge.svg?branch=dev)

Source code for the Spires 2024 robot.

This repository started as a fork of [RobotCasserole2024](https://github.com/RobotCasserole1736/RobotCasserole2024). We are grateful to Team #1736 for the inspiration.

## Installation

Before developing code on a new computer, perform the following:

1. [Download and install wpilib](https://github.com/wpilibsuite/allwpilib/releases)
2. [Download and install python](https://www.python.org/downloads/)
3. Run these commands:

```cmd
    python -m pip install --upgrade pip
    python -m pip install robotpy
    python -m robotpy_installer download-python
    python -m pip install -r requirements_dev.txt
```

## Docs

[Click here to see documentation for common libraries](.docs/UserAPI).

## The robot website

On a simulator
- http://localhost:5805/

On a RoboRIO
- http://10.91.6.2:5805/
- Be sure that you are connected to the RoboRIO's network via WiFi or Ethernet

## Interesting links

[RobotPy source code](https://github.com/robotpy/mostrobotpy)

[PyTest Docs](https://docs.pytest.org/en/7.4.x/)

[PyTest Examples](https://pytest.org/en/7.4.x/example/index.html)

## Deploying to the Robot

Use the `WPILib: Deploy Robot Code` task in VSCode's command palette.

OR

`robotpy deploy` will deploy all code to the robot. Be sure to be on the robot's network via WiFi or Ethernet.

### Deploy Notes

`robotpy deploy --skip-tests` to avoid requiring tests to pass before deployment can proceed. This is helpful for quick iterations, but don't make it a bad habit.

`.deploy_cfg` contains specific configuration about the deploy process.

Any folder or file prefixed with a `.` will be skipped in the deploy. This is good to avoid sending unnecessary files to the resource limited RoboRIO like documentation and images.

## Linting

"Linting" is the process of checking our code format and style to keep it looking nice and avoid unnecessary inconsistencies.

`pylint --rcfile=.pylintrc **\*.py`

`.pylintrc` contains configuration about what checks the linter runs, and what formatting it enforces

## Testing

Run the `WPILib: Test Robot Code` task in VSCode's command palette.

OR

`robotpy test`

## Simulating

Run the `WPILib: Simulate Robot Code` task in VSCode's command palette.

OR

`robotpy sim`

## RIO First-time Installation

Follow [the robotpy instructions for setting up the RIO](https://robotpy.readthedocs.io/en/stable/install/robot.html)

Then, install all packages specific to our repo, from `requirements_dev.txt`, following the
[two step process for roboRIO package installer](https://robotpy.readthedocs.io/en/stable/install/packages.html)

While on the internet:

`python -m robotpy_installer download -r requirements_dev.txt`

Then, while connected to the robot's network:

```cmd
python -m robotpy_installer install-python
python -m robotpy_installer install robotpy
python -m robotpy_installer list
```

To check what is installed:

`python -m robotpy_installer list`

example output:
```cmd
10:32:35:371 INFO    : robotpy.installer   : RobotPy Installer 2023.0.4
10:32:35:371 INFO    : robotpy.installer   : -> caching files at C:\Users\MikeStitt\wpilib\2023\robotpy
10:32:35:372 INFO    : robotpy.installer   : -> using existing config at 'C:\Users\MikeStitt\Documents\first\sw\spiresFrc9106\firstRoboPy\.installer_config'
10:32:35:374 INFO    : robotpy.installer   : Finding robot for team 9106
10:32:35:380 INFO    : robotpy.installer   : -> Robot is at 172.22.11.2
10:32:35:380 INFO    : robotpy.installer   : Connecting to robot via SSH at 172.22.11.2
10:32:35:495 INFO    : paramiko.transport  : Connected (version 2.0, client OpenSSH_8.3)
10:32:35:599 INFO    : paramiko.transport  : Auth banner: b'NI Linux Real-Time (run mode)\n\nLog in with your NI-Auth credentials.\n\n'
10:32:35:600 INFO    : paramiko.transport  : Authentication (password) successful!
10:32:35:676 INFO    : robotpy.installer   : -> RoboRIO 2 image version: 2023_v3.2
10:32:35:752 INFO    : robotpy.installer   : -> RoboRIO disk usage 584.0M/3.3G (17% full)
Package                   Version
------------------------- ----------
debugpy                   1.8.0
numpy                     1.24.2
pip                       22.3.1
pyntcore                  2023.4.3.0
robotpy                   2023.4.3.1
robotpy-apriltag          2023.4.3.0
robotpy-commands-v2       2023.4.3.0
robotpy-cscore            2023.4.3.0
robotpy-ctre              2023.1.0
robotpy-hal               2023.4.3.0
robotpy-libgfortran5      12.1.0+r5
robotpy-navx              2023.0.3
robotpy-openblas          0.3.21+r2
robotpy-opencv            4.6.0+r2
robotpy-opencv-core       4.6.0+r2
robotpy-pathplannerlib    2023.3.4.1
robotpy-photonvision      2023.4.2
robotpy-playingwithfusion 2023.1.0
robotpy-rev               2023.1.3.2
robotpy-wpilib-utilities  2023.1.0
robotpy-wpimath           2023.4.3.0
robotpy-wpinet            2023.4.3.0
robotpy-wpiutil           2023.4.3.0
setuptools                65.5.0
wpilib                    2023.4.3.0
```

## Dependency Management

`requirements_dev.txt` is used to list dependencies that we only need on our development computers, not on the RoboRIO. This is tools like linting and formatting; they aren't mission critical (or even used) at runtime, but still very helpful to have.

`pyproject.toml` defines the dependencies that are required to be installed on the RoboRIO for our code to successfully run. For tests and simulations you will also need these dependencies on your development machine. They are managed automatically via `robotpy sync`.

## Useful commands:

See network logs: `python -m netconsole roboRIO-9106-frc.local`

SSH into the robot: `ssh lvuser@roboRIO-9106-frc.local`

## Roborio 2.0 image install

Use balenaEtcher to install the roborio image

The 2023 roborio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2020\project\roboRIO Tool\FRC Images\SD Images

The 2024 roboio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2023\project\roboRIO Tool\FRC Images\SD Images

use roborio team number setter to set the team number
