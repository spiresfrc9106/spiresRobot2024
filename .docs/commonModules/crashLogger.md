# Crash Logger

It's useful to have as much information as possible if our robot code stops working.

While on the field, it's unlikely someone will be watching the driver station logs to catch the exact stack trace as it flies past.

In cases like this, we want errors logged to files so that we can read the files after the crash to determine root cause.

The `CrashLogger` class sets up just such a log. To use it, first import it:

```py
from utils.crashLogger import CrashLogger
```

Instantiate it, ideally as one of the first things in `robotInit()`

```py
self.crashLogger = CrashLogger()
```

Finally, call the update function in the `robotPeriodic()` class:

```py
self.crashLogger.update()
```

This update function makes sure that as soon as FMS or time information is available, it gets dumped to file.

Crash logs should show up on the flash drive of the roboRIO, under a folder `/U/crashLogs`. They are numbered, the highest number is the most recent log.
