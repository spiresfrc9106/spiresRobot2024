# Webserver

Casserole's robots have traditionally hosted a small website with debug, diagnostic, and dashboard information.

## Usage - End-User

The webserver on the robot is accessed at:

[http://10.91.6.2:5805](http://10.91.6.2:5805)

This is because the roboRIO is at the IP address `10.9.6.2`, and the website is served on port `5805`

If running in simulation, that same website is hosted on your PC (`localhost`). It can be accessed at:

[http://localhost:5805](http://localhost:5805)

## Usage - Code

First, import the webserver class.

```py
from webserver.webserver import Webserver
```

Then, within `robotInit()`, instantiate a webserver:

```py
ws = Webserver()
```

Most things in the website are automatically populated, and require no additional interaction. The main exception to this is the Dashboard. Each widget must be added

```py
ws.addDashboardWidget(myWidget)
```

[More information about adding widgets is found here.](dashboardWidgets.py)
