# Dashboard

The driver dashboard allows for a customizable widget layout. Multiple widgets are availble.

## Basic Dashboard Concepts

The following info assumes the webserver has already been instantiated:

```py
webserver = Webserver()
```

Each new widget is added to the dashboard with the `addDashboardWidget()` method:

```py
webserver.addDashboardWidget(
            <new widget here>)
```

All widgets should be instantiated and added inside of `robotInit()`

You will have to import all the widget types you want to use:

```py
from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.camera import Camera, getRIOStreamURL
from dashboardWidgets.circularGauge import CircularGauge
from dashboardWidgets.lineGauge import LineGauge
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
```

### Location

The X/Y location of each widget defines its _center_, as a percentage of the screen. 

For X, 0 is to the left, and 100 is to the right.

For Y, 0 is at the top, and 100 is at the bottom.

X and Y location should always be the first two arguments when making a new dashboard widget.

### NT4 Topic

All widgets are tied to one or more Network Tables topics. To change the value of the widget, the networktables value must be updated.

[Glass](https://docs.wpilib.org/en/stable/docs/software/dashboards/glass/introduction.html) is the wpilib tool used to inspect what values are currently available in networktables.

All [signals](signal.md) produce an NT4 topic. Creating a signal for a dashboard widget is probably the easiest way to provide values to drive the widget.

The NT table topic should be a string, and will be the third argument when making a new dashboard widget.

## Specific Widget Types

### Gauges

Gauges show a numeric value at a glance. They all have the following features:

1. A color change to indicate when the value is "good" or "bad".
2. A graphical pointer that moves between a fixed min and max value.
3. A numeric readout of the actual number.

These three layers are necessary for comprehending the meaning of the value as fast as possible during a match.

1. Color is the fastest - no notion of value, simply "we're ok" or "we have a problem"
2. Pointer is slower, but more accurate. It gives a relative sense of low/medium/high
3. Numeric value takes the longest to read and understand, but is the most detiled.

The last four arguments define the min and max range of the widget (#2), as well as the min and max acceptable values where the color should transition.

```
        red            green                red
<---|----------|--------------------|--------------------|--->
    min        min acceptable       max acceptable       max
```

#### Circular Gauge

```py
webserver.addDashboardWidget(
            CircularGauge(15, 15, "/SmartDashboard/test", -10,10,-5,5))
```

#### Line Gauge

```py
webserver.addDashboardWidget(
            LineGauge(15, 50, "/SmartDashboard/test", -10,10,-5,5))
```

### Text

Text widgets display a string. It's useful for text messages, states, or simple numbers.

```py
webserver.addDashboardWidget(
    Text(30, 75, "/SmartDashboard/test"))
```

### Swerve State

A swerve state widget helps debug the actual and desired speed for all four wheels, and the actual and desired angles for all four modules.

Unlike other widgets, it has a hardcoded list of NT topics it subscribes to. For it to work, you _must_ publish the following NT topics:

```
/SmartDashboard/DtModule_FL_azmthDes
/SmartDashboard/DtModule_FL_azmthAct
/SmartDashboard/DtModule_FL_speedDes
/SmartDashboard/DtModule_FL_speedAct
/SmartDashboard/DtModule_FR_azmthDes
/SmartDashboard/DtModule_FR_azmthAct
/SmartDashboard/DtModule_FR_speedDes
/SmartDashboard/DtModule_FR_speedAct
/SmartDashboard/DtModule_BL_azmthDes
/SmartDashboard/DtModule_BL_azmthAct
/SmartDashboard/DtModule_BL_speedDes
/SmartDashboard/DtModule_BL_speedAct
/SmartDashboard/DtModule_BR_azmthDes
/SmartDashboard/DtModule_BR_azmthAct
/SmartDashboard/DtModule_BR_speedDes
/SmartDashboard/DtModule_BR_speedAct
```

Once published, it can be added very simply:

```py
webserver.addDashboardWidget(
    SwerveState(85, 15))
```

### Camera

A camera widget shows a MJPEG camera stream from the RIO or from a coprocessor.

Unlike other widgets, it does not require a NT topic. It instead requires the web address of the MJPEG stream to view.

```py
webserver.addDashboardWidget(
    Camera(75, 60, "http://roborio-9106-frc.local:1181"))
```

### Auto Chooser

The Auto-Chooser widget is hardcoded to work with AutoSequencerV2 to select two auto modes (one for delay, one for main mode).

```py
webserver.addDashboardWidget(
    AutoChooser(50, 10, 
        self.autoSequencer.getDelayModeNTTableName(), 
        self.autoSequencer.getDelayModeList()))
```
