# Form implementation generated from reading ui file 'StyleManagerWindow.ui'
#
# Created by: PyQt6 UI code generator 6.0.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_StyleManagerWindow(object):
    def setupUi(self, StyleManagerWindow):
        StyleManagerWindow.setObjectName("StyleManagerWindow")
        StyleManagerWindow.resize(332, 113)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        StyleManagerWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:/Downloads/SSH-Keys.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        StyleManagerWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(StyleManagerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bChangeStyle = QtWidgets.QPushButton(self.centralwidget)
        self.bChangeStyle.setGeometry(QtCore.QRect(10, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(16)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.bChangeStyle.setFont(font)
        self.bChangeStyle.setObjectName("bChangeStyle")
        self.bAddStyle = QtWidgets.QPushButton(self.centralwidget)
        self.bAddStyle.setGeometry(QtCore.QRect(170, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(16)
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.bAddStyle.setFont(font)
        self.bAddStyle.setObjectName("bAddStyle")
        StyleManagerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StyleManagerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 332, 22))
        self.menubar.setObjectName("menubar")
        StyleManagerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StyleManagerWindow)
        self.statusbar.setObjectName("statusbar")
        StyleManagerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StyleManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(StyleManagerWindow)

    def retranslateUi(self, StyleManagerWindow):
        _translate = QtCore.QCoreApplication.translate
        StyleManagerWindow.setWindowTitle(_translate("StyleManagerWindow", "Style Manager"))
        self.bChangeStyle.setText(_translate("StyleManagerWindow", "Change Style"))
        self.bChangeStyle.setShortcut(_translate("StyleManagerWindow", "2"))
        self.bAddStyle.setText(_translate("StyleManagerWindow", "Add Style"))
        self.bAddStyle.setShortcut(_translate("StyleManagerWindow", "3"))
