# Form implementation generated from reading ui file 'RemoveAccountWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RemoveAccountWindow(object):
    def setupUi(self, RemoveAccountWindow):
        RemoveAccountWindow.setObjectName("RemoveAccountWindow")
        RemoveAccountWindow.resize(611, 202)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        RemoveAccountWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(RemoveAccountWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UsernameLabel = QtWidgets.QLabel(self.centralwidget)
        self.UsernameLabel.setGeometry(QtCore.QRect(10, 0, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(20)
        self.UsernameLabel.setFont(font)
        self.UsernameLabel.setObjectName("UsernameLabel")
        self.PasswordLabel = QtWidgets.QLabel(self.centralwidget)
        self.PasswordLabel.setGeometry(QtCore.QRect(10, 30, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(20)
        self.PasswordLabel.setFont(font)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.PasswordAgainLabel = QtWidgets.QLabel(self.centralwidget)
        self.PasswordAgainLabel.setGeometry(QtCore.QRect(10, 60, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(20)
        self.PasswordAgainLabel.setFont(font)
        self.PasswordAgainLabel.setObjectName("PasswordAgainLabel")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(210, 0, 20, 101))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.UsernameInput = QtWidgets.QLineEdit(self.centralwidget)
        self.UsernameInput.setGeometry(QtCore.QRect(230, 11, 361, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.UsernameInput.setFont(font)
        self.UsernameInput.setObjectName("UsernameInput")
        self.PasswordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordInput.setGeometry(QtCore.QRect(230, 40, 361, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.PasswordInput.setFont(font)
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.PasswordInput.setObjectName("PasswordInput")
        self.PasswordAgainInput = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordAgainInput.setGeometry(QtCore.QRect(230, 70, 361, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.PasswordAgainInput.setFont(font)
        self.PasswordAgainInput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.PasswordAgainInput.setObjectName("PasswordAgainInput")
        self.bRemoveAccount = QtWidgets.QPushButton(self.centralwidget)
        self.bRemoveAccount.setGeometry(QtCore.QRect(350, 110, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        font.setBold(True)
        self.bRemoveAccount.setFont(font)
        self.bRemoveAccount.setObjectName("bRemoveAccount")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(590, 0, 21, 101))
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(7, 93, 591, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        RemoveAccountWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RemoveAccountWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 611, 24))
        self.menubar.setObjectName("menubar")
        RemoveAccountWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RemoveAccountWindow)
        self.statusbar.setObjectName("statusbar")
        RemoveAccountWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RemoveAccountWindow)
        QtCore.QMetaObject.connectSlotsByName(RemoveAccountWindow)

    def retranslateUi(self, RemoveAccountWindow):
        _translate = QtCore.QCoreApplication.translate
        RemoveAccountWindow.setWindowTitle(_translate("RemoveAccountWindow", "Remove Account"))
        self.UsernameLabel.setText(_translate("RemoveAccountWindow", "Username:"))
        self.PasswordLabel.setText(_translate("RemoveAccountWindow", "Password:"))
        self.PasswordAgainLabel.setText(_translate("RemoveAccountWindow", "Password Again:"))
        self.UsernameInput.setWhatsThis(_translate("RemoveAccountWindow", "Test"))
        self.bRemoveAccount.setText(_translate("RemoveAccountWindow", "Remove \n"
"Account"))
        self.bRemoveAccount.setShortcut(_translate("RemoveAccountWindow", "Return"))
