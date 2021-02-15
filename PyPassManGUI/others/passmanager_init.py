from others import accounts
from others import window_init
from PyQt6.QtWidgets import QMessageBox


def register():
    register_account_form = window_init.RegisterAccountWindow()
    register_account_form.show()

    def validate_add_account():
        username_input = register_account_form.UsernameInput.text()
        password_input = register_account_form.PasswordInput.text()
        password_again_input = register_account_form.PasswordAgainInput.text()

        if password_input == password_again_input:
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
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()
                register_account_form.close()
        elif password_input != password_again_input:
            error = QMessageBox()
            error.setText('The passwords don\'t match! Try again')
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
            error.setText('An account with username ' + username_input + ' doesn\'t exist. Try again!')
            error.exec()
        else:
            error = QMessageBox()
            error.setText('An unknown error occurred. Close the app and try again!')
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
                error.setText('Accounts with username ' + username_input + ' doesn\'t exist. Try again!')
                error.exec()
            elif response == 'password incorrect':
                error = QMessageBox()
                error.setText('The password is incorrect. Try again!')
                error.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
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
    acc_folders_list_form = window_init.AccFolderListWindow()
    locker_form.show()

    def create_acc_folder():
        create_acc_folder_form = window_init.CreateAccFolderWindow()
        create_acc_folder_form.show()

        def validate_creation():
            folder_name = create_acc_folder_form.FolderNameInput.text()
            response = accounts.create_acc_folder(username, folder_name)

            if response == 'folder already exists':
                error = QMessageBox()
                error.setText('Acc Folder with name ' + folder_name + ' already exists, try a different name!')
                error.exec()
            elif response == 'folder created':
                created = QMessageBox()
                created.setText('Acc Folder ' + folder_name + ' was created successfully!')
                created.exec()
            elif response == 'folder name can not be empty':
                error = QMessageBox()
                error.setText('Folder name can not be empty')
                error.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        create_acc_folder_form.bCreateAccFolder.clicked.connect(validate_creation)

    def list_acc_folders():
        acc_folders_list_form.show()
        folder_list = accounts.get_acc_folders(username)
        if folder_list != '':
            acc_folders_list_form.AccFolderListText.setPlainText(folder_list)
        else:
            acc_folders_list_form.AccFolderListText.setPlainText('You don\'t have any account folders.')

    def delete_acc_folder():
        delete_acc_folder_form = window_init.DeleteAccFolderWindow()
        delete_acc_folder_form.show()

        def validate_deletion():
            folder_name = delete_acc_folder_form.FolderNameInput.text()
            response = accounts.remove_acc_folder(username, folder_name)

            if response == 'folder not found':
                error = QMessageBox()
                error.setText('Acc Folder with name ' + folder_name + ' doesn\'t exist, try a different one.')
                error.exec()
            elif response == 'deleted acc folder':
                deleted = QMessageBox()
                deleted.setText('Acc Folder with name ' + folder_name + ' was successfully deleted!')
                deleted.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        delete_acc_folder_form.bDeleteAccFolder.clicked.connect(validate_deletion)

    def add_acc_to_folder():
        add_acc_to_folder_form = window_init.AddAccToFolderWindow()
        add_acc_to_folder_form.show()

        def validate_acc_add():
            folder_name = add_acc_to_folder_form.FolderNameInput.text()
            label = add_acc_to_folder_form.LabelInput.text()
            acc_username = add_acc_to_folder_form.UsernameInput.text()
            password = add_acc_to_folder_form.PasswordInput.text()
            password_again = add_acc_to_folder_form.PasswordAgainInput.text()

            if password == password_again:
                if label == '':
                    label = '0'
                    response = accounts.add_acc_to_folder(username, label, folder_name, acc_username, password)
                else:
                    response = accounts.add_acc_to_folder(username, label, folder_name, acc_username, password)

                if response == 'folder not found':
                    error = QMessageBox()
                    error.setText('Folder not found!')
                    error.exec()
                elif response == 'added acc to folder':
                    acc_added = QMessageBox()
                    acc_added.setText('Account was added successfully!')
                    acc_added.exec()
                elif response == 'folder name can not be empty':
                    error = QMessageBox()
                    error.setText('Folder name can\'t be empty!')
                    error.exec()
                else:
                    error = QMessageBox()
                    error.setText('An unknown error occurred. Close the app and try again!')
                    error.exec()

            elif password == password_again:
                error = QMessageBox()
                error.setText('Passwords do not match!')
                error.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        add_acc_to_folder_form.bAddAccToFolder.clicked.connect(validate_acc_add)

    def list_acc_in_folder():
        acc_in_folder_list_form = window_init.AccInFolderListWindow()
        acc_in_folder_list_form.show()

        def validate_list_acc():
            folder_name = acc_in_folder_list_form.FolderNameInput.text()

            response = accounts.get_acc_in_folder(username, folder_name)

            if response == 'folder not found':
                error = QMessageBox()
                error.setText('Folder not found!')
                error.exec()
            elif isinstance(response, str):
                acc_in_folder_list_form.AccInFolderListText.setPlainText(response)
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        acc_in_folder_list_form.bListAccounts.clicked.connect(validate_list_acc)

    def remove_acc_in_folder():
        remove_acc_in_folder_form = window_init.RemoveAccInFolderWindow()
        remove_acc_in_folder_form.show()

        def validate_remove_acc():
            folder_name = remove_acc_in_folder_form.FolderNameInput.text()
            acc_username = remove_acc_in_folder_form.UsernameInput.text()
            acc_number = remove_acc_in_folder_form.NumberInput.text()

            response = accounts.remove_acc_in_folder(username, folder_name, acc_number, acc_username)
            if response == 'folder not found':
                error = QMessageBox()
                error.setText('Folder not found!')
                error.exec()
            elif response == 'account not found':
                error = QMessageBox()
                error.setText('Account not found!')
                error.exec()
            elif response == 'account removed':
                removed_acc = QMessageBox()
                removed_acc.setText('Account successfully removed!')
                removed_acc.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        remove_acc_in_folder_form.bRemoveAccInFolder.clicked.connect(validate_remove_acc)

    def clear_acc_in_folder():
        clear_acc_in_folder_form = window_init.ClearAccInFolderWindow()
        clear_acc_in_folder_form.show()

        def validate_clear_acc():
            folder_name = clear_acc_in_folder_form.FolderNameInput.text()

            response = accounts.clear_acc_folder(username, folder_name)
            if response == 'folder not found':
                error = QMessageBox()
                error.setText('Folder not found!')
                error.exec()
            elif response == 'acc folder cleared':
                cleared_acc = QMessageBox()
                cleared_acc.setText('Accounts folder successfully cleared!')
                cleared_acc.exec()
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        clear_acc_in_folder_form.bClearAccInFolder.clicked.connect(validate_clear_acc)

    def generate_strong_pass():
        generate_strong_pass_form = window_init.GenerateStrongPasswordWindow()
        generate_strong_pass_form.show()

        def generate():
            chars_number = generate_strong_pass_form.NumberOfCharsInput.text()

            response = accounts.pass_gen(chars_number)
            if response == 'invalid length':
                error = QMessageBox()
                error.setText('Invalid length!')
                error.exec()
            elif isinstance(response, str):
                generate_strong_pass_form.OutputText.setText(response)
            else:
                error = QMessageBox()
                error.setText('An unknown error occurred. Close the app and try again!')
                error.exec()

        generate_strong_pass_form.bGenerateStrongPass.clicked.connect(generate)

    def backup_acc():
        accounts.backup(username)

        backup = QMessageBox()
        backup.setText('Successfully backed up the accounts to backup.txt (on desktop)')
        backup.exec()

    def restore_acc():
        response = accounts.restore(username)
        if response == 'desktop no backup.txt':
            error = QMessageBox()
            error.setText('There is no ' + username + 'backup.txt file on the desktop')
            error.exec()
        else:
            restored = QMessageBox()
            restored.setText('Successfully restored all accounts!')
            restored.exec()

    locker_form.bCreateAccFolder.clicked.connect(create_acc_folder)
    locker_form.bListAccFolder.clicked.connect(list_acc_folders)
    locker_form.bRemoveAccFolder.clicked.connect(delete_acc_folder)
    locker_form.bAddAccToFolder.clicked.connect(add_acc_to_folder)
    locker_form.bGetAccInFolder.clicked.connect(list_acc_in_folder)
    locker_form.bRemoveAccInFolder.clicked.connect(remove_acc_in_folder)
    locker_form.bClearAccInFolder.clicked.connect(clear_acc_in_folder)
    locker_form.bGeneratePass.clicked.connect(generate_strong_pass)
    locker_form.bLogout.clicked.connect(locker_form.close)
    locker_form.bBackup.clicked.connect(backup_acc)
    locker_form.bRestore.clicked.connect(restore_acc)
