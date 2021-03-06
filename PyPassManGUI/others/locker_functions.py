from others import accounts, window_init, stylesheets
from PyQt6.QtWidgets import QMessageBox

# Common errors used among the file
unknown_error = "An unknown error occurred. Close the app and try again!"
folder_not_found_error = "folder not found"
print_folder_not_found_error = "Folder not found!"
banned_chars = "banned chars in text"
banned_chars_error = "A file name can't contain any of the following characters:\n\t\t\\ / : * ? \" < > |"
app_acc_dir_not_found_error = "PyPassMan accounts dir does not exist"
user_acc_dir_not_found_error = "user accounts dir does not exist"
user_acc_folder_not_found_error = "user acc folder does not exist"
app_dir_error = (
    "The directory with the accounts for the app was not found!"
    " If after a restart it does not work reinstalling the application"
    " might be the only solution."
)
user_acc_dir_error = (
    "The user acc directory was not found! This means that there is no data "
    "about any accounts! Reinstalling the program might be the only solution."
)
user_acc_folder_error = (
    "The folder with this user data was not found! Removing and adding back "
    "the account might be the only to fix this."
)

# Loads the current ui style and assigns it
current_style = stylesheets.load_current_style()


def window_prompt(title: str, prompt_text: str):  # Window prompts template used in app
    prompt = QMessageBox()
    prompt.setWindowTitle(title)
    prompt.setText(prompt_text)
    prompt.setStyleSheet(current_style)
    prompt.exec()


def create_acc_folder(username: str):
    # Initializes the window with the help of window_init file
    create_acc_folder_form = window_init.CreateAccFolderWindow()

    def validate_creation():
        folder_name = create_acc_folder_form.FolderNameInput.text()

        response = accounts.create_acc_folder(username, folder_name)
        # Based on the return of accounts.py function prompts the user with what happened
        if response == "folder already exists":
            window_prompt(
                "Error",
                "Acc Folder with name "
                + folder_name
                + " already exists, try a different name!",
            )
            create_acc_folder_form.FolderNameInput.clear()
        elif response == "folder created":
            window_prompt(
                "Success", "Acc Folder " + folder_name + " was created successfully!"
            )
        elif response == "folder name can not be empty":
            window_prompt("Error", "Folder name can not be empty")
        elif response == banned_chars:
            window_prompt("Error", banned_chars_error)
            create_acc_folder_form.FolderNameInput.clear()
        elif response == user_acc_dir_not_found_error:
            window_prompt("Error", user_acc_dir_error)
        else:
            window_prompt("Error", unknown_error)
            create_acc_folder_form.close()

    create_acc_folder_form.bCreateAccFolder.clicked.connect(validate_creation)
    create_acc_folder_form.show()  # Windows shown only after fully initialized


def list_acc_folders(username: str):
    # Initializes the window with the help of window_init file
    acc_folders_list_form = window_init.AccFolderListWindow()

    def get_folders():
        folder_list = accounts.get_acc_folders(username)
        if folder_list != "":
            acc_folders_list_form.AccFolderListText.setPlainText(folder_list)
        elif folder_list == user_acc_folder_not_found_error:
            window_prompt("Error", user_acc_folder_error)
        else:
            acc_folders_list_form.AccFolderListText.setPlainText(
                "You don't have any account folders."
            )

    # Runs get_folders once to have them printed when opening the window
    get_folders()

    acc_folders_list_form.bRefresh.clicked.connect(get_folders)
    acc_folders_list_form.show()  # Windows shown only after fully initialized


def delete_acc_folder(username: str):
    # Initializes the window with the help of window_init file
    delete_acc_folder_form = window_init.DeleteAccFolderWindow()

    # Makes a list out of the folders string and assigns it to the combo box
    folder_list = accounts.get_acc_folders(username).split("/    ")
    for folder in folder_list:
        if folder != "":
            delete_acc_folder_form.cbFolders.addItem(folder)

    def validate_deletion():
        folder_name = delete_acc_folder_form.cbFolders.currentText()

        response = accounts.remove_acc_folder(username, folder_name)
        # Prompts user based on the response returned by the function
        if response == folder_not_found_error:
            window_prompt(
                "Error",
                "Acc Folder with name "
                + folder_name
                + " does not exist, try a different one.",
            )
        elif response == "deleted acc folder":
            window_prompt(
                "Success",
                "Acc Folder with name " + folder_name + " was successfully deleted!",
            )
        elif response == user_acc_folder_not_found_error:
            window_prompt("Error", user_acc_folder_error)
        else:
            window_prompt("Error", unknown_error)
            delete_acc_folder_form.close()

        # Clears the combo box before adding new values
        delete_acc_folder_form.cbFolders.clear()

        # Splits the string with the folders list and adds them to the combo box
        new_folder_list = accounts.get_acc_folders(username).split("/    ")
        for new_folder in new_folder_list:
            if new_folder != "":
                delete_acc_folder_form.cbFolders.addItem(new_folder)

    delete_acc_folder_form.bDeleteAccFolder.clicked.connect(validate_deletion)
    delete_acc_folder_form.show()  # Windows only shown after fully initialized


def add_acc_to_folder(username: str):
    # Initializes the window with the help of window_init file
    add_acc_to_folder_form = window_init.AddAccToFolderWindow()

    # Splits the folder list and adds each folder to the combo box
    folder_list = accounts.get_acc_folders(username).split("/    ")
    for folder in folder_list:
        if folder != "":
            add_acc_to_folder_form.cbFolders.addItem(folder)

    def validate_acc_add():
        folder_name = add_acc_to_folder_form.cbFolders.currentText()
        label = add_acc_to_folder_form.LabelInput.text()
        acc_username = add_acc_to_folder_form.UsernameInput.text()
        password = add_acc_to_folder_form.PasswordInput.text()
        password_again = add_acc_to_folder_form.PasswordAgainInput.text()

        if "username: " in acc_username:
            window_prompt("Error", 'Username can not contain "username: " in it!')
        elif acc_username == "" or password == "":
            window_prompt("Error", "Username and password can not be empty!")
        elif password == password_again:
            if label == "":
                label = "0"
                response = accounts.add_acc_to_folder(
                    username, label, folder_name, acc_username, password
                )
            else:
                response = accounts.add_acc_to_folder(
                    username, label, folder_name, acc_username, password
                )

            # Prompts the user based on the response returned by the function
            if response == folder_not_found_error:
                window_prompt("Error", print_folder_not_found_error)
            elif response == "added acc to folder":
                window_prompt("Success", "Account was added successfully!")
            elif response == "folder name can not be empty":
                window_prompt("Error", "Folder name can't be empty!")
            elif response == user_acc_folder_not_found_error:
                window_prompt("Error", user_acc_folder_error)
            elif response == "username contains digit_separator":
                window_prompt(
                    "Error",
                    "Username can not contain the following phrase:\n\t\t///!@#$%^&*()\\\\\\",
                )
            elif response == "password contains label_separator":
                window_prompt(
                    "Error",
                    "Password can not contain the following phrase:\n\t\t\\\\\\)(*&^%$#@!///",
                )
            else:
                window_prompt("Error", unknown_error)
                add_acc_to_folder_form.close()
        elif password != password_again:
            window_prompt("Error", "Passwords do not match!")
            add_acc_to_folder_form.PasswordInput.clear()
            add_acc_to_folder_form.PasswordAgainInput.clear()
        else:
            window_prompt("Error", unknown_error)
            add_acc_to_folder_form.close()

    add_acc_to_folder_form.bAddAccToFolder.clicked.connect(validate_acc_add)
    add_acc_to_folder_form.show()  # Windows only shown after fully initialized


def list_acc_in_folder(username: str):
    # Initializes the window with the help of window_init file
    acc_in_folder_list_form = window_init.AccInFolderListWindow()

    # Splits the folder list and adds each folder in the combo box
    folder_list = accounts.get_acc_folders(username).split("/    ")
    for folder in folder_list:
        if folder != "":
            acc_in_folder_list_form.cbFolders.addItem(folder)

    def validate_list_acc():
        folder_name = acc_in_folder_list_form.cbFolders.currentText()

        response = accounts.get_acc_in_folder(username, folder_name)
        # Prompts the user based on the response returned by the function
        if response == folder_not_found_error:
            window_prompt("Error", print_folder_not_found_error)
        elif response == user_acc_folder_not_found_error:
            window_prompt("Error", user_acc_folder_error)
        elif isinstance(response, str):
            acc_in_folder_list_form.AccInFolderListText.setPlainText(response)
        else:
            window_prompt("Error", unknown_error)
            acc_in_folder_list_form.close()

    acc_in_folder_list_form.bListAccounts.clicked.connect(validate_list_acc)
    acc_in_folder_list_form.show()  # Windows are only shown after fully initialized


def remove_acc_in_folder(username: str):
    # Initializes the window with the help of window_init file
    remove_acc_in_folder_form = window_init.RemoveAccInFolderWindow()

    # Splits the folder list and adds each folder in the combo box
    folder_list = accounts.get_acc_folders(username).split("/    ")
    for folder in folder_list:
        if folder != "":
            remove_acc_in_folder_form.cbFolders.addItem(folder)

    def get_acc_in_folder():
        remove_acc_in_folder_form.cbAccounts.clear()
        account = ""
        folder_name = remove_acc_in_folder_form.cbFolders.currentText()
        accounts_list = accounts.get_acc_in_folder(username, folder_name)
        if accounts_list == user_acc_folder_not_found_error:
            window_prompt("Error", user_acc_folder_error)
            return "user acc folder not found"
        else:
            accounts_list = accounts_list.split("\n\n")
        for account_item in accounts_list:
            if account_item != "":
                account_item = account_item.split("\n")
                for account_part in account_item:
                    if (
                        "password: " not in account_part
                        and "username: " not in account_part
                    ):
                        account += account_part + " "
                    elif "password: " not in account_part:
                        account += account_part
            if account != "":
                remove_acc_in_folder_form.cbAccounts.addItem(account)
            account = ""

    def validate_remove_acc():
        folder_name = remove_acc_in_folder_form.cbFolders.currentText()
        acc_number = remove_acc_in_folder_form.cbAccounts.currentText().split(".")[0]
        acc_username = remove_acc_in_folder_form.cbAccounts.currentText().split(
            "username: "
        )[-1]

        response = accounts.remove_acc_in_folder(
            username, folder_name, acc_number, acc_username
        )
        # Prompts the user based on the response returned by the function
        if response == folder_not_found_error:
            window_prompt("Error", print_folder_not_found_error)
        elif response == "account not found":
            window_prompt("Error", "Account not found!")
        elif response == "account removed":
            window_prompt("Success", "Account successfully removed!")
        else:
            window_prompt("Error", unknown_error)
            remove_acc_in_folder_form.close()

        get_acc_in_folder()  # this is run to display the accounts in the selected folder

    remove_acc_in_folder_form.bGetAcc.clicked.connect(get_acc_in_folder)
    remove_acc_in_folder_form.bRemoveAccInFolder.clicked.connect(validate_remove_acc)
    remove_acc_in_folder_form.show()  # Windows only shown when fully initialized


def clear_acc_in_folder(username: str):
    clear_acc_in_folder_form = window_init.ClearAccInFolderWindow()

    # Splits folder list and adds each folder in the combo box
    folder_list = accounts.get_acc_folders(username).split("/    ")
    for folder in folder_list:
        if folder != "":
            clear_acc_in_folder_form.cbFolders.addItem(folder)

    def validate_clear_acc():
        folder_name = clear_acc_in_folder_form.cbFolders.currentText()

        response = accounts.clear_acc_folder(username, folder_name)
        # Prompts the user based on the response returned by the function
        if response == folder_not_found_error:
            window_prompt("Error", print_folder_not_found_error)
        elif response == "acc folder cleared":
            window_prompt("Success", "Accounts folder successfully cleared!")
        elif response == user_acc_folder_not_found_error:
            window_prompt("Error", user_acc_folder_error)
        else:
            window_prompt("Error", unknown_error)
            clear_acc_in_folder_form.close()

    clear_acc_in_folder_form.bClearAccInFolder.clicked.connect(validate_clear_acc)
    clear_acc_in_folder_form.show()  # Windows only shown when fully initialized


def generate_strong_pass():
    # Initializes the window with the help of window_init file
    generate_strong_pass_form = window_init.GenerateStrongPasswordWindow()

    def generate():
        chars_number = generate_strong_pass_form.NumberOfCharsInput.text()

        response = accounts.pass_gen(chars_number)
        # Prompts the user based on the response returned by the function
        if response == "invalid length":
            window_prompt("Error", "Invalid length!")
            generate_strong_pass_form.NumberOfCharsInput.clear()
        elif isinstance(response, str):
            generate_strong_pass_form.OutputText.setText(response)
        else:
            window_prompt("Error", unknown_error)
            generate_strong_pass_form.close()

    generate_strong_pass_form.bGenerateStrongPass.clicked.connect(generate)
    generate_strong_pass_form.show()  # Windows only shown when fully initialized


def backup_acc(username: str):
    accounts.backup(username)
    if accounts == user_acc_folder_not_found_error:
        window_prompt("Error", user_acc_folder_error)
    else:
        window_prompt(
            "Success", "Successfully backed up the accounts to backup.txt (on desktop)"
        )


def restore_acc(username: str):
    response = accounts.restore(username)
    # Prompts the user based on the response returned by the function
    if response == "desktop no backup.txt":
        window_prompt(
            "Error", "There is no " + username + "backup.txt file on the desktop"
        )
    elif response == user_acc_folder_not_found_error:
        window_prompt("Error", user_acc_folder_error)
    else:
        window_prompt("Success", "Successfully restored all accounts!")
