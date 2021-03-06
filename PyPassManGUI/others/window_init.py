# This file contain all the classes for every window in order to save up lines in the main files
from PyQt6.QtCore import Qt

from window_python_files import (
    login_window,
    register_account_window,
    login_account_window,
    remove_account_window,
    locker_window,
    create_acc_folder_window,
    acc_folders_list_window,
    delete_acc_folder_window,
    add_acc_to_folder_window,
    acc_in_folder_list_window,
    remove_acc_in_folder_window,
    clear_acc_in_folder_window,
    generate_strong_pass_window,
    style_manager_window,
    change_style_window,
    add_style_window,
)
from others import stylesheets
from PyQt6 import QtWidgets

current_style = stylesheets.load_current_style()


class LoginWindow(QtWidgets.QMainWindow, login_window.Ui_LoginWindow):
    """
    Initializes the "Login" window.
    """

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        LoginWindow.setStyleSheet(self, current_style)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setupUi(self)


class RegisterAccountWindow(
    QtWidgets.QMainWindow, register_account_window.Ui_RegisterAccountWindow
):
    """
    Initializes the "RegisterAccount" window.
    """

    def __init__(self, parent=None):
        super(RegisterAccountWindow, self).__init__(parent)
        RegisterAccountWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class LoginAccountWindow(
    QtWidgets.QMainWindow, login_account_window.Ui_LoginAccountWindow
):
    """
    Initializes the "LoginAccount" window.
    """

    def __init__(self, parent=None):
        super(LoginAccountWindow, self).__init__(parent)
        LoginAccountWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class RemoveAccountWindow(
    QtWidgets.QMainWindow, remove_account_window.Ui_RemoveAccountWindow
):
    """
    Initializes the "RemoveAccount" window.
    """

    def __init__(self, parent=None):
        super(RemoveAccountWindow, self).__init__(parent)
        RemoveAccountWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class LockerWindow(QtWidgets.QMainWindow, locker_window.Ui_LockerWindow):
    """
    Initializes the "Locker" window.
    """

    def __init__(self, parent=None):
        super(LockerWindow, self).__init__(parent)
        LockerWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class CreateAccFolderWindow(
    QtWidgets.QMainWindow, create_acc_folder_window.Ui_CreateAccFolderWindow
):
    """
    Initializes the "CreateAccFolder" window.
    """

    def __init__(self, parent=None):
        super(CreateAccFolderWindow, self).__init__(parent)
        CreateAccFolderWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class AccFolderListWindow(
    QtWidgets.QMainWindow, acc_folders_list_window.Ui_AccFolderListWindow
):
    """
    Initializes the "AccFolderList" window.
    """

    def __init__(self, parent=None):
        super(AccFolderListWindow, self).__init__(parent)
        AccFolderListWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class DeleteAccFolderWindow(
    QtWidgets.QMainWindow, delete_acc_folder_window.Ui_DeleteAccFolderWindow
):
    """
    Initializes the "DeleteAccFolder" window.
    """

    def __init__(self, parent=None):
        super(DeleteAccFolderWindow, self).__init__(parent)
        DeleteAccFolderWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class AddAccToFolderWindow(
    QtWidgets.QMainWindow, add_acc_to_folder_window.Ui_AddAccToFolderWindow
):
    """
    Initializes the "AddAccToFolder" window.
    """

    def __init__(self, parent=None):
        super(AddAccToFolderWindow, self).__init__(parent)
        AddAccToFolderWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class AccInFolderListWindow(
    QtWidgets.QMainWindow, acc_in_folder_list_window.Ui_AccInFolderListWindow
):
    """
    Initializes the "AccInFolderList" window.
    """

    def __init__(self, parent=None):
        super(AccInFolderListWindow, self).__init__(parent)
        AccInFolderListWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class RemoveAccInFolderWindow(
    QtWidgets.QMainWindow, remove_acc_in_folder_window.Ui_RemoveAccInFolderWindow
):
    """
    Initializes the "RemoveAccInFolder" window.
    """

    def __init__(self, parent=None):
        super(RemoveAccInFolderWindow, self).__init__(parent)
        RemoveAccInFolderWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class ClearAccInFolderWindow(
    QtWidgets.QMainWindow, clear_acc_in_folder_window.Ui_ClearAccInFolderWindow
):
    """
    Initializes the "ClearAccInFolder" window.
    """

    def __init__(self, parent=None):
        super(ClearAccInFolderWindow, self).__init__(parent)
        ClearAccInFolderWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class GenerateStrongPasswordWindow(
    QtWidgets.QMainWindow, generate_strong_pass_window.Ui_GenerateStrongPassWindow
):
    """
    Initializes the "GenerateStrongPassword" window.
    """

    def __init__(self, parent=None):
        super(GenerateStrongPasswordWindow, self).__init__(parent)
        GenerateStrongPasswordWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class StyleManagerWindow(
    QtWidgets.QMainWindow, style_manager_window.Ui_StyleManagerWindow
):
    """
    Initializes the "StyleManager" window.
    """

    def __init__(self, parent=None):
        super(StyleManagerWindow, self).__init__(parent)
        StyleManagerWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class ChangeStyleWindow(
    QtWidgets.QMainWindow, change_style_window.Ui_ChangeStyleWindow
):
    """
    Initializes the "ChangeStyle" window.
    """

    def __init__(self, parent=None):
        super(ChangeStyleWindow, self).__init__(parent)
        ChangeStyleWindow.setStyleSheet(self, current_style)
        self.setupUi(self)


class AddStyleWindow(QtWidgets.QMainWindow, add_style_window.Ui_AddStyleWindow):
    """
    Initializes the "AddStyle" window.
    """

    def __init__(self, parent=None):
        super(AddStyleWindow, self).__init__(parent)
        AddStyleWindow.setStyleSheet(self, current_style)
        self.setupUi(self)
