import installer_first_window
import installer_second_window
from PyQt6 import QtWidgets


class InstallerFirstWindow(QtWidgets.QMainWindow, installer_first_window.Ui_InstallerFirstWindow):
    def __init__(self, parent=None):
        super(InstallerFirstWindow, self).__init__(parent)
        self.setupUi(self)


class InstallerSecondWindow(QtWidgets.QMainWindow, installer_second_window.Ui_InstallerSecondWindow):
    def __init__(self, parent=None):
        super(InstallerSecondWindow, self).__init__(parent)
        self.setupUi(self)
