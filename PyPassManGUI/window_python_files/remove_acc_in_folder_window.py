# Form implementation generated from reading ui file 'RemoveAccInFolderWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RemoveAccInFolderWindow(object):
    def setupUi(self, RemoveAccInFolderWindow):
        RemoveAccInFolderWindow.setObjectName("RemoveAccInFolderWindow")
        RemoveAccInFolderWindow.resize(544, 138)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        RemoveAccInFolderWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(RemoveAccInFolderWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bRemoveAccInFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bRemoveAccInFolder.setGeometry(QtCore.QRect(200, 70, 151, 24))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        self.bRemoveAccInFolder.setFont(font)
        self.bRemoveAccInFolder.setObjectName("bRemoveAccInFolder")
        self.FolderNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FolderNameLabel.setGeometry(QtCore.QRect(10, 10, 111, 20))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.FolderNameLabel.setFont(font)
        self.FolderNameLabel.setObjectName("FolderNameLabel")
        self.AccountsLabel = QtWidgets.QLabel(self.centralwidget)
        self.AccountsLabel.setGeometry(QtCore.QRect(10, 40, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.AccountsLabel.setFont(font)
        self.AccountsLabel.setObjectName("AccountsLabel")
        self.cbFolders = QtWidgets.QComboBox(self.centralwidget)
        self.cbFolders.setGeometry(QtCore.QRect(120, 10, 331, 22))
        self.cbFolders.setObjectName("cbFolders")
        self.bGetAcc = QtWidgets.QPushButton(self.centralwidget)
        self.bGetAcc.setGeometry(QtCore.QRect(460, 10, 71, 24))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        self.bGetAcc.setFont(font)
        self.bGetAcc.setObjectName("bGetAcc")
        self.cbAccounts = QtWidgets.QComboBox(self.centralwidget)
        self.cbAccounts.setGeometry(QtCore.QRect(120, 40, 411, 22))
        self.cbAccounts.setObjectName("cbAccounts")
        RemoveAccInFolderWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RemoveAccInFolderWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 544, 22))
        self.menubar.setObjectName("menubar")
        RemoveAccInFolderWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RemoveAccInFolderWindow)
        self.statusbar.setObjectName("statusbar")
        RemoveAccInFolderWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RemoveAccInFolderWindow)
        QtCore.QMetaObject.connectSlotsByName(RemoveAccInFolderWindow)

    def retranslateUi(self, RemoveAccInFolderWindow):
        _translate = QtCore.QCoreApplication.translate
        RemoveAccInFolderWindow.setWindowTitle(_translate("RemoveAccInFolderWindow", "Remove Acc In Folder"))
        self.bRemoveAccInFolder.setText(_translate("RemoveAccInFolderWindow", "Remove Acc In Folder"))
        self.bRemoveAccInFolder.setShortcut(_translate("RemoveAccInFolderWindow", "Return"))
        self.FolderNameLabel.setText(_translate("RemoveAccInFolderWindow", "Folder Name:"))
        self.AccountsLabel.setText(_translate("RemoveAccInFolderWindow", "Accounts:"))
        self.bGetAcc.setText(_translate("RemoveAccInFolderWindow", "Get Acc"))
