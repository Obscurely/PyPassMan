import re
import requests
import json
import platform
from others import aes, locker_functions, accounts, window_init, stylesheets
from PyQt6.QtWidgets import QMessageBox

# Common errors used among the file
unknown_error = "An unknown error occurred. Close the app and try again!"
banned_chars = "banned chars in text"
banned_chars_error = (
    "Usernames can't contain any of the following characters:\n\t\t\\ / : * ? \" < > |"
)
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

# other vars
if platform.system() == "Windows":
    config_file = "PyPassMan_Files\\config.json"
else:
    config_file = "PyPassMan_Files/config.json"

# Loads the current ui style and assigns it
current_style = stylesheets.load_current_style()


def window_prompt(title: str, prompt_text: str):  # Window prompts template used in app
    prompt = QMessageBox()
    prompt.setWindowTitle(title)
    prompt.setText(prompt_text)
    prompt.setStyleSheet(current_style)
    prompt.exec()


def check_first_run():  # Checks if its first app run in order to know if it needs to generate the encryption keys
    with open(config_file, "r") as f:
        metadata = json.load(f)  # Loads the config file

    if metadata["first_run"] == "Yes":
        aes.gen_keys()
        metadata["first_run"] = "No"
        with open(config_file, "w") as f:
            json.dump(metadata, f, indent=4)  # Dumps the new config file


def check_version():
    with open(config_file, "r") as f:
        metadata = json.load(f)  # Loads the config file

    metadata_url = metadata["metadata_url"]

    # Gets the latest version using requests and regex
    content = requests.get(metadata_url).text
    pattern = re.compile(r"(?<=-=-=&gt;&gt;).*?(?=&lt;=-=-)")
    latest_version = pattern.findall(content)[0]

    # If the current version doesn't match with latest one the user it prompted
    current_version = metadata["version"]
    if latest_version != current_version:
        window_prompt(
            "Update",
            "There is an update available, version: "
            + latest_version
            + "\n"
            + "You can download it with the installer or from github and read the patch notes there:\n"
            + "https://github.com/Obscurely/PyPassMan/releases",
        )


def register():
    # Initializes the window with the help of window_init file
    register_account_form = window_init.RegisterAccountWindow()

    def validate_add_account():
        username_input = register_account_form.UsernameInput.text()
        password_input = register_account_form.PasswordInput.text()
        password_again_input = register_account_form.PasswordAgainInput.text()

        if password_input == password_again_input and len(password_input) > 3:
            response = accounts.register_acc(username_input, password_input)
            # Prompts the user based on the response returned by the function
            if response == "created account":
                window_prompt(
                    "Success",
                    "Successfully created account "
                    + username_input
                    + "! You can now Login",
                )
                register_account_form.close()
            elif response == "username exists":
                window_prompt(
                    "Error",
                    "An account with username "
                    + username_input
                    + " already exists. Try again with a different username!",
                )
                register_account_form.UsernameInput.clear()
            elif response == "username empty":
                window_prompt("Error", "Username can't be empty")
            elif response == banned_chars:
                window_prompt("Error", banned_chars_error)
                register_account_form.UsernameInput.clear()
            elif response == app_acc_dir_not_found_error:
                window_prompt("Error", app_dir_error)
            elif response == user_acc_dir_not_found_error:
                window_prompt("Error", user_acc_dir_error)
            elif response == "acc folder already exists":
                window_prompt(
                    "Error",
                    "A folder with user is already present in the app! Any data this "
                    "folder had was not changed, if you did not want this you can "
                    "delete the acc and try recreate it.",
                )
            else:
                window_prompt("Error", unknown_error)
                register_account_form.close()
        elif password_input != password_again_input:
            window_prompt("Error", "The passwords don't match! Try again")
            register_account_form.PasswordInput.clear()
            register_account_form.PasswordAgainInput.clear()
        elif len(password_input) < 4:
            window_prompt("Error", "The password has to be 4 or more characters")
            register_account_form.PasswordInput.clear()
            register_account_form.PasswordAgainInput.clear()
        else:
            window_prompt("Error", unknown_error)
            register_account_form.close()

    register_account_form.bRegisterAccount.clicked.connect(validate_add_account)
    register_account_form.show()  # Windows only shown when fully initialized


def login():
    # Initializes the windows with the help of window_init file
    login_account_form = window_init.LoginAccountWindow()
    locker_form = window_init.LockerWindow()

    def validate_login():
        username_input = login_account_form.UsernameInput.text()
        password_input = login_account_form.PasswordInput.text()

        response = accounts.login(username_input, password_input)
        # Prompts the user based on the response returned by the function
        if response == "login successful":
            window_prompt(
                "Success", "Successfully logged into account " + username_input + "."
            )
            login_account_form.close()
            after_login(locker_form, username_input)
        elif response == "account not exist":
            window_prompt(
                "Error",
                "An account with username "
                + username_input
                + " does not exist. Try again!",
            )
            login_account_form.UsernameInput.clear()
        elif response == "incorrect password":
            window_prompt("Error", "Incorrect password!")
            login_account_form.PasswordInput.clear()
        elif response == app_acc_dir_not_found_error:
            window_prompt("Error", app_dir_error)
        else:
            window_prompt("Error", unknown_error)
            login_account_form.close()

    login_account_form.bLogin.clicked.connect(validate_login)
    login_account_form.show()  # Windows only shown when fully initialized


def remove_acc():
    # Initializes the window with the help of window_init file
    remove_account_form = window_init.RemoveAccountWindow()

    def validate_remove_acc():
        username_input = remove_account_form.UsernameInput.text()
        password_input = remove_account_form.PasswordInput.text()
        password_again_input = remove_account_form.PasswordAgainInput.text()

        if password_input == password_again_input:
            response = accounts.remove_acc(username_input, password_input)
            # Prompts the user based on the response return by the function
            if response == "account deleted":
                window_prompt(
                    "Success", "Successfully removed account " + username_input + "!"
                )
            elif response == "account with this username not exist":
                window_prompt(
                    "Error",
                    "An account with username "
                    + username_input
                    + " does not exist. Try again!",
                )
                remove_account_form.UsernameInput.clear()
            elif response == "password incorrect":
                window_prompt("Error", "The password is incorrect. Try again!")
                remove_account_form.PasswordInput.clear()
                remove_account_form.PasswordAgainInput.clear()
            elif response == app_acc_dir_not_found_error:
                window_prompt("Error", app_dir_error)
            elif response == user_acc_dir_not_found_error:
                window_prompt("Error", user_acc_dir_error)
            elif response == "user folder was not found":
                window_prompt(
                    "Error",
                    "This user folder was not found, we just deleted it's metadata "
                    "and everything should be fine in theory!",
                )
            else:
                window_prompt("Error", unknown_error)
                remove_account_form.close()

        elif password_input != password_again_input:
            window_prompt("Error", "The passwords don't match! Try again")
            remove_account_form.PasswordInput.clear()
            remove_account_form.PasswordAgainInput.clear()
        else:
            window_prompt("Error", unknown_error)
            remove_account_form.close()

    remove_account_form.bRemoveAccount.clicked.connect(validate_remove_acc)
    remove_account_form.show()  # Windows shown only when fully initialized


def style_manager(style_manager_form):
    # Initializes the window with the help of window_init file
    change_style_form = window_init.ChangeStyleWindow()
    add_style_form = window_init.AddStyleWindow()

    def change_style():
        change_style_form.cbStyles.addItems(stylesheets.get_stylesheets())

        def validate_change_style():
            style = change_style_form.cbStyles.currentText()
            style = style + ".qss"

            response = stylesheets.change_current_style(style)
            # Prompts the user based on the response returned by the function
            if response == "changed current style":
                window_prompt(
                    "Success",
                    "Successfully changed the current style, "
                    + "in order for it to apply please restart the app!",
                )
                exit(0)
            else:
                window_prompt("Error", unknown_error)

        change_style_form.bChangeStyle.clicked.connect(validate_change_style)
        change_style_form.show()  # Windows only shown when fully initialized

    def add_style():
        def validate_add_style():
            style_text = add_style_form.ptStyleText.toPlainText()
            style_name = add_style_form.StyleNameText.text()
            if style_name == "":
                window_prompt("Error", "Style name can not be empty!")
            else:
                response = stylesheets.add_style_sheet(style_name, style_text)
                # Prompts the user based on the response returned by the function
                if response == "style added":
                    window_prompt(
                        "Success",
                        "Successfully added style.\n"
                        + "Now you can go in change style window and apply it!",
                    )
                else:
                    window_prompt("Error", unknown_error)

        add_style_form.bAddStyle.clicked.connect(validate_add_style)
        add_style_form.show()  # Windows only shown when fully initialized

    style_manager_form.bChangeStyle.clicked.connect(change_style)
    style_manager_form.bAddStyle.clicked.connect(add_style)
    style_manager_form.show()


def after_login(locker_form, username: str):
    locker_form.bCreateAccFolder.clicked.connect(
        lambda: locker_functions.create_acc_folder(username)
    )
    locker_form.bListAccFolder.clicked.connect(
        lambda: locker_functions.list_acc_folders(username)
    )
    locker_form.bRemoveAccFolder.clicked.connect(
        lambda: locker_functions.delete_acc_folder(username)
    )
    locker_form.bAddAccToFolder.clicked.connect(
        lambda: locker_functions.add_acc_to_folder(username)
    )
    locker_form.bGetAccInFolder.clicked.connect(
        lambda: locker_functions.list_acc_in_folder(username)
    )
    locker_form.bRemoveAccInFolder.clicked.connect(
        lambda: locker_functions.remove_acc_in_folder(username)
    )
    locker_form.bClearAccInFolder.clicked.connect(
        lambda: locker_functions.clear_acc_in_folder(username)
    )
    locker_form.bGeneratePass.clicked.connect(locker_functions.generate_strong_pass)
    locker_form.bBackup.clicked.connect(lambda: locker_functions.backup_acc(username))
    locker_form.bRestore.clicked.connect(lambda: locker_functions.restore_acc(username))
    locker_form.bLogout.clicked.connect(locker_form.close)

    locker_form.show()  # Windows only shown after fully initialized
