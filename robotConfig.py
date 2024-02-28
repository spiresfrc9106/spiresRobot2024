from webserver.webserver import Webserver
from dashboard import Dashboard

# pylint: disable=R0801

def webserverConstructorOrNone():
    return Webserver()

def dashboardOrNone():
    return Dashboard()
