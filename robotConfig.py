"""
from utils.singleton import Singleton

# pylint: disable=R0801

class DisabledWebserver(metaclass=Singleton):

    def __init__(self):
        print(f"Disabled Webserver:Initializing")

    # Ensure we invoke shutdown procedures on the class destruction
    def __del__(self):
        print("Disabled Webserver:Server shutting down")

class DisabledDashboard():
    def __init__(self):
        print(f"Disabled Dashboard:Initializing")

    def __del__(self):
        print("Disabled Dashboard:Server shutting down")

#TODO-Chris The webserver and dashboad are disabled.
def webserverConstructorOrNone():
    return DisabledWebserver()

def dashboardOrNone():
    return DisabledDashboard()
"""

from webserver.webserver import Webserver
from dashboard import Dashboard

# pylint: disable=R0801

def webserverConstructorOrNone():
    return Webserver()

def dashboardOrNone():
    return Dashboard()
