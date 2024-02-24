# firstRoboPy
A very simple first attempt at robot written in python

![Workflow Status](https://github.com/RobotCasserole1736/firstRoboPy/actions/workflows/ci.yml/badge.svg)

## Installation

Before developing code on a new computer, perform the following:

1. [Download and install wpilib](https://github.com/wpilibsuite/allwpilib/releases)
2. [Download and install python](https://www.python.org/downloads/)
3. Run these commands:

```cmd
    python -m pip install --upgrade pip
    python -m pip install robotpy[all]
    python -m robotpy_installer download-python
    python -m pip install -r requirements_dev.txt
    python -m pip install -r requirements_run.txt
```

## Docs

[Click here to see documentation for common libraries](docs/UserAPI).

## The robot website

On a simulator: http://localhost:5805/

On a RoboRIO:

* RobotCasserole: http://10.17.36.2:5805/
* Spires: http://10.91.6.2:5805/

# Interesting commands

## options for pytest


Add a space '--' space and then pytest options: https://docs.pytest.org/en/6.2.x/usage.html

```cmd
python -m robotpy test -- -xvv
python -m robotpy test -- -xvvvv
python -m robotpy test -- -xlsvvvv
```

`-xvv` is the same as `-x -vv`

`-xlsvvvv` is the same as `-x -l -s -vvvv`
```

Details

```cmd
python -m robotpy test -- --tb=auto    # (default) 'long' tracebacks for the first and last
                                       # entry, but 'short' style for the other entries
python -m robotpy test -- --tb=long    # exhaustive, informative traceback formatting
python -m robotpy test -- --full-trace # long traces to be printed on error (longer than --tb=long). It also ensures 
                                       # that a stack trace is printed on KeyboardInterrupt (Ctrl+C). This is very 
                                       # useful if the tests are taking too long and you interrupt them with Ctrl+C to 
                                       # find out where the tests are hanging. By default no output will be shown 
                                       # (because KeyboardInterrupt is caught by pytest). By using this option you make
                                       # sure a trace is shown.
python -m robotpy test -- -l           # pytest lets the stderr/stdout flow through to the console
python -m robotpy test -- -s           # pytest lets the stderr/stdout flow through to the console
python -m robotpy test -- -v           # show each individual test step
python -m robotpy test -- -vv          # pytest shows more details of what faild
python -m robotpy test -- -vvv         # some plugins might make use of -vvv verbosity.
python -m robotpy test -- -vvvv        # some plugins might make use of -vvvv verbosity.
python -m robotpy test -- -x           # stop after first failure
```

# Interesting links

https://github.com/robotpy/mostrobotpy

https://docs.pytest.org/en/7.4.x/

https://pytest.org/en/7.4.x/example/index.html


# TODO Fix these up.

## Deploying to the Robot

`deploy.bat` will deploy all code to the robot. Be sure to be on the same network as the robot.

`.deploy_cfg` contains specific configuration about the deploy process.

Note any folder or file prefixed with a `.` will be skipped in the deploy.

## Linting

Yavin clutch code:

```
pylint --rcfile=.pylintrc **\*.py
```

"Linting" is the process of checking our code format and style to keep it looking nice

`lint.bat` will execute the linter.

`.pylintrc` contains configuration about what checks the linter runs, and what formatting it enforces


## Testing

Run the `Test` configuration in the debugger in vsCode.

## Simulating

Run the `Simulate` configuration in the debugger in vsCode.

## Continuous Integration

Github runs our code on its servers on every commit to ensure our code stays high quality. This is called "Continuous Integration".

`.github/workflows/ci.yml` contains configuration for all the commands that our continuous integration environment.

To minimize frustration and rework, before committing, be sure to:


1. Run lint and fix any formatting errors
```cmd
pylint --rcfile=.pylintrc $(git ls-files '*.py')
```
2. Run the test suite
```cmd
python -m robotpy test
```
## RIO First-time Installation

Follow [the robotpy instructions for setting up the RIO](https://robotpy.readthedocs.io/en/stable/install/robot.html)

Then, install all packages specific to our repo, from `requirements_run.txt`, following the
[two step process for roboRIO package installer](https://robotpy.readthedocs.io/en/stable/install/packages.html)

While on the internet:

`python -m robotpy_installer download -r requirements_run.txt`

Then, while connected to the robot's network:

```cmd
python -m robotpy_installer install-python
python -m robotpy_installer install robotpy
python -m robotpy_installer install -r requirements_run.txt
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

In python, `requirements.txt` lists out all the non-standard packages that need to be installed.

However, a few hangups:

* The list of dependencies for the RIO and for our PC's to do software development is different
* The RIO has limited disk storage space, so we don't want extra packages if we can avoid it.

For now, we're resolving that by having two requirements files - `requirements_dev.txt` lists everything needed just for software development. `requirements_run.txt` lists everything needed to run the code.

Development PC's should pip-install both.

The RoboRIO should only install _run.txt

When recording a new dependency, run `pip freeze > tmp.txt`, then open up `tmp.txt`. It will have a lot of things inside it. Find your new dependency in the list, and add it to the appropriate requirements file. Then delete `tmp.txt`

# Useful stuff:

python -m netconsole roboRIO-9106-frc.local

ssh lvuser@roboRIO-9106-frc.local

## Roborio 2.0 image

The 2023 roborio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2020\project\roboRIO Tool\FRC Images\SD Images

The 2024 roboio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2023\project\roboRIO Tool\FRC Images\SD Images


## Quick notes on install:

Use balenaEtcher to install the roborio image

The 2023 roborio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2020\project\roboRIO Tool\FRC Images\SD Images

The 2024 roboio 2.0 image is here:

C:\Program Files (x86)\National Instruments\LabVIEW 2023\project\roboRIO Tool\FRC Images\SD Images

use roborio team number setter to set the team number


`python -m robotpy_installer download -r requirements_run.txt`

Then, while connected to the robot's network:

```cmd
python -m robotpy_installer install-python
python -m robotpy_installer install robotpy
python -m robotpy_installer install -r requirements_run.txt
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
