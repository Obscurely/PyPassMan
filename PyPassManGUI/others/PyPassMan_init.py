import re
import requests
from others import locker_functions
from others import accounts
from others import window_init
from PyQt6.QtWidgets import QMessageBox

# error vars
unknown_error = 'An unknown error occurred. Close the app and try again!'


def check_version():
    content = requests.get('https://pastebin.com/f077vm8L').text
    pattern = re.compile(r'(?<=-=-=&gt;&gt;).*?(?=&lt;=-=-)')
    latest_version = pattern.findall(content)[0]

    with open('version.txt', 'r') as f:
        current_version = f.read()

    if latest_version != current_version:
        error = QMessageBox()
        error.setText('There is an update available, version: ' + latest_version + '\n'
                      + 'You can download it with the installer or from github and you can read patch notes at:\n'
                      + 'https://github.com/Obscurely/PyPassMan/releases')
        error.exec()


def register():
    register_account_form = window_init.RegisterAccountWindow()
    register_account_form.show()

    def validate_add_account():
        username_input = register_account_form.UsernameInput.text()
        password_input = register_account_form.PasswordInput.text()
        password_again_input = register_account_form.PasswordAgainInput.text()

        if password_input == password_again_input and len(password_input) > 3:
            response = accounts.register_acc(username_input, password_input)

            if response == 'created account':
                added_account = QMessageBox()
                added_account.setText('Successfully created account ' + username_input + '! You can now Login')
                added_account.exec()
                register_account_form.close()
            elif response == 'username exists':
                error = QMessageBox()
                error.setText('An account with username ' + username_input
                              + ' already exists. Try again with a different username!')
                error.exec()
            elif response == 'username empty':
                error = QMessageBox()
                error.setText('Username can\'t be empty')
                error.exec()
            else:
                error = QMessageBox()
                error.setText(unknown_error)
                error.exec()
                register_account_form.close()
        elif password_input != password_again_input:
            error = QMessageBox()
            error.setText('The passwords don\'t match! Try again')
            error.exec()
        elif len(password_input) < 4:
            error = QMessageBox()
            error.setText('The password has to be 4 or more characters')
            error.exec()
        else:
            error = QMessageBox()
            error.setText('An unknown error occurred! Restart app for safety!')
            error.exec()
            register_account_form.close()

    register_account_form.bRegisterAccount.clicked.connect(validate_add_account)


def login():
    login_account_form = window_init.LoginAccountWindow()
    locker_form = window_init.LockerWindow()
    login_account_form.show()

    def validate_login():
        username_input = login_account_form.UsernameInput.text()
        password_input = login_account_form.PasswordInput.text()
        response = accounts.login(username_input, password_input)

        if response == 'login successful':
            logged = QMessageBox()
            logged.setText('Successfully logged into account ' + username_input + '.')
            logged.exec()
            login_account_form.close()
            after_login(locker_form, username_input)
        elif response == 'account not exist':
            error = QMessageBox()
            error.setText('An account with username ' + username_input + ' does not exist. Try again!')
            error.exec()
        else:
            error = QMessageBox()
            error.setText(unknown_error)
            error.exec()
            login_account_form.close()

    login_account_form.bLogin.clicked.connect(validate_login)


def remove_acc():
    remove_account_form = window_init.RemoveAccountWindow()
    remove_account_form.show()

    def validate_remove_acc():
        username_input = remove_account_form.UsernameInput.text()
        password_input = remove_account_form.PasswordInput.text()
        password_again_input = remove_account_form.PasswordAgainInput.text()

        if password_input == password_again_input:
            response = accounts.remove_acc(username_input, password_input)

            if response == 'account deleted':
                added_account = QMessageBox()
                added_account.setText('Successfully removed account ' + username_input + '!')
                added_account.exec()
                remove_account_form.close()
            elif response == 'account with this username not exist':
                error = QMessageBox()
                error.setText('An account with username ' + username_input + ' does not exist. Try again!')
                error.exec()
            elif response == 'password incorrect':
                error = QMessageBox()
                error.setText('The password is incorrect. Try again!')
                error.exec()
            else:
                error = QMessageBox()
                error.setText(unknown_error)
                error.exec()
                remove_account_form.close()

        elif password_input != password_again_input:
            error = QMessageBox()
            error.setText('The passwords don\'t match! Try again')
            error.exec()
        else:
            error = QMessageBox()
            error.setText('An unknown error occurred! Restart app for safety!')
            error.exec()
            remove_account_form.close()

    remove_account_form.bRemoveAccount.clicked.connect(validate_remove_acc)


def after_login(locker_form, username):
    locker_form.show()

    locker_form.bCreateAccFolder.clicked.connect(lambda: locker_functions.create_acc_folder(username))
    locker_form.bListAccFolder.clicked.connect(lambda: locker_functions.list_acc_folders(username))
    locker_form.bRemoveAccFolder.clicked.connect(lambda: locker_functions.delete_acc_folder(username))
    locker_form.bAddAccToFolder.clicked.connect(lambda: locker_functions.add_acc_to_folder(username))
    locker_form.bGetAccInFolder.clicked.connect(lambda: locker_functions.list_acc_in_folder(username))
    locker_form.bRemoveAccInFolder.clicked.connect(lambda: locker_functions.remove_acc_in_folder(username))
    locker_form.bClearAccInFolder.clicked.connect(lambda: locker_functions.clear_acc_in_folder(username))
    locker_form.bGeneratePass.clicked.connect(locker_functions.generate_strong_pass)
    locker_form.bBackup.clicked.connect(lambda: locker_functions.backup_acc(username))
    locker_form.bRestore.clicked.connect(lambda: locker_functions.restore_acc(username))
    locker_form.bLogout.clicked.connect(locker_form.close)
