# Form implementation generated from reading ui file 'CreateAccFolderWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CreateAccFolderWindow(object):
    def setupUi(self, CreateAccFolderWindow):
        CreateAccFolderWindow.setObjectName("CreateAccFolderWindow")
        CreateAccFolderWindow.resize(342, 108)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        CreateAccFolderWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(CreateAccFolderWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.FolderNameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.FolderNameInput.setGeometry(QtCore.QRect(50, 10, 281, 22))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.FolderNameInput.setFont(font)
        self.FolderNameInput.setObjectName("FolderNameInput")
        self.bCreateAccFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bCreateAccFolder.setGeometry(QtCore.QRect(110, 40, 121, 24))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        self.bCreateAccFolder.setFont(font)
        self.bCreateAccFolder.setObjectName("bCreateAccFolder")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        CreateAccFolderWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CreateAccFolderWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 342, 22))
        self.menubar.setObjectName("menubar")
        CreateAccFolderWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CreateAccFolderWindow)
        self.statusbar.setObjectName("statusbar")
        CreateAccFolderWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CreateAccFolderWindow)
        QtCore.QMetaObject.connectSlotsByName(CreateAccFolderWindow)

    def retranslateUi(self, CreateAccFolderWindow):
        _translate = QtCore.QCoreApplication.translate
        CreateAccFolderWindow.setWindowTitle(_translate("CreateAccFolderWindow", "Create Acc Folder"))
        self.bCreateAccFolder.setText(_translate("CreateAccFolderWindow", "Create Acc Folder"))
        self.bCreateAccFolder.setShortcut(_translate("CreateAccFolderWindow", "Return"))
        self.label.setText(_translate("CreateAccFolderWindow", "Name:"))
