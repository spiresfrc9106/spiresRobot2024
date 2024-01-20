import socketserver
import socket
import threading
import functools
from webserver.casseroleWebServerImpl import (
    CasseroleWebServerImpl,
    dashboardWidgetList,
    WEB_ROOT,
)
from utils.singleton import Singleton


# A threaded TCP server starts up new python threads for each client request, which allows
# complex requests to be handled in the background and not bog down robot code
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# Main robot website server
class Webserver(metaclass=Singleton):
    def __init__(self):
        httpPort = 5805

        # Serve all contents of the webserver/www folder, with special
        # logic to handle filling out template html files
        templatingHttpHandler = functools.partial(
            CasseroleWebServerImpl, directory=str(WEB_ROOT)
        )

        hostname = socket.gethostname()
        ipAddr="unknown"
        try:
            ipAddr=socket.gethostbyname(hostname)
        except socket.gaierror:
            # socket.gaierror is thrown when there is no dns server.
            # This can happen when there is no FRC Radio and the roborio
            # is connected directly to a dhcp server on a non-robot 
            # private network during development. Allow this
            # development mode to work.
            pass

        self.httpServer = ThreadedTCPServer(("", httpPort), templatingHttpHandler)

        # Start a thread with the HTTP server -- that thread will then start one
        # more thread for each request
        self.serverThread = threading.Thread(target=self.httpServer.serve_forever)
        # Exit the server thread when the main thread terminates
        self.serverThread.daemon = True
        self.serverThread.start()

        print(
            f"Server started on {hostname} at {ipAddr}:{httpPort} "
            + "in thread { self.serverThread.name}"
        )

    # Ensure we invoke shutdown procedures on the class destruction
    def __del__(self):
        print("Server shutting down")
        self.shutdown()

    # Stop the server and the background thread its running in.
    def shutdown(self):
        self.httpServer.shutdown()
        self.serverThread.join()

    # public api to submit a new dashboard widget
    def addDashboardWidget(self, widget):
        widget.idx = len(dashboardWidgetList)
        dashboardWidgetList.append(widget)
