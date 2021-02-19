# Form implementation generated from reading ui file 'InstallerFirstWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InstallerFirstWindow(object):
    def setupUi(self, InstallerFirstWindow):
        InstallerFirstWindow.setObjectName("InstallerFirstWindow")
        InstallerFirstWindow.resize(800, 456)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        InstallerFirstWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("download.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        InstallerFirstWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(InstallerFirstWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PassmanagerInstallerLabel = QtWidgets.QLabel(self.centralwidget)
        self.PassmanagerInstallerLabel.setGeometry(QtCore.QRect(240, 20, 331, 71))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(24)
        self.PassmanagerInstallerLabel.setFont(font)
        self.PassmanagerInstallerLabel.setObjectName("PassmanagerInstallerLabel")
        self.brDirC = QtWidgets.QRadioButton(self.centralwidget)
        self.brDirC.setGeometry(QtCore.QRect(50, 140, 491, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.brDirC.setFont(font)
        self.brDirC.setAutoFillBackground(False)
        self.brDirC.setObjectName("brDirC")
        self.brDirCProgramFiles = QtWidgets.QRadioButton(self.centralwidget)
        self.brDirCProgramFiles.setGeometry(QtCore.QRect(50, 170, 491, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.brDirCProgramFiles.setFont(font)
        self.brDirCProgramFiles.setAutoFillBackground(False)
        self.brDirCProgramFiles.setObjectName("brDirCProgramFiles")
        self.brCustomLocation = QtWidgets.QRadioButton(self.centralwidget)
        self.brCustomLocation.setGeometry(QtCore.QRect(50, 200, 491, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.brCustomLocation.setFont(font)
        self.brCustomLocation.setAutoFillBackground(False)
        self.brCustomLocation.setObjectName("brCustomLocation")
        self.CustomLocationInput = QtWidgets.QLineEdit(self.centralwidget)
        self.CustomLocationInput.setEnabled(True)
        self.CustomLocationInput.setGeometry(QtCore.QRect(70, 230, 491, 22))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.CustomLocationInput.setFont(font)
        self.CustomLocationInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.CustomLocationInput.setReadOnly(False)
        self.CustomLocationInput.setObjectName("CustomLocationInput")
        self.SpaceRequiredLabel = QtWidgets.QLabel(self.centralwidget)
        self.SpaceRequiredLabel.setGeometry(QtCore.QRect(590, 110, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.SpaceRequiredLabel.setFont(font)
        self.SpaceRequiredLabel.setObjectName("SpaceRequiredLabel")
        self.bInstall = QtWidgets.QPushButton(self.centralwidget)
        self.bInstall.setGeometry(QtCore.QRect(480, 200, 75, 24))
        self.bInstall.setObjectName("bInstall")
        self.bClose = QtWidgets.QPushButton(self.centralwidget)
        self.bClose.setGeometry(QtCore.QRect(710, 380, 75, 24))
        self.bClose.setObjectName("bClose")
        self.installLabel = QtWidgets.QLabel(self.centralwidget)
        self.installLabel.setGeometry(QtCore.QRect(20, 110, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.installLabel.setFont(font)
        self.installLabel.setObjectName("installLabel")
        self.uninstallLabel = QtWidgets.QLabel(self.centralwidget)
        self.uninstallLabel.setGeometry(QtCore.QRect(20, 270, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.uninstallLabel.setFont(font)
        self.uninstallLabel.setObjectName("uninstallLabel")
        self.brUnins_dirC = QtWidgets.QRadioButton(self.centralwidget)
        self.brUnins_dirC.setGeometry(QtCore.QRect(50, 300, 491, 20))
        self.brUnins_dirC.setObjectName("brUnins_dirC")
        self.brUnins_dirCProgramFiles = QtWidgets.QRadioButton(self.centralwidget)
        self.brUnins_dirCProgramFiles.setGeometry(QtCore.QRect(50, 330, 491, 20))
        self.brUnins_dirCProgramFiles.setObjectName("brUnins_dirCProgramFiles")
        self.brUnins_CustomLocation = QtWidgets.QRadioButton(self.centralwidget)
        self.brUnins_CustomLocation.setGeometry(QtCore.QRect(50, 360, 491, 20))
        self.brUnins_CustomLocation.setObjectName("brUnins_CustomLocation")
        self.Unins_CustomLocationInput = QtWidgets.QLineEdit(self.centralwidget)
        self.Unins_CustomLocationInput.setEnabled(True)
        self.Unins_CustomLocationInput.setGeometry(QtCore.QRect(70, 390, 491, 22))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.Unins_CustomLocationInput.setFont(font)
        self.Unins_CustomLocationInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.Unins_CustomLocationInput.setReadOnly(False)
        self.Unins_CustomLocationInput.setObjectName("Unins_CustomLocationInput")
        self.bUninstall = QtWidgets.QPushButton(self.centralwidget)
        self.bUninstall.setGeometry(QtCore.QRect(480, 360, 75, 24))
        self.bUninstall.setObjectName("bUninstall")
        self.VersionLabel = QtWidgets.QLabel(self.centralwidget)
        self.VersionLabel.setGeometry(QtCore.QRect(590, 140, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.VersionLabel.setFont(font)
        self.VersionLabel.setObjectName("VersionLabel")
        self.VersionChannelLabel = QtWidgets.QLabel(self.centralwidget)
        self.VersionChannelLabel.setGeometry(QtCore.QRect(580, 0, 121, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        self.VersionChannelLabel.setFont(font)
        self.VersionChannelLabel.setObjectName("VersionChannelLabel")
        self.cbVersion = QtWidgets.QComboBox(self.centralwidget)
        self.cbVersion.setGeometry(QtCore.QRect(580, 20, 141, 22))
        self.cbVersion.setObjectName("cbVersion")
        self.bRefreshMetadata = QtWidgets.QPushButton(self.centralwidget)
        self.bRefreshMetadata.setGeometry(QtCore.QRect(580, 50, 111, 24))
        self.bRefreshMetadata.setObjectName("bRefreshMetadata")
        self.MustLabel = QtWidgets.QLabel(self.centralwidget)
        self.MustLabel.setGeometry(QtCore.QRect(700, 50, 101, 16))
        self.MustLabel.setObjectName("MustLabel")
        InstallerFirstWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InstallerFirstWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        InstallerFirstWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InstallerFirstWindow)
        self.statusbar.setObjectName("statusbar")
        InstallerFirstWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InstallerFirstWindow)
        QtCore.QMetaObject.connectSlotsByName(InstallerFirstWindow)

    def retranslateUi(self, InstallerFirstWindow):
        _translate = QtCore.QCoreApplication.translate
        InstallerFirstWindow.setWindowTitle(_translate("InstallerFirstWindow", "Passmanager Installer"))
        self.PassmanagerInstallerLabel.setText(_translate("InstallerFirstWindow", "Passmanager Installer"))
        self.brDirC.setText(_translate("InstallerFirstWindow", "Install to C:\\Passmanager"))
        self.brDirCProgramFiles.setText(_translate("InstallerFirstWindow", "Install to C:\\Program Files\\Passmanager"))
        self.brCustomLocation.setText(_translate("InstallerFirstWindow", "Install to Custom Location"))
        self.CustomLocationInput.setStatusTip(_translate("InstallerFirstWindow", "Custom Location Input"))
        self.CustomLocationInput.setWhatsThis(_translate("InstallerFirstWindow", "Custom Location Input"))
        self.SpaceRequiredLabel.setText(_translate("InstallerFirstWindow", "Space Required:"))
        self.bInstall.setStatusTip(_translate("InstallerFirstWindow", "Install"))
        self.bInstall.setWhatsThis(_translate("InstallerFirstWindow", "Install"))
        self.bInstall.setText(_translate("InstallerFirstWindow", "Install>"))
        self.bClose.setStatusTip(_translate("InstallerFirstWindow", "Close"))
        self.bClose.setWhatsThis(_translate("InstallerFirstWindow", "Close"))
        self.bClose.setText(_translate("InstallerFirstWindow", "Close"))
        self.installLabel.setText(_translate("InstallerFirstWindow", "Install:"))
        self.uninstallLabel.setText(_translate("InstallerFirstWindow", "Uninstall:"))
        self.brUnins_dirC.setText(_translate("InstallerFirstWindow", "Uninstall from C:\\Passmanager"))
        self.brUnins_dirCProgramFiles.setText(_translate("InstallerFirstWindow", "Uninstall from C:\\Program Files\\Passmanager"))
        self.brUnins_CustomLocation.setText(_translate("InstallerFirstWindow", "Uninstall from Custom Location"))
        self.Unins_CustomLocationInput.setStatusTip(_translate("InstallerFirstWindow", "Custom Location Input"))
        self.Unins_CustomLocationInput.setWhatsThis(_translate("InstallerFirstWindow", "Custom Location Input"))
        self.bUninstall.setStatusTip(_translate("InstallerFirstWindow", "Uninstall"))
        self.bUninstall.setWhatsThis(_translate("InstallerFirstWindow", "Uninstall"))
        self.bUninstall.setText(_translate("InstallerFirstWindow", "Uninstall"))
        self.VersionLabel.setText(_translate("InstallerFirstWindow", "Version:"))
        self.VersionChannelLabel.setText(_translate("InstallerFirstWindow", "Version Channel:"))
        self.bRefreshMetadata.setText(_translate("InstallerFirstWindow", "Refresh Metadata"))
        self.MustLabel.setText(_translate("InstallerFirstWindow", "(Must if changed)"))
