# Form implementation generated from reading ui file 'AccFoldersListWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_AccFolderListWindow(object):
    def setupUi(self, AccFolderListWindow):
        AccFolderListWindow.setObjectName("AccFolderListWindow")
        AccFolderListWindow.resize(802, 359)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        AccFolderListWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(AccFolderListWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.AccFolderListText = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.AccFolderListText.setEnabled(True)
        self.AccFolderListText.setGeometry(QtCore.QRect(10, 30, 781, 271))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.AccFolderListText.setFont(font)
        self.AccFolderListText.setReadOnly(True)
        self.AccFolderListText.setObjectName("AccFolderListText")
        self.bRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.bRefresh.setGeometry(QtCore.QRect(704, 0, 81, 24))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(True)
        self.bRefresh.setFont(font)
        self.bRefresh.setObjectName("bRefresh")
        AccFolderListWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AccFolderListWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 22))
        self.menubar.setObjectName("menubar")
        AccFolderListWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AccFolderListWindow)
        self.statusbar.setObjectName("statusbar")
        AccFolderListWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AccFolderListWindow)
        QtCore.QMetaObject.connectSlotsByName(AccFolderListWindow)

    def retranslateUi(self, AccFolderListWindow):
        _translate = QtCore.QCoreApplication.translate
        AccFolderListWindow.setWindowTitle(_translate("AccFolderListWindow", "Acc Folders List"))
        self.bRefresh.setText(_translate("AccFolderListWindow", "Refresh"))