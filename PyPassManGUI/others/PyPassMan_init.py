import os
from others import locker_functions, accounts, window_init, stylesheets, logger
from PyQt6.QtWidgets import QMessageBox


def window_prompt(title: str, prompt_text: str):
    """
    Window prompt template used across the app.

    :param title: Window title.
    :param prompt_text: Text to prompt.
    :return: Nothing, just shows a window prompt.
    """
    # Loads the current ui style and assigns it
    current_style = stylesheets.load_current_style()
    prompt = QMessageBox()
    prompt.setWindowTitle(title)
    prompt.setText(prompt_text)
    prompt.setStyleSheet(current_style)
    prompt.exec()


class MainForm:
    """
    MainForm UI functions.
    """

    log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
    # Common returns used in this functions
    banned_chars = "banned chars in text"
    app_acc_dir_not_found_error = "PyPassMan accounts dir does not exist"
    user_acc_dir_not_found_error = "user accounts dir does not exist"
    # Common error prompts used in this functions
    banned_chars_error = "Usernames can't contain any of the following characters:\n\t\t\\ / : * ? \" < > |"
    app_dir_error = (
        "The directory with the accounts for the app was not found!"
        " If after a restart it does not work reinstalling the application"
        " might be the only solution."
    )
    user_acc_dir_error = (
        "The user acc directory was not found! This means that there is no data "
        "about any accounts! Reinstalling the program might be the only solution."
    )
    unknown_error = "An unknown error occurred. Close the app and try again!"

    @classmethod
    def register(cls):
        """
        Initializes, manages and shows the "Register" window.

        :return: Nothing.
        """
        # Initializes the window with the help of window_init file
        register_account_form = window_init.RegisterAccountWindow()

        def validate_add_account():
            """
            Validates the info in order to add the account to the app.

            :return: Nothing.
            """
            username_input = register_account_form.UsernameInput.text()
            password_input = register_account_form.PasswordInput.text()
            password_again_input = register_account_form.PasswordAgainInput.text()

            if password_input == password_again_input and len(password_input) > 3:
                response = accounts.PyPassManAcc.register_acc(
                    username_input, password_input
                )
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
                elif response == cls.banned_chars:
                    window_prompt("Error", cls.banned_chars_error)
                    register_account_form.UsernameInput.clear()
                elif response == cls.app_acc_dir_not_found_error:
                    window_prompt("Error", cls.app_dir_error)
                elif response == cls.user_acc_dir_not_found_error:
                    window_prompt("Error", cls.user_acc_dir_error)
                elif response == "acc folder already exists":
                    window_prompt(
                        "Error",
                        "A folder with user is already present in the app! Any data this "
                        "folder had was not changed, if you did not want this you can "
                        "delete the acc and try recreate it.",
                    )
                else:
                    window_prompt("Error", cls.unknown_error)
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
                window_prompt("Error", cls.unknown_error)
                register_account_form.close()

        register_account_form.bRegisterAccount.clicked.connect(validate_add_account)
        register_account_form.show()  # Windows only shown when fully initialized
        # Logging line
        cls.log.debug_log('"Register Account" window opened.', logger.get_lineno())

    @classmethod
    def login(cls):
        """
        Initializes, manages and shows the "Login" window.

        :return: Nothing.
        """
        # Initializes the windows with the help of window_init file
        login_account_form = window_init.LoginAccountWindow()
        locker_form = window_init.LockerWindow()

        def validate_login():
            """
            Validates the info in order to login user into their account.

            :return: Nothing.
            """
            username_input = login_account_form.UsernameInput.text()
            password_input = login_account_form.PasswordInput.text()

            response = accounts.PyPassManAcc.login(username_input, password_input)
            # Prompts the user based on the response returned by the function
            if response == "login successful":
                window_prompt(
                    "Success",
                    "Successfully logged into account " + username_input + ".",
                )
                login_account_form.close()
                MainForm.after_login(locker_form, username_input)
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
            elif response == cls.app_acc_dir_not_found_error:
                window_prompt("Error", cls.app_dir_error)
            else:
                window_prompt("Error", cls.unknown_error)
                login_account_form.close()

        login_account_form.bLogin.clicked.connect(validate_login)
        login_account_form.show()  # Windows only shown when fully initialized
        # Logging line
        cls.log.debug_log('"Login Account" window opened.', logger.get_lineno())

    @classmethod
    def remove_acc(cls):
        """
        Initializes, manages and shows the "Remove Acc" window.

        :return: Nothing.
        """
        # Initializes the window with the help of window_init file
        remove_account_form = window_init.RemoveAccountWindow()

        def validate_remove_acc():
            """
            Validates the info in order to remove the app account.

            :return: Nothing.
            """
            username_input = remove_account_form.UsernameInput.text()
            password_input = remove_account_form.PasswordInput.text()
            password_again_input = remove_account_form.PasswordAgainInput.text()

            if password_input == password_again_input:
                response = accounts.PyPassManAcc.remove_acc(
                    username_input, password_input
                )
                # Prompts the user based on the response return by the function
                if response == "account deleted":
                    window_prompt(
                        "Success",
                        "Successfully removed account " + username_input + "!",
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
                elif response == cls.app_acc_dir_not_found_error:
                    window_prompt("Error", cls.app_dir_error)
                elif response == cls.user_acc_dir_not_found_error:
                    window_prompt("Error", cls.user_acc_dir_error)
                elif response == "user folder was not found":
                    window_prompt(
                        "Error",
                        "This user folder was not found, we just deleted it's metadata "
                        "and everything should be fine in theory!",
                    )
                else:
                    window_prompt("Error", cls.unknown_error)
                    remove_account_form.close()

            elif password_input != password_again_input:
                window_prompt("Error", "The passwords don't match! Try again")
                remove_account_form.PasswordInput.clear()
                remove_account_form.PasswordAgainInput.clear()
            else:
                window_prompt("Error", cls.unknown_error)
                remove_account_form.close()

        remove_account_form.bRemoveAccount.clicked.connect(validate_remove_acc)
        remove_account_form.show()  # Windows shown only when fully initialized
        # Logging line
        cls.log.debug_log('"Remove Account" window opened.', logger.get_lineno())

    @classmethod
    def style_manager(cls, style_manager_form):
        """
        Initializes, manages and shows the "Style Manager" window.

        :return: Nothing.
        """
        # Initializes the window with the help of window_init file
        change_style_form = window_init.ChangeStyleWindow()
        add_style_form = window_init.AddStyleWindow()

        def change_style():
            change_style_form.cbStyles.clear()
            change_style_form.cbStyles.addItems(stylesheets.get_stylesheets())

            def validate_change_style():
                """
                Validates the information in order to change the app style.

                :return: Nothing.
                """
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
                    window_prompt("Error", cls.unknown_error)

            change_style_form.bChangeStyle.clicked.connect(validate_change_style)
            change_style_form.show()  # Windows only shown when fully initialized
            # Logging line
            cls.log.debug_log('"Change Style" window opened.', logger.get_lineno())

        def add_style():
            """
            Initializes, manages and shows the "Add Style" window.

            :return: Nothing.
            """

            def validate_add_style():
                """
                Validates the info in order to add the new style for the app.

                :return: Nothing.
                """
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
                        window_prompt("Error", cls.unknown_error)

            add_style_form.bAddStyle.clicked.connect(validate_add_style)
            add_style_form.show()  # Windows only shown when fully initialized
            # Logging line
            cls.log.debug_log('"Add Style" window opened.', logger.get_lineno())

        style_manager_form.bChangeStyle.clicked.connect(change_style)
        style_manager_form.bAddStyle.clicked.connect(add_style)
        style_manager_form.show()
        # Logging line
        cls.log.debug_log('"Style Manager" window opened.', logger.get_lineno())

    @classmethod
    def after_login(cls, locker_form, user):
        """
        Initializes, manages and shows the "Locker" window.

        :return: Nothing.
        """
        user_acc_folders = locker_functions.Locker.UserAccFolders(user)
        user_acc_folders_content = locker_functions.Locker.UserAccFoldersContent(user)
        user_acc_manager = locker_functions.Locker.UserAccManager(user)

        locker_form.bCreateAccFolder.clicked.connect(
            lambda: user_acc_folders.create_acc_folder()
        )
        locker_form.bListAccFolder.clicked.connect(
            lambda: user_acc_folders.list_acc_folders()
        )
        locker_form.bRemoveAccFolder.clicked.connect(
            lambda: user_acc_folders.delete_acc_folder()
        )
        locker_form.bAddAccToFolder.clicked.connect(
            lambda: user_acc_folders_content.add_acc_to_folder()
        )
        locker_form.bGetAccInFolder.clicked.connect(
            lambda: user_acc_folders_content.list_acc_in_folder()
        )
        locker_form.bRemoveAccInFolder.clicked.connect(
            lambda: user_acc_folders_content.remove_acc_in_folder()
        )
        locker_form.bClearAccInFolder.clicked.connect(
            lambda: user_acc_folders_content.clear_acc_in_folder()
        )
        locker_form.bGeneratePass.clicked.connect(
            lambda: locker_functions.Locker.generate_strong_pass()
        )
        locker_form.bBackup.clicked.connect(lambda: user_acc_manager.backup_acc())
        locker_form.bRestore.clicked.connect(lambda: user_acc_manager.restore_acc())
        locker_form.bLogout.clicked.connect(locker_form.close)

        locker_form.show()  # Windows only shown after fully initialized
        # Logging line
        cls.log.debug_log('"Locker" window opened.', logger.get_lineno())
