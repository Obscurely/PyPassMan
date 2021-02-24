import re
import requests
import json
from others import aes
from others import locker_functions
from others import accounts
from others import window_init
from PyQt6.QtWidgets import QMessageBox

# error vars
unknown_error = 'An unknown error occurred. Close the app and try again!'
banned_chars = 'banned chars in text'
banned_chars_error = 'Usernames can\'t contain any of the following characters:\n\t\t\\ / : * ? " < > |'
app_acc_dir_not_found_error = 'PyPassMan accounts dir does not exist'
user_acc_dir_not_found_error = 'user accounts dir does not exist'
user_acc_folder_not_found_error = 'user acc folder does not exist'
app_dir_error = 'The directory with the accounts for the app was not found!' \
                ' If after a restart it does not work reinstalling the application' \
                ' might be the only solution.'
user_acc_dir_error = 'The user acc directory was not found! This means that there is no data ' \
                     'about any accounts! Reinstalling the program might be the only solution.'

# other vars
config_file = 'config.json'


def check_first_run():
    with open(config_file, 'r') as f:
        metadata = json.load(f)

    if metadata['first_run'] == 'Yes':
        aes.gen_keys()
        metadata['first_run'] = 'No'
        with open(config_file, 'w') as f:
            json.dump(metadata, f, indent=4)


def check_version():
    with open(config_file, 'r') as f:
        metadata = json.load(f)

    metadata_url = metadata['metadata_url']

    content = requests.get(metadata_url).text
    pattern = re.compile(r'(?<=-=-=&gt;&gt;).*?(?=&lt;=-=-)')
    latest_version = pattern.findall(content)[0]
    current_version = metadata['version']

    if latest_version != current_version:
        error = QMessageBox()
        error.setWindowTitle('Update')
        error.setText('There is an update available, version: ' + latest_version + '\n'
                      + 'You can download it with the installer or from github and read the patch notes there:\n'
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
                added_account.setWindowTitle('Success')
                added_account.setText('Successfully created account ' + username_input + '! You can now Login')
                added_account.exec()
                register_account_form.close()
            elif response == 'username exists':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('An account with username ' + username_input
                              + ' already exists. Try again with a different username!')
                error.exec()
                register_account_form.UsernameInput.clear()
            elif response == 'username empty':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('Username can\'t be empty')
                error.exec()
            elif response == banned_chars:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(banned_chars_error)
                error.exec()
                register_account_form.UsernameInput.clear()
            elif response == app_acc_dir_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(app_dir_error)
                error.exec()
            elif response == user_acc_dir_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(user_acc_dir_error)
                error.exec()
            elif response == 'acc folder already exists':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('A folder with user is already present in the app! Any data this '
                              'folder had was not changed, if you did not want this you can '
                              'delete the acc and try recreate it.')
                error.exec()
            else:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(unknown_error)
                error.exec()
                register_account_form.close()
        elif password_input != password_again_input:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('The passwords don\'t match! Try again')
            error.exec()
            register_account_form.PasswordInput.clear()
            register_account_form.PasswordAgainInput.clear()
        elif len(password_input) < 4:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('The password has to be 4 or more characters')
            error.exec()
            register_account_form.PasswordInput.clear()
            register_account_form.PasswordAgainInput.clear()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
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
            logged.setWindowTitle('Success')
            logged.setText('Successfully logged into account ' + username_input + '.')
            logged.exec()
            login_account_form.close()
            after_login(locker_form, username_input)
        elif response == 'account not exist':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('An account with username ' + username_input + ' does not exist. Try again!')
            error.exec()
            login_account_form.UsernameInput.clear()
        elif response == 'incorrect password':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Incorrect password!')
            error.exec()
            login_account_form.PasswordInput.clear()
        elif response == app_acc_dir_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(app_dir_error)
            error.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
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
                added_account.setWindowTitle('Success')
                added_account.setText('Successfully removed account ' + username_input + '!')
                added_account.exec()
                remove_account_form.close()
            elif response == 'account with this username not exist':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('An account with username ' + username_input + ' does not exist. Try again!')
                error.exec()
                remove_account_form.UsernameInput.clear()
            elif response == 'password incorrect':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('The password is incorrect. Try again!')
                error.exec()
                remove_account_form.PasswordInput.clear()
                remove_account_form.PasswordAgainInput.clear()
            elif response == app_acc_dir_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(app_dir_error)
                error.exec()
            elif response == user_acc_dir_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(user_acc_dir_error)
                error.exec()
            elif response == 'user folder was not found':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('This user folder was not found, we just deleted it\'s metadata '
                              'and everything should be fine in theory!')
                error.exec()
            else:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(unknown_error)
                error.exec()
                remove_account_form.close()

        elif password_input != password_again_input:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('The passwords don\'t match! Try again')
            error.exec()
            remove_account_form.PasswordInput.clear()
            remove_account_form.PasswordAgainInput.clear()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
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
