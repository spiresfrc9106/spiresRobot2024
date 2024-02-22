from AutoSequencerV2.autoSequencer import AutoSequencer
from dashboardWidgets.autoChooser import AutoChooser
from dashboardWidgets.swerveState import SwerveState
from dashboardWidgets.text import Text
from webserver.webserver import Webserver


class Dashboard:
    def __init__(self):
        Webserver().addDashboardWidget(Text(50, 75, "/SmartDashboard/faultDescription"))
        Webserver().addDashboardWidget(SwerveState(85, 15))
        Webserver().addDashboardWidget(
            AutoChooser(
                50,
                10,
                AutoSequencer().getDelayModeNTTableName(),
                AutoSequencer().getDelayModeList(),
            )
        )
        Webserver().addDashboardWidget(
            AutoChooser(
                50,
                20,
                AutoSequencer().getMainModeNTTableName(),
                AutoSequencer().getMainModeList(),
            )
        )
