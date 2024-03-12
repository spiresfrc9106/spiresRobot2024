# Calibration

A _Calibration_ is a numeric value which is normally a constant during robot operation, but might have to be tuned or tweaked as part of a software development process.

Common examples include ramp rates, debounce times, and PID constants. All these are numbers which impact the feel or response of the robot, and are "tuned to taste".

An anti-example would be a gear ratio or wheel radius. These are known and unchanging, and should simply be constants in the code (and not adjusted).

## Usage - End-User

Calibrations by default are shown in the [webserver](webserver.md). Their values can be adjusted through the webpage. Be sure to set up the webserver properly in code for Calibrations to show up.

## Usage - Code

To declare a new Calibration, first import the proper module:

```py
from utils.calibration import Calibration
```

Then, declare your Calibration.

```py
myCal = Calibration(name="My super cool calibration", default=0)
```

The Calibration must have a unique `name`, and provide a `default` value.

Some optional arguments include:

```py
myCal = Calibration(name="My super cool calibration", default=0, units="m/s", minVal=-4, maxVal=8.5)
```

The `units` field is purely cosmetic, but is a useful reminder to the person doing calibration what units they are working in.

The allowable range of the Calibration can be specified with `minVal` and `maxVal` to prevent the person who is doing calibration from entering a nonsensical or destructive value.

Finally, in code, access the Calibration's current value with the `get()` method.

```py
curVal = myCal.get()
```

### One-Shot Update

The easiest way to use a calibration is to simply read its value with `get()` every loop. However, sometimes one-time actions need to be executed when the calibration is updated from the website.

A common example is reconfiguring PID constants in CAN motor controllers. We only need to send value updates once, when they are changed. We should not send them every loop.

The `isChanged()` method will indicate whether cal's value has been changed since the last call to `get()`.

```py
if(myCal.isChanged()):
    newVal = myCal.get()
    # ...
    # do something with newVal
```

