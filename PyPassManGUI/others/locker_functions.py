from others import accounts
from others import window_init
from PyQt6.QtWidgets import QMessageBox

# error vars
unknown_error = 'An unknown error occurred. Close the app and try again!'
folder_not_found_error = 'folder not found'
print_folder_not_found_error = 'Folder not found!'
banned_chars = 'banned chars in text'
banned_chars_error = 'A file name can\'t contain any of the following characters:\n\t\t\\ / : * ? " < > |'
app_acc_dir_not_found_error = 'PyPassMan accounts dir does not exist'
user_acc_dir_not_found_error = 'user accounts dir does not exist'
user_acc_folder_not_found_error = 'user acc folder does not exist'
app_dir_error = 'The directory with the accounts for the app was not found!' \
                ' If after a restart it does not work reinstalling the application' \
                ' might be the only solution.'
user_acc_dir_error = 'The user acc directory was not found! This means that there is no data ' \
                     'about any accounts! Reinstalling the program might be the only solution.'
user_acc_folder_error = 'The folder with this user data was not found! Removing and adding back ' \
                        'the account might be the only to fix this.'


def create_acc_folder(username):
    create_acc_folder_form = window_init.CreateAccFolderWindow()
    create_acc_folder_form.show()

    def validate_creation():
        folder_name = create_acc_folder_form.FolderNameInput.text()
        response = accounts.create_acc_folder(username, folder_name)

        if response == 'folder already exists':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Acc Folder with name ' + folder_name + ' already exists, try a different name!')
            error.exec()
            create_acc_folder_form.FolderNameInput.clear()
        elif response == 'folder created':
            created = QMessageBox()
            created.setWindowTitle('Success')
            created.setText('Acc Folder ' + folder_name + ' was created successfully!')
            created.exec()
        elif response == 'folder name can not be empty':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Folder name can not be empty')
            error.exec()
        elif response == banned_chars:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(banned_chars_error)
            error.exec()
            create_acc_folder_form.FolderNameInput.clear()
        elif response == user_acc_dir_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_dir_error)
            error.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            create_acc_folder_form.close()
            error.exec()

    create_acc_folder_form.bCreateAccFolder.clicked.connect(validate_creation)


def list_acc_folders(username):
    acc_folders_list_form = window_init.AccFolderListWindow()
    acc_folders_list_form.show()

    def get_folders():
        folder_list = accounts.get_acc_folders(username)
        if folder_list != '':
            acc_folders_list_form.AccFolderListText.setPlainText(folder_list)
        elif folder_list == user_acc_folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_folder_error)
            error.exec()
        else:
            acc_folders_list_form.AccFolderListText.setPlainText('You don\'t have any account folders.')
    get_folders()

    acc_folders_list_form.bRefresh.clicked.connect(get_folders)


def delete_acc_folder(username):
    delete_acc_folder_form = window_init.DeleteAccFolderWindow()
    delete_acc_folder_form.show()

    folder_list = accounts.get_acc_folders(username).split('/    ')
    for folder in folder_list:
        if folder != '':
            delete_acc_folder_form.cbFolders.addItem(folder)

    def validate_deletion():
        folder_name = delete_acc_folder_form.cbFolders.currentText()
        response = accounts.remove_acc_folder(username, folder_name)

        if response == folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Acc Folder with name ' + folder_name + ' does not exist, try a different one.')
            error.exec()
        elif response == 'deleted acc folder':
            deleted = QMessageBox()
            deleted.setWindowTitle('Success')
            deleted.setText('Acc Folder with name ' + folder_name + ' was successfully deleted!')
            deleted.exec()
        elif response == user_acc_folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_folder_error)
            error.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            delete_acc_folder_form.close()
            error.exec()

        delete_acc_folder_form.cbFolders.clear()
        new_folder_list = accounts.get_acc_folders(username).split('/    ')
        for new_folder in new_folder_list:
            if new_folder != '':
                delete_acc_folder_form.cbFolders.addItem(new_folder)

    delete_acc_folder_form.bDeleteAccFolder.clicked.connect(validate_deletion)


def add_acc_to_folder(username):
    add_acc_to_folder_form = window_init.AddAccToFolderWindow()
    add_acc_to_folder_form.show()

    folder_list = accounts.get_acc_folders(username).split('/    ')
    for folder in folder_list:
        if folder != '':
            add_acc_to_folder_form.cbFolders.addItem(folder)

    def validate_acc_add():
        folder_name = add_acc_to_folder_form.cbFolders.currentText()
        label = add_acc_to_folder_form.LabelInput.text()
        acc_username = add_acc_to_folder_form.UsernameInput.text()
        password = add_acc_to_folder_form.PasswordInput.text()
        password_again = add_acc_to_folder_form.PasswordAgainInput.text()

        if 'username: ' in acc_username:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Username can not contain "username: " in it!')
            error.exec()
        elif acc_username == '' or password == '':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Username and password can not be empty!')
            error.exec()
        elif password == password_again:
            if label == '':
                label = '0'
                response = accounts.add_acc_to_folder(username, label, folder_name, acc_username, password)
            else:
                response = accounts.add_acc_to_folder(username, label, folder_name, acc_username, password)

            if response == folder_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(print_folder_not_found_error)
                error.exec()
            elif response == 'added acc to folder':
                acc_added = QMessageBox()
                acc_added.setWindowTitle('Success')
                acc_added.setText('Account was added successfully!')
                acc_added.exec()
            elif response == 'folder name can not be empty':
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText('Folder name can\'t be empty!')
                error.exec()
            elif response == user_acc_folder_not_found_error:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(user_acc_folder_error)
                error.exec()
            else:
                error = QMessageBox()
                error.setWindowTitle('Error')
                error.setText(unknown_error)
                add_acc_to_folder_form.close()
                error.exec()
        elif password != password_again:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Passwords do not match!')
            error.exec()
            add_acc_to_folder_form.PasswordInput.clear()
            add_acc_to_folder_form.PasswordAgainInput.clear()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            add_acc_to_folder_form.close()
            error.exec()

    add_acc_to_folder_form.bAddAccToFolder.clicked.connect(validate_acc_add)


def list_acc_in_folder(username):
    acc_in_folder_list_form = window_init.AccInFolderListWindow()
    acc_in_folder_list_form.show()

    folder_list = accounts.get_acc_folders(username).split('/    ')
    for folder in folder_list:
        if folder != '':
            acc_in_folder_list_form.cbFolders.addItem(folder)

    def validate_list_acc():
        folder_name = acc_in_folder_list_form.cbFolders.currentText()

        response = accounts.get_acc_in_folder(username, folder_name)

        if response == folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(print_folder_not_found_error)
            error.exec()
        elif response == user_acc_folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_folder_error)
            error.exec()
        elif isinstance(response, str):
            acc_in_folder_list_form.AccInFolderListText.setPlainText(response)
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            acc_in_folder_list_form.close()
            error.exec()

    acc_in_folder_list_form.bListAccounts.clicked.connect(validate_list_acc)


def remove_acc_in_folder(username):
    remove_acc_in_folder_form = window_init.RemoveAccInFolderWindow()
    remove_acc_in_folder_form.show()

    folder_list = accounts.get_acc_folders(username).split('/    ')
    for folder in folder_list:
        if folder != '':
            remove_acc_in_folder_form.cbFolders.addItem(folder)

    def get_acc_in_folder():
        remove_acc_in_folder_form.cbAccounts.clear()
        account = ''
        folder_name = remove_acc_in_folder_form.cbFolders.currentText()
        accounts_list = accounts.get_acc_in_folder(username, folder_name)
        if accounts_list == user_acc_folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_folder_error)
            error.exec()
            return 'user acc folder not found'
        else:
            accounts_list = accounts_list.split('\n\n')
        for account_item in accounts_list:
            if account_item != '':
                account_item = account_item.split('\n')
                for account_part in account_item:
                    if 'password: ' not in account_part and 'username: ' not in account_part:
                        account += account_part + ' '
                    elif 'password: ' not in account_part:
                        account += account_part
            if account != '':
                remove_acc_in_folder_form.cbAccounts.addItem(account)
            account = ''

    def validate_remove_acc():
        folder_name = remove_acc_in_folder_form.cbFolders.currentText()
        acc_number = remove_acc_in_folder_form.cbAccounts.currentText().split('.')[0]
        acc_username = remove_acc_in_folder_form.cbAccounts.currentText().split('username: ')[-1]

        response = accounts.remove_acc_in_folder(username, folder_name, acc_number, acc_username)
        if response == folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(print_folder_not_found_error)
            error.exec()
        elif response == 'account not found':
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText('Account not found!')
            error.exec()
        elif response == 'account removed':
            removed_acc = QMessageBox()
            removed_acc.setWindowTitle('Success')
            removed_acc.setText('Account successfully removed!')
            removed_acc.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            remove_acc_in_folder_form.close()
            error.exec()

        get_acc_in_folder()

    remove_acc_in_folder_form.bGetAcc.clicked.connect(get_acc_in_folder)
    remove_acc_in_folder_form.bRemoveAccInFolder.clicked.connect(validate_remove_acc)


def clear_acc_in_folder(username):
    clear_acc_in_folder_form = window_init.ClearAccInFolderWindow()
    clear_acc_in_folder_form.show()

    folder_list = accounts.get_acc_folders(username).split('/    ')
    for folder in folder_list:
        if folder != '':
            clear_acc_in_folder_form.cbFolders.addItem(folder)

    def validate_clear_acc():
        folder_name = clear_acc_in_folder_form.cbFolders.currentText()

        response = accounts.clear_acc_folder(username, folder_name)
        if response == folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(print_folder_not_found_error)
            error.exec()
        elif response == 'acc folder cleared':
            cleared_acc = QMessageBox()
            cleared_acc.setWindowTitle('Success')
            cleared_acc.setText('Accounts folder successfully cleared!')
            cleared_acc.exec()
        elif response == user_acc_folder_not_found_error:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(user_acc_folder_error)
            error.exec()
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            clear_acc_in_folder_form.close()
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
            error.setWindowTitle('Error')
            error.setText('Invalid length!')
            error.exec()
            generate_strong_pass_form.NumberOfCharsInput.clear()
        elif isinstance(response, str):
            generate_strong_pass_form.OutputText.setText(response)
        else:
            error = QMessageBox()
            error.setWindowTitle('Error')
            error.setText(unknown_error)
            generate_strong_pass_form.close()
            error.exec()

    generate_strong_pass_form.bGenerateStrongPass.clicked.connect(generate)


def backup_acc(username):
    accounts.backup(username)

    if accounts == user_acc_folder_not_found_error:
        error = QMessageBox()
        error.setWindowTitle('Error')
        error.setText(user_acc_folder_error)
        error.exec()
    else:
        backup = QMessageBox()
        backup.setWindowTitle('Success')
        backup.setText('Successfully backed up the accounts to backup.txt (on desktop)')
        backup.exec()


def restore_acc(username):
    response = accounts.restore(username)
    if response == 'desktop no backup.txt':
        error = QMessageBox()
        error.setWindowTitle('Error')
        error.setText('There is no ' + username + 'backup.txt file on the desktop')
        error.exec()
    elif response == user_acc_folder_not_found_error:
        error = QMessageBox()
        error.setWindowTitle('Error')
        error.setText(user_acc_folder_error)
        error.exec()
    else:
        restored = QMessageBox()
        restored.setWindowTitle('Success')
        restored.setText('Successfully restored all accounts!')
        restored.exec()
