# Segment Time Tracker

It's critical we can verify that our perodic code is indeed executing at the rate we expect (one run every 20ms). Additionally, it's often useful to _instrumet_ parts of code to figure out which is taking the longest. This helps focus efforts when increasing the efficency of code. 

The `SegmentTimeTracker` class provides some convienet methods to do all of that.

To use it, first import it:

```py
from utils.segmentTimeTracker import SegmentTimeTracker
```

Then instantiate it once:

```py
def robotInit(self):
    #... other stuff
    self.myStt = SegmentTimeTracker()
    #... more other stuff
```

At a minimum, call the `start()` and `end()` methods as the first and last steps of a periodic method:

```py

def robotPeriodic(self):
    self.mySttt.start()
    # Do all the periodic stuff
    self.mySttt.end()
```

Additionally, the `mark()` method can be called in the middle of periodic execution to sub-divide the loop:

```py

# some code
self.stt.mark("some code")

# some more code
self.stt.mark("some more code")
```

If the loop takes too long, a message will be printed which contains the overall duration, as well as the duration between each mark. This should help narrow down which parts of code are taking the longest.