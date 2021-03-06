# Form implementation generated from reading ui file 'InstallerSecondWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InstallerSecondWindow(object):
    def setupUi(self, InstallerSecondWindow):
        InstallerSecondWindow.setObjectName("InstallerSecondWindow")
        InstallerSecondWindow.resize(800, 456)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        InstallerSecondWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("download.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        InstallerSecondWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(InstallerSecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bFinish = QtWidgets.QPushButton(self.centralwidget)
        self.bFinish.setEnabled(False)
        self.bFinish.setGeometry(QtCore.QRect(710, 380, 75, 24))
        self.bFinish.setObjectName("bFinish")
        self.OutputLabel = QtWidgets.QLabel(self.centralwidget)
        self.OutputLabel.setGeometry(QtCore.QRect(10, 50, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.OutputLabel.setFont(font)
        self.OutputLabel.setObjectName("OutputLabel")
        self.OutputText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.OutputText.setGeometry(QtCore.QRect(13, 80, 771, 241))
        self.OutputText.setReadOnly(True)
        self.OutputText.setObjectName("OutputText")
        self.checkRunAfterInstall = QtWidgets.QCheckBox(self.centralwidget)
        self.checkRunAfterInstall.setEnabled(False)
        self.checkRunAfterInstall.setGeometry(QtCore.QRect(20, 380, 221, 20))
        self.checkRunAfterInstall.setObjectName("checkRunAfterInstall")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(17, 340, 761, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.checkDesktopShortcut = QtWidgets.QCheckBox(self.centralwidget)
        self.checkDesktopShortcut.setGeometry(QtCore.QRect(10, 10, 151, 20))
        self.checkDesktopShortcut.setChecked(True)
        self.checkDesktopShortcut.setObjectName("checkDesktopShortcut")
        self.checkStartMenuShortcut = QtWidgets.QCheckBox(self.centralwidget)
        self.checkStartMenuShortcut.setGeometry(QtCore.QRect(10, 30, 171, 20))
        self.checkStartMenuShortcut.setChecked(True)
        self.checkStartMenuShortcut.setObjectName("checkStartMenuShortcut")
        self.bInstall = QtWidgets.QPushButton(self.centralwidget)
        self.bInstall.setGeometry(QtCore.QRect(700, 40, 75, 24))
        self.bInstall.setObjectName("bInstall")
        InstallerSecondWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InstallerSecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        InstallerSecondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InstallerSecondWindow)
        self.statusbar.setObjectName("statusbar")
        InstallerSecondWindow.setStatusBar(self.statusbar)

        self.retranslateUi(InstallerSecondWindow)
        QtCore.QMetaObject.connectSlotsByName(InstallerSecondWindow)

    def retranslateUi(self, InstallerSecondWindow):
        _translate = QtCore.QCoreApplication.translate
        InstallerSecondWindow.setWindowTitle(_translate("InstallerSecondWindow", "PyPassMan Installer"))
        self.bFinish.setStatusTip(_translate("InstallerSecondWindow", "Finish"))
        self.bFinish.setWhatsThis(_translate("InstallerSecondWindow", "Finish"))
        self.bFinish.setText(_translate("InstallerSecondWindow", "Finish"))
        self.OutputLabel.setText(_translate("InstallerSecondWindow", "Output:"))
        self.OutputText.setStatusTip(_translate("InstallerSecondWindow", "Output"))
        self.OutputText.setWhatsThis(_translate("InstallerSecondWindow", "Output"))
        self.OutputText.setPlainText(_translate("InstallerSecondWindow", "Install directory:"))
        self.checkRunAfterInstall.setText(_translate("InstallerSecondWindow", "Run PyPassMan After Installation."))
        self.checkDesktopShortcut.setText(_translate("InstallerSecondWindow", "Create desktop shortcut"))
        self.checkStartMenuShortcut.setText(_translate("InstallerSecondWindow", "Create start menu shortcut"))
        self.bInstall.setStatusTip(_translate("InstallerSecondWindow", "Install"))
        self.bInstall.setWhatsThis(_translate("InstallerSecondWindow", "Install"))
        self.bInstall.setText(_translate("InstallerSecondWindow", "Install"))
