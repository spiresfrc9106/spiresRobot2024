# AutoSequencerV2

Casserole has developed an in-house autonomous coordination infrastrcuture.

Starting in 2023 it got a major overhaul, incorporting a more flexible event/command grouping scheme, and methods to _compose_ things together.

It is intentionally modeled after WPILib's command-based paradigms, but without requriing subsystem architecture. Think of it as both a stepping stone to a full command-based paradigm, without committing to restructuring other code.

The autosequencer is a singleton- there is only ever one sequencer. One sequencer may have multiple mode lists. The selection from each mode list should be concatenated together with an `andThen()` composition.

See [the AutoSequencerV2 requirements](..\requirements\AutoSequencerV2Requirements.md) for more info.

## Usage - Code

### Main Robot Integration

First, import the AutoSequencer class.

```py
from AutoSequencerV2.autoSequencer import AutoSequencer
```

Second, declare a new AutoSequencer, and add all autonomous modes.

```py
def robotInit(self):
    # ...
    # New AutoSequencer
    self.autoSequencer = AutoSequencer()
    # Add each Auto Mode
    self.autoSequencer.addMode(MyNewAutoMode())
    # ...
```

Then, call the auto sequencer methods from the three Autonomous methods:

```py
def autonomousInit(self):
    # Start up the autonomous sequencer
    self.autoSequencer.initiaize()

def autonomousPeriodic(self):
    self.autoSequencer.update()

def autonomousExit(self):
    self.autoSequencer.end()
```

These methods must always be called in the order of initialize -> update -> end

To allow users to select the mode(s), add an approprate set of widgets to the dashboard.

```py
    webserver.addDashboardWidget(
        AutoChooser(50, 10, 
            self.autoSequencer.getDelayModeNTTableName(), 
            self.autoSequencer.getDelayModeList()))
    webserver.addDashboardWidget(
        AutoChooser(50, 20, 
            self.autoSequencer.getMainModeNTTableName(), 
            self.autoSequencer.getMainModeList()))
```

[More information about adding widgets is found here.](dashboardWidgets.py)

The call to `get*NTTableName()` returns a string, indicating what NetworkTables topic should be used for selecting an autonomous mode.

The call to `get*ModeList()` returns a list of strings, indicating what human-readable name the dashboard should display for modes.

### Creating new Autonomous Modes

First, make a new file, named after the mode you want to have.

Import the generic mode class.

```py
from AutoSequencerV2.mode import Mode
```

Create a new class for your new mode, which extends the base `Mode` class.

```py
class MyNewMode(Mode):

    def getCmdGroup(self):
        # TODO - return a command group that should be run when this mode is selected
        #return WaitCommand(4.0).andThen(WaitCommand(3.0)).andThen(WaitCommand(5.0))
    
    def getInitialDrivetrainPose(self):
        # TODO - Return the Pose2d() of where the robot starts for this mode
        # Ex: return Pose2d(0,0,0)
    
    def getName(self):
        # TODO - Return a custom name for this mode
        # ex: return "leeeroooyy jeeeennnkkinnnsssss"
```

See above for registering the mode with the AutoSequencer.