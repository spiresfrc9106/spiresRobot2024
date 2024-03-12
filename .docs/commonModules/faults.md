# Faults

A _Fault_ is a class containing a text description of a problem which software can detect, and a status indicating if the problem exists or not.

Faults should be used to inform the pit crew or drive team of a condition on the robot which software cannot rectify and needs attention.

## Usage - Code

### Faults

To declare a new Fault, first import the proper module:

```py
from utils.faults import Fault
```

Then, declare your Fault.

```py
myFault = Fault("This thing is broken!")
```

The Fault must have a short but descriptive message.

The `units` field is purely cosmetic, but is a useful reminder to the person doing calibration what units they are working in.

Finally, in code, set the current value of the fault:

```py
if(good_stuff):
    myFault.setNoFault()

if(bad_stuff):
    myFault.setFaulted()
```

### Fault Wrangler

The `FaultWrangler` singleton class is used to hold the list of all current faults, and change LED state and text description string for active faults.

A RIO output is driven by the `FaultStatusLEDs` to pulse when one or more faults are active. A white pulsing heartbeat LED also indicates that code is running.

A few things are necessary to keep the whole system ticking:

```py

def robotInit(self):
    # ...
    self.faultLEDs = FaultStatusLEDs()
    # ...

def robotPeriodic(self):
    # ...
    FaultWrangler().update()
    self.faultLEDs.update()
    # ...

```
