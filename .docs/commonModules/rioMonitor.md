# RIO Monitor

It's useful to track statistics on how our roboRIO is doing as a PC. This can help make sure we will continue to run smoothly on the field.

To monitor these metrics, first import the class:

```py
from utils.rioMonitor import RIOMonitor
```

Then, simply instantiate it.

```py
self.rioMonitor = RIOMonitor()
```

The class will start recording and producing new logged signals in the background.