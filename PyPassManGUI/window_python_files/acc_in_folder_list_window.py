# Form implementation generated from reading ui file 'AccInFolderListWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AccInFolderListWindow(object):
    def setupUi(self, AccInFolderListWindow):
        AccInFolderListWindow.setObjectName("AccInFolderListWindow")
        AccInFolderListWindow.resize(802, 358)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        AccInFolderListWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(AccInFolderListWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AccInFolderListText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.AccInFolderListText.setEnabled(True)
        self.AccInFolderListText.setGeometry(QtCore.QRect(10, 30, 781, 271))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.AccInFolderListText.setFont(font)
        self.AccInFolderListText.setReadOnly(True)
        self.AccInFolderListText.setObjectName("AccInFolderListText")
        self.FolderNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FolderNameLabel.setGeometry(QtCore.QRect(10, 0, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.FolderNameLabel.setFont(font)
        self.FolderNameLabel.setObjectName("FolderNameLabel")
        self.FolderNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.FolderNameInput.setGeometry(QtCore.QRect(130, 0, 531, 22))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.FolderNameInput.setFont(font)
        self.FolderNameInput.setObjectName("FolderNameInput")
        self.bListAccounts = QtWidgets.QPushButton(self.centralwidget)
        self.bListAccounts.setGeometry(QtCore.QRect(670, 0, 121, 24))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.bListAccounts.setFont(font)
        self.bListAccounts.setObjectName("bListAccounts")
        AccInFolderListWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AccInFolderListWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        AccInFolderListWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AccInFolderListWindow)
        self.statusbar.setObjectName("statusbar")
        AccInFolderListWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AccInFolderListWindow)
        QtCore.QMetaObject.connectSlotsByName(AccInFolderListWindow)

    def retranslateUi(self, AccInFolderListWindow):
        _translate = QtCore.QCoreApplication.translate
        AccInFolderListWindow.setWindowTitle(_translate("AccInFolderListWindow", "Acc In Folder List"))
        self.FolderNameLabel.setText(_translate("AccInFolderListWindow", "Folder To List:"))
        self.bListAccounts.setText(_translate("AccInFolderListWindow", "List Accounts"))
