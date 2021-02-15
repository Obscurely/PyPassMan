from window_python_files import login_window
from window_python_files import register_account_window
from window_python_files import login_account_window
from window_python_files import remove_account_window
from window_python_files import locker_window
from window_python_files import create_acc_folder_window
from window_python_files import acc_folders_list_window
from window_python_files import delete_acc_folder_window
from window_python_files import add_acc_to_folder_window
from window_python_files import acc_in_folder_list_window
from window_python_files import remove_acc_in_folder_window
from window_python_files import clear_acc_in_folder_window
from window_python_files import generate_strong_pass_window
from PyQt6 import QtWidgets


class LoginWindow(QtWidgets.QMainWindow, login_window.Ui_LoginWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)


class RegisterAccountWindow(QtWidgets.QMainWindow, register_account_window.Ui_RegisterAccountWindow):
    def __init__(self, parent=None):
        super(RegisterAccountWindow, self).__init__(parent)
        self.setupUi(self)


class LoginAccountWindow(QtWidgets.QMainWindow, login_account_window.Ui_LoginAccountWindow):
    def __init__(self, parent=None):
        super(LoginAccountWindow, self).__init__(parent)
        self.setupUi(self)


class RemoveAccountWindow(QtWidgets.QMainWindow, remove_account_window.Ui_RemoveAccountWindow):
    def __init__(self, parent=None):
        super(RemoveAccountWindow, self).__init__(parent)
        self.setupUi(self)


class LockerWindow(QtWidgets.QMainWindow, locker_window.Ui_LockerWindow):
    def __init__(self, parent=None):
        super(LockerWindow, self).__init__(parent)
        self.setupUi(self)


class CreateAccFolderWindow(QtWidgets.QMainWindow, create_acc_folder_window.Ui_CreateAccFolderWindow):
    def __init__(self, parent=None):
        super(CreateAccFolderWindow, self).__init__(parent)
        self.setupUi(self)


class AccFolderListWindow(QtWidgets.QMainWindow, acc_folders_list_window.Ui_AccFolderListWindow):
    def __init__(self, parent=None):
        super(AccFolderListWindow, self).__init__(parent)
        self.setupUi(self)


class DeleteAccFolderWindow(QtWidgets.QMainWindow, delete_acc_folder_window.Ui_DeleteAccFolderWindow):
    def __init__(self, parent=None):
        super(DeleteAccFolderWindow, self).__init__(parent)
        self.setupUi(self)


class AddAccToFolderWindow(QtWidgets.QMainWindow, add_acc_to_folder_window.Ui_AddAccToFolderWindow):
    def __init__(self, parent=None):
        super(AddAccToFolderWindow, self).__init__(parent)
        self.setupUi(self)


class AccInFolderListWindow(QtWidgets.QMainWindow, acc_in_folder_list_window.Ui_AccInFolderListWindow):
    def __init__(self, parent=None):
        super(AccInFolderListWindow, self).__init__(parent)
        self.setupUi(self)


class RemoveAccInFolderWindow(QtWidgets.QMainWindow, remove_acc_in_folder_window.Ui_RemoveAccInFolderWindow):
    def __init__(self, parent=None):
        super(RemoveAccInFolderWindow, self).__init__(parent)
        self.setupUi(self)


class ClearAccInFolderWindow(QtWidgets.QMainWindow, clear_acc_in_folder_window.Ui_ClearAccInFolderWindow):
    def __init__(self, parent=None):
        super(ClearAccInFolderWindow, self).__init__(parent)
        self.setupUi(self)


class GenerateStrongPasswordWindow(QtWidgets.QMainWindow, generate_strong_pass_window.Ui_GenerateStrongPassWindow):
    def __init__(self, parent=None):
        super(GenerateStrongPasswordWindow, self).__init__(parent)
        self.setupUi(self)
