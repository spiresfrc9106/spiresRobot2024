# Signal

In code, we often want to keep track of how a value changes over time. We have created code to help streamline this, creating what we call a 'Signal" to track it.

To record a signal, first import the signal modules:

```py
from utils.signalLogging import log
```

Then, after you've calculated the value, record it with the `log` function:

```py
log("signal name", val)
```

Be sure that `"signal name"` is unique - recording the same named signal in multiple spots will cause issues.

All signals are recorded both to the website (NT), and to  log files on disc.