from PySide2.QtCore import Qt
from PySide2.QtGui import QCloseEvent, QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QWidget, QDialog, QGridLayout

from game import Game
from game.event import ControlPointType
from qt_ui.uiconstants import EVENT_ICONS
from qt_ui.windows.GameUpdateSignal import GameUpdateSignal
from qt_ui.windows.basemenu.QBaseMenuTabs import QBaseMenuTabs
from theater import ControlPoint


class QBaseMenu2(QDialog):

    def __init__(self, parent, cp: ControlPoint, game: Game):
        super(QBaseMenu2, self).__init__(parent)

        # Attrs
        self.cp = cp
        self.game = game
        self.is_carrier = self.cp.cptype in [ControlPointType.AIRCRAFT_CARRIER_GROUP, ControlPointType.LHA_GROUP]

        # Widgets
        self.qbase_menu_tab = QBaseMenuTabs(cp, game)

        try:
            self.airport = game.theater.terrain.airport_by_id(self.cp.id)
        except:
            self.airport = None

        if self.cp.captured:
            self.deliveryEvent = None

        self.setWindowIcon(EVENT_ICONS["capture"])

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMinimumSize(300, 200)
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)
        self.setModal(True)
        self.initUi()

    def initUi(self):
        self.setWindowTitle(self.cp.name)
        self.topLayoutWidget = QWidget()
        self.topLayout = QHBoxLayout()

        self.topLayoutWidget = QWidget()
        self.topLayout = QHBoxLayout()

        header = QLabel(self)
        header.setGeometry(0, 0, 655, 106)
        pixmap = QPixmap(self.get_base_image())
        header.setPixmap(pixmap)

        title = QLabel("<b>" + self.cp.name + "</b>")
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title.setProperty("style", "base-title")
        unitsPower = QLabel("{} / {} /  Runway : {}".format(self.cp.base.total_planes, self.cp.base.total_armor,
                                                            "Available" if self.cp.has_runway() else "Unavailable"))

        self.topLayout.addWidget(title)
        self.topLayout.addWidget(unitsPower)
        self.topLayout.setAlignment(Qt.AlignTop)
        self.topLayoutWidget.setProperty("style", "baseMenuHeader")
        self.topLayoutWidget.setLayout(self.topLayout)

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(header, 0, 0)
        self.mainLayout.addWidget(self.topLayoutWidget, 1, 0)
        self.mainLayout.addWidget(self.qbase_menu_tab, 2, 0)

        self.setLayout(self.mainLayout)

    def closeEvent(self, closeEvent:QCloseEvent):
        GameUpdateSignal.get_instance().updateGame(self.game)

    def get_base_image(self):
        if self.cp.cptype == ControlPointType.AIRCRAFT_CARRIER_GROUP:
            return "./resources/ui/carrier.png"
        elif self.cp.cptype == ControlPointType.LHA_GROUP:
            return "./resources/ui/lha.png"
        else:
            return "./resources/ui/airbase.png"