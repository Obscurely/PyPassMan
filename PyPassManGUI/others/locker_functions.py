import os
from others import accounts, window_init, PyPassMan_init, logger


class Locker:
    """
    Locker UI functions.
    """

    log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
    # Common error prompts used in this functions
    unknown_error = "An unknown error occurred. Close the app and try again!"

    class UserAccFolders:
        """
        Locker UI functions related to account folders.
        """

        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        # Common returns used in this functions
        banned_chars = "banned chars in text"
        user_acc_dir_not_found_error = "user accounts dir does not exist"
        user_acc_folder_not_found_error = "user acc folder does not exist"
        folder_not_found_error = "folder not found"
        # Common error prompts used in this functions
        banned_chars_error = "A file name can't contain any of the following characters:\n\t\t\\ / : * ? \" < > |"
        user_acc_dir_error = (
            "The user acc directory was not found! This means that there is no data "
            "about any accounts! Reinstalling the program might be the only solution."
        )
        user_acc_folder_error = (
            "The folder with this user data was not found! Removing and adding back "
            "the account might be the only to fix this."
        )
        unknown_error = "An unknown error occurred. Close the app and try again!"

        def create_acc_folder(self):
            """
            Initializes, manages and shows the "Create Acc Folder" window.

            :return: Nothing.
            """

            # Initializes the window with the help of window_init file
            create_acc_folder_form = window_init.CreateAccFolderWindow()

            def validate_creation():
                """
                Validates if the info is right for creating the account folder.

                :return: Nothing.
                """

                folder_name = create_acc_folder_form.FolderNameInput.text()

                response = self.acc_folders.create_acc_folder(folder_name)
                # Based on the return of accounts.py function prompts the user with what happened
                if response == "folder already exists":
                    PyPassMan_init.window_prompt(
                        "Error",
                        "Acc Folder with name "
                        + folder_name
                        + " already exists, try a different name!",
                    )
                    create_acc_folder_form.FolderNameInput.clear()
                elif response == "folder created":
                    PyPassMan_init.window_prompt(
                        "Success",
                        "Acc Folder " + folder_name + " was created successfully!",
                    )
                elif response == "folder name can not be empty":
                    PyPassMan_init.window_prompt(
                        "Error", "Folder name can not be empty"
                    )
                elif response == self.banned_chars:
                    PyPassMan_init.window_prompt("Error", self.banned_chars_error)
                    create_acc_folder_form.FolderNameInput.clear()
                elif response == self.user_acc_dir_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_dir_error)
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    create_acc_folder_form.close()

            create_acc_folder_form.bCreateAccFolder.clicked.connect(validate_creation)
            create_acc_folder_form.show()  # Windows shown only after fully initialized
            # Logging line
            self.log.debug_log(
                '"Create Acc Folder" window opened.', logger.get_lineno()
            )

        def list_acc_folders(self):
            """
            Initializes, manages and shows the "List Acc Folders" window.

            :return: Nothing.
            """

            # Initializes the window with the help of window_init file
            acc_folders_list_form = window_init.AccFolderListWindow()

            def get_folders():
                """
                Writes the folder list in the text box.

                :return: Nothing.
                """
                folder_list = self.acc_folders.get_acc_folders()
                if folder_list != "":
                    acc_folders_list_form.AccFolderListText.setPlainText(folder_list)
                elif folder_list == self.user_acc_folder_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
                else:
                    acc_folders_list_form.AccFolderListText.setPlainText(
                        "You don't have any account folders."
                    )

            # Runs get_folders once to have them printed when opening the window
            get_folders()

            acc_folders_list_form.bRefresh.clicked.connect(get_folders)
            acc_folders_list_form.show()  # Windows shown only after fully initialized
            # Logging line
            self.log.debug_log('"Acc Folder List" window opened.', logger.get_lineno())

        def delete_acc_folder(self):
            """
            Initializes, manages and shows the "Delete Acc Folder" window.

            :return: Nothing.
            """

            # Initializes the window with the help of window_init file
            delete_acc_folder_form = window_init.DeleteAccFolderWindow()

            # Makes a list out of the folders string and assigns it to the combo box
            folder_list = self.acc_folders.get_acc_folders().split("/    ")
            for folder in folder_list:
                if folder != "":
                    delete_acc_folder_form.cbFolders.addItem(folder)

            def validate_deletion():
                """
                Validates if info is right for deleting the account folder.

                :return: Nothing.
                """

                folder_name = delete_acc_folder_form.cbFolders.currentText()

                response = self.acc_folders.remove_acc_folder(folder_name)
                # Prompts user based on the response returned by the function
                if response == self.folder_not_found_error:
                    PyPassMan_init.window_prompt(
                        "Error",
                        "Acc Folder with name "
                        + folder_name
                        + " does not exist, try a different one.",
                    )
                elif response == "deleted acc folder":
                    PyPassMan_init.window_prompt(
                        "Success",
                        "Acc Folder with name "
                        + folder_name
                        + " was successfully deleted!",
                    )
                elif response == self.user_acc_folder_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    delete_acc_folder_form.close()

                # Clears the combo box before adding new values
                delete_acc_folder_form.cbFolders.clear()

                # Splits the string with the folders list and adds them to the combo box
                new_folder_list = self.acc_folders.get_acc_folders().split("/    ")
                for new_folder in new_folder_list:
                    if new_folder != "":
                        delete_acc_folder_form.cbFolders.addItem(new_folder)

            delete_acc_folder_form.bDeleteAccFolder.clicked.connect(validate_deletion)
            delete_acc_folder_form.show()  # Windows only shown after fully initialized
            # Logging line
            self.log.debug_log('"Delete Acc Folder" window opened', logger.get_lineno())

        def __init__(self, user):
            self.user = user
            self.acc_folders = accounts.Locker.AccFolders(user)

    class UserAccFoldersContent:
        """
        Locker UI functions related to the contents of the user's account folders.
        """

        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        # Common returns used in this functions
        folder_not_found_error = "folder not found"
        user_acc_folder_not_found_error = "user acc folder does not exist"
        # Common error prompts used in this functions
        print_folder_not_found_error = "Folder not found!"
        user_acc_folder_error = (
            "The folder with this user data was not found! Removing and adding back "
            "the account might be the only to fix this."
        )
        unknown_error = "An unknown error occurred. Close the app and try again!"

        def add_acc_to_folder(self):
            """
            Initializes, manages and shows the "Add Acc To Folder" window.

            :return: Nothing.
            """

            # Initializes the window with the help of window_init file
            add_acc_to_folder_form = window_init.AddAccToFolderWindow()

            # Splits the folder list and adds each folder to the combo box
            folder_list = self.acc_folders.get_acc_folders().split("/    ")
            for folder in folder_list:
                if folder != "":
                    add_acc_to_folder_form.cbFolders.addItem(folder)

            def validate_acc_add():
                """
                Validates if the info is right in order to add the account to the folder.

                :return: Nothing.
                """

                folder_name = add_acc_to_folder_form.cbFolders.currentText()
                label = add_acc_to_folder_form.LabelInput.text()
                acc_username = add_acc_to_folder_form.UsernameInput.text()
                password = add_acc_to_folder_form.PasswordInput.text()
                password_again = add_acc_to_folder_form.PasswordAgainInput.text()

                if "username: " in acc_username:
                    PyPassMan_init.window_prompt(
                        "Error", 'Username can not contain "username: " in it!'
                    )
                elif acc_username == "" or password == "":
                    PyPassMan_init.window_prompt(
                        "Error", "Username and password can not be empty!"
                    )
                elif password == password_again:
                    if label == "":
                        label = "0"
                        response = self.acc_folders_content.add_acc_to_folder(
                            label, folder_name, acc_username, password
                        )
                    elif label == "0":
                        PyPassMan_init.window_prompt("Error", "Label can not be 0!")
                        return "label can not be 0"
                    else:
                        response = self.acc_folders_content.add_acc_to_folder(
                            label, folder_name, acc_username, password
                        )

                    # Prompts the user based on the response returned by the function
                    if response == self.folder_not_found_error:
                        PyPassMan_init.window_prompt(
                            "Error", self.print_folder_not_found_error
                        )
                    elif response == "added acc to folder":
                        PyPassMan_init.window_prompt(
                            "Success", "Account was added successfully!"
                        )
                    elif response == "folder name can not be empty":
                        PyPassMan_init.window_prompt(
                            "Error", "Folder name can't be empty!"
                        )
                    elif response == self.user_acc_folder_not_found_error:
                        PyPassMan_init.window_prompt(
                            "Error", self.user_acc_folder_error
                        )
                    elif response == "username contains digit_separator":
                        PyPassMan_init.window_prompt(
                            "Error",
                            "Username can not contain the following phrase:\n\t\t///!@#$%^&*()\\\\\\",
                        )
                    elif response == "password contains label_separator":
                        PyPassMan_init.window_prompt(
                            "Error",
                            "Password can not contain the following phrase:\n\t\t\\\\\\)(*&^%$#@!///",
                        )
                    else:
                        PyPassMan_init.window_prompt("Error", self.unknown_error)
                        add_acc_to_folder_form.close()
                elif password != password_again:
                    PyPassMan_init.window_prompt("Error", "Passwords do not match!")
                    add_acc_to_folder_form.PasswordInput.clear()
                    add_acc_to_folder_form.PasswordAgainInput.clear()
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    add_acc_to_folder_form.close()

            add_acc_to_folder_form.bAddAccToFolder.clicked.connect(validate_acc_add)
            add_acc_to_folder_form.show()  # Windows only shown after fully initialized
            # Logging line
            self.log.debug_log(
                '"Add Acc To Folder" window opened.', logger.get_lineno()
            )

        def list_acc_in_folder(self):
            """
            Initializes, manages and shows the "List Acc In Folder" window.

            :return: Nothing.
            """

            # Initializes the window with the help of window_init file
            acc_in_folder_list_form = window_init.AccInFolderListWindow()

            # Splits the folder list and adds each folder in the combo box
            folder_list = self.acc_folders.get_acc_folders().split("/    ")
            for folder in folder_list:
                if folder != "":
                    acc_in_folder_list_form.cbFolders.addItem(folder)

            def validate_list_acc():
                """
                Validates the info and displays the list of the accounts in the folder.

                :return: Nothing.
                """
                folder_name = acc_in_folder_list_form.cbFolders.currentText()

                response = self.acc_folders_content.get_acc_in_folder(folder_name)
                # Prompts the user based on the response returned by the function
                if response == self.folder_not_found_error:
                    PyPassMan_init.window_prompt(
                        "Error", self.print_folder_not_found_error
                    )
                elif response == self.user_acc_folder_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
                elif isinstance(response, str):
                    acc_in_folder_list_form.AccInFolderListText.setPlainText(response)
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    acc_in_folder_list_form.close()

            acc_in_folder_list_form.bListAccounts.clicked.connect(validate_list_acc)
            acc_in_folder_list_form.show()  # Windows are only shown after fully initialized
            # Logging line
            self.log.debug_log(
                '"Acc In folder List" window opened.', logger.get_lineno()
            )

        def remove_acc_in_folder(self):
            """
            Initializes, manages and shows the "Remove Acc In Folder" window.

            :return: Nothing.
            """
            # Initializes the window with the help of window_init file
            remove_acc_in_folder_form = window_init.RemoveAccInFolderWindow()

            # Splits the folder list and adds each folder in the combo box
            folder_list = self.acc_folders.get_acc_folders().split("/    ")
            for folder in folder_list:
                if folder != "":
                    remove_acc_in_folder_form.cbFolders.addItem(folder)

            def get_acc_in_folder():
                """
                Gets the available accounts for deletion.

                :return: Available accounts for deletion.
                """
                remove_acc_in_folder_form.cbAccounts.clear()
                account = ""
                folder_name = remove_acc_in_folder_form.cbFolders.currentText()
                accounts_list = self.acc_folders_content.get_acc_in_folder(folder_name)
                if accounts_list == self.user_acc_folder_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
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
                """
                Validates the given info in order to delete the specified account.

                :return: Nothing.
                """

                folder_name = remove_acc_in_folder_form.cbFolders.currentText()
                acc_number = remove_acc_in_folder_form.cbAccounts.currentText().split(
                    "."
                )[0]
                acc_username = remove_acc_in_folder_form.cbAccounts.currentText().split(
                    "username: "
                )[-1]

                response = self.acc_folders_content.remove_acc_in_folder(
                    folder_name, acc_number, acc_username
                )
                # Prompts the user based on the response returned by the function
                if response == self.folder_not_found_error:
                    PyPassMan_init.window_prompt(
                        "Error", self.print_folder_not_found_error
                    )
                elif response == "account not found":
                    PyPassMan_init.window_prompt("Error", "Account not found!")
                elif response == "account removed":
                    PyPassMan_init.window_prompt(
                        "Success", "Account successfully removed!"
                    )
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    remove_acc_in_folder_form.close()

                get_acc_in_folder()  # this is run to display the accounts in the selected folder

            remove_acc_in_folder_form.bGetAcc.clicked.connect(get_acc_in_folder)
            remove_acc_in_folder_form.bRemoveAccInFolder.clicked.connect(
                validate_remove_acc
            )
            remove_acc_in_folder_form.show()  # Windows only shown when fully initialized
            # Logging line
            self.log.debug_log(
                '"Remove Acc In Folder" window opened.', logger.get_lineno()
            )

        def clear_acc_in_folder(self):
            """
            Initializes, manages and shows the "Clear Acc In Folder" window.

            :return: Nothing.
            """

            clear_acc_in_folder_form = window_init.ClearAccInFolderWindow()

            # Splits folder list and adds each folder in the combo box
            folder_list = self.acc_folders.get_acc_folders().split("/    ")
            for folder in folder_list:
                if folder != "":
                    clear_acc_in_folder_form.cbFolders.addItem(folder)

            def validate_clear_acc():
                """
                Validates the info in order to clear the account folder.

                :return: Nothing.
                """
                folder_name = clear_acc_in_folder_form.cbFolders.currentText()

                response = self.acc_folders_content.clear_acc_folder(folder_name)
                # Prompts the user based on the response returned by the function
                if response == self.folder_not_found_error:
                    PyPassMan_init.window_prompt(
                        "Error", self.print_folder_not_found_error
                    )
                elif response == "acc folder cleared":
                    PyPassMan_init.window_prompt(
                        "Success", "Accounts folder successfully cleared!"
                    )
                elif response == self.user_acc_folder_not_found_error:
                    PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
                else:
                    PyPassMan_init.window_prompt("Error", self.unknown_error)
                    clear_acc_in_folder_form.close()

            clear_acc_in_folder_form.bClearAccInFolder.clicked.connect(
                validate_clear_acc
            )
            clear_acc_in_folder_form.show()  # Windows only shown when fully initialized
            # Logging line
            self.log.debug_log(
                '"Clear Acc In Folder" window opened.', logger.get_lineno()
            )

        def __init__(self, user):
            self.user = user
            self.acc_folders_content = accounts.Locker.AccFoldersContent(user)
            self.acc_folders = accounts.Locker.AccFolders(user)

    class UserAccManager:
        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        # Common returns used in this functions
        user_acc_folder_not_found_error = "user acc folder does not exist"
        # Common error prompts used in this functions
        user_acc_folder_error = (
            "The folder with this user data was not found! Removing and adding back "
            "the account might be the only to fix this."
        )

        def backup_acc(self):
            """
            Initializes, manages and shows the "Backup Acc" window.

            :return: Nothing.
            """

            self.acc_manager.backup()
            if accounts == self.user_acc_folder_not_found_error:
                PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
            else:
                PyPassMan_init.window_prompt(
                    "Success",
                    "Successfully backed up the accounts to backup.txt (on desktop)",
                )

        def restore_acc(self):
            """
            Initializes, manages and shows the "Restore Acc" window.

            :return: Nothing.
            """

            response = self.acc_manager.restore()
            # Prompts the user based on the response returned by the function
            if response == "desktop no backup.txt":
                PyPassMan_init.window_prompt(
                    "Error",
                    "There is no " + self.user + "backup.txt file on the desktop",
                )
            elif response == self.user_acc_folder_not_found_error:
                PyPassMan_init.window_prompt("Error", self.user_acc_folder_error)
            else:
                PyPassMan_init.window_prompt(
                    "Success", "Successfully restored all accounts!"
                )

        def __init__(self, user):
            self.user = user
            self.acc_manager = accounts.Locker.AccManager(user)

    @classmethod
    def generate_strong_pass(cls):
        """
        Initializes, manages and shows the "Generate Strong Pass" window.

        :return: Nothing.
        """

        # Initializes the window with the help of window_init file
        generate_strong_pass_form = window_init.GenerateStrongPasswordWindow()

        def generate():
            """
            Validates the info in order to generate a password.

            :return: Nothing.
            """

            chars_number = generate_strong_pass_form.NumberOfCharsInput.text()

            response = accounts.Locker.pass_gen(chars_number)
            # Prompts the user based on the response returned by the function
            if response == "invalid length":
                PyPassMan_init.window_prompt("Error", "Invalid length!")
                generate_strong_pass_form.NumberOfCharsInput.clear()
            elif isinstance(response, str):
                generate_strong_pass_form.OutputText.setText(response)
            else:
                PyPassMan_init.window_prompt("Error", cls.unknown_error)
                generate_strong_pass_form.close()

        generate_strong_pass_form.bGenerateStrongPass.clicked.connect(generate)
        generate_strong_pass_form.show()  # Windows only shown when fully initialized
        # Logging line
        cls.log.debug_log('"Generate Strong Pass" window opened.', logger.get_lineno())
