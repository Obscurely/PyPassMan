import json
import os
import random
import string
import re
import shutil
import platform
import requests
from others import logger, aes, PyPassMan_init


class Checker:
    """
    Class with checker functions like: check_platform, check_chars, check_first_run and check_version.
    """

    # Platform check (for file location)
    @staticmethod
    def check_platform():
        """
        Gets the right path separator for the os in order to make program cross-platform.

        :return: "\\" if os is Windows, "/" if os is Unix-like (including MacOS).
        """
        if platform.system() == "Windows":
            path_separator = "\\"
        else:
            path_separator = "/"
        return path_separator

    # Stops user from creating files with chars not supported by the os
    @staticmethod
    def check_chars(text: str):
        """
        Checks if string contains banned chars for a file name.

        :param text: string to be checked.
        :return: "Good" if no banned chars are present in string, "banned chars in text" if banned chars are present in
                 string.
        """
        banned_chars_error = "banned chars in text"
        # This are char not supported by os as file names
        banned_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        for char in banned_chars:
            if char in text:
                return banned_chars_error
        return "Good"

    @staticmethod
    def check_first_run():  # Checks if its first app run in order to know if it needs to generate the encryption keys
        """
        Checks if it's first time running the app. If yes it changes it to "No" in config file and generates the
        encryption keys for the app.
        """
        # Checks the platform in order to determine the right file location
        if platform.system() == "Windows":
            config_file = "PyPassMan_Files\\config.json"
        else:
            config_file = "PyPassMan_Files/config.json"

        with open(config_file, "r") as f:
            metadata = json.load(f)  # Loads the config file
        if metadata["first_run"] == "Yes":
            aes.gen_keys()
            metadata["first_run"] = "No"
            with open(config_file, "w") as f:
                json.dump(metadata, f, indent=4)  # Dumps the new config file

    @staticmethod
    def check_version():
        """
        Checks if the app is up to date. If no it prompts the user to update it.
        """
        # Checks the platform in order to determine the right file location
        if platform.system() == "Windows":
            config_file = "PyPassMan_Files\\config.json"
        else:
            config_file = "PyPassMan_Files/config.json"

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
            PyPassMan_init.window_prompt(
                "Update",
                "There is an update available, version: "
                + latest_version
                + "\n"
                + "You can download it with the installer or from github and read the patch notes there:\n"
                + "https://github.com/Obscurely/PyPassMan/releases",
            )


class PyPassManAcc:
    """
    Class with functions for the main form of the app (Login Form).
    """

    log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
    platform_separator = (
        Checker.check_platform()
    )  # Assigns either "/" or "\" depending on the platform
    # Common directories used in this functions
    program_accounts_dir = "PyPassMan_Files" + platform_separator + "accounts.json"
    user_accounts_dir = platform_separator + "user_accounts"
    # Common errors used in this functions
    app_acc_dir_not_found_error = "PyPassMan accounts dir does not exist"
    banned_chars_error = "banned chars in text"
    user_acc_dir_not_found_error = "user accounts dir does not exist"

    @classmethod
    def register_acc(cls, username: str, password: str):
        """
        Registers account for the app.

        :param username: Username for the new account.
        :param password: Password for the new account.
        :return: Returns "created account" if registering was successful else returns the error that occurred.
        """
        current_dir = os.getcwd()

        try:
            with open(cls.program_accounts_dir, "r") as f:
                accounts = json.load(f)  # Loads the PyPassMan accounts file
            # Logging line
            cls.log.debug_log(
                "Loaded the PyPassMan accounts file.", logger.get_lineno()
            )
        except FileNotFoundError:
            # Logging line
            cls.log.critical_log(
                cls.app_acc_dir_not_found_error + ".", logger.get_lineno()
            )
            return cls.app_acc_dir_not_found_error

        if aes.encrypt(username) in accounts:
            # Logging line
            cls.log.debug_log(
                f'Tried registering an account with username "{username}", but it already exists.',
                logger.get_lineno(),
            )
            return "username exists"
        elif username == "":
            # Logging line
            cls.log.debug_log(
                "Tried registering an account with empty username which is not allowed!",
                logger.get_lineno(),
            )
            return "username empty"
        elif Checker.check_chars(username) == cls.banned_chars_error:
            # Logging line
            cls.log.debug_log(
                f'Tried registering an account with username "{username}", but it contains banned '
                f"chars.",
                logger.get_lineno(),
            )
            return cls.banned_chars_error
        else:
            accounts[aes.encrypt(username)] = aes.encrypt(password)

            with open(cls.program_accounts_dir, "w", encoding="utf8") as f:
                json.dump(accounts, f, indent=4)  # Adds PyPassMan account to file
            # Logging line
            cls.log.debug_log(
                f'Successfully dumped account "{username}" in file!',
                logger.get_lineno(),
            )

            # Creates a new folder to store account's data
            try:
                os.chdir(current_dir + cls.user_accounts_dir)
            except NotADirectoryError:
                # Logging line
                cls.log.critical_log(
                    "User accounts dir does not exist!", logger.get_lineno()
                )
                return cls.user_acc_dir_not_found_error

            try:
                os.mkdir(username)
                # Logging line
                cls.log.debug_log(
                    f'Created a directory for account "{username}".',
                    logger.get_lineno(),
                )
            except FileExistsError:
                # Logging line
                cls.log.error_log(
                    f'Folder for the account "{username}" already exists!',
                    logger.get_lineno(),
                )
                return "acc folder already exists"

            # Generates encryption key in the account's dir
            os.chdir(
                current_dir + cls.user_accounts_dir + cls.platform_separator + username
            )
            aes.gen_keys()
            # Logging line
            cls.log.debug_log(
                f'Generated encryption keys for account "{username}".',
                logger.get_lineno(),
            )

            os.chdir(current_dir)

            # Logging line
            cls.log.debug_log(
                f'Successfully created account "{username}"!', logger.get_lineno()
            )
            return "created account"

    @classmethod
    def login(cls, username: str, password: str):
        """
        Login into app function that checks if login info is right.

        :param username: Username used for login.
        :param password: Password used for login.
        :return: Returns "login successful" if login was successful else returns the error that occurred.
        """
        try:
            with open(cls.program_accounts_dir, "r") as f:
                accounts = json.load(f)  # Loads PyPassMan accounts file
            # Logging line
            cls.log.debug_log(
                "Loaded the PyPassMan accounts file.", logger.get_lineno()
            )
        except FileNotFoundError:
            # Logging line
            cls.log.critical_log(
                cls.app_acc_dir_not_found_error + ".", logger.get_lineno()
            )
            return cls.app_acc_dir_not_found_error

        if aes.encrypt(username) in accounts:
            if accounts[aes.encrypt(username)] == aes.encrypt(password):
                # Logging line
                cls.log.debug_log(
                    f'Successfully logged into account "{username}".',
                    logger.get_lineno(),
                )
                # If username in file and password match, authorization is accepted
                return "login successful"
            else:
                # Logging line
                cls.log.debug_log(
                    f'Tried logging into account "{username}", but the password was incorrect.',
                    logger.get_lineno(),
                )
                return "incorrect password"
        else:
            # Logging line
            cls.log.debug_log(
                f'Tried logging into account "{username}", but it does not exist.',
                logger.get_lineno(),
            )
            return "account not exist"

    @classmethod
    def remove_acc(cls, username: str, password: str):
        """
        Remove app account function that checks if info is right and if so it removes the account.

        :param username: Username of account to remove.
        :param password: Password of account to remove.
        :return: Returns "account deleted" if account was deleted successfully else returns the error that occurred.
        """
        current_dir = os.getcwd()

        try:
            with open(cls.program_accounts_dir, "r") as f:
                accounts = json.load(f)  # Loads the PyPassMan accounts file
            # Logging line
            cls.log.debug_log(
                "Loaded the PyPassMan accounts file.", logger.get_lineno()
            )
        except FileNotFoundError:
            # Logging line
            cls.log.critical_log(
                cls.app_acc_dir_not_found_error + ".", logger.get_lineno()
            )
            return cls.app_acc_dir_not_found_error

        if aes.encrypt(username) not in accounts:
            # Logging line
            cls.log.debug_log(
                f'Tried removing account "{username}", but it does not exist.',
                logger.get_lineno(),
            )
            return "account with this username not exist"
        elif accounts[aes.encrypt(username)] != aes.encrypt(password):
            # Logging line
            cls.log.debug_log(
                f'Tried removing account "{username}", but the password was incorrect.',
                logger.get_lineno(),
            )
            return "password incorrect"
        elif accounts[aes.encrypt(username)] == aes.encrypt(password):
            # Deletes the json entry with the specific username in file
            del accounts[aes.encrypt(username)]

            with open(cls.program_accounts_dir, "w") as f:
                json.dump(accounts, f, indent=4)  # Dumps the new json in file
            # Logging line
            cls.log.debug_log(
                f'Successfully removed account "{username}" from file.',
                logger.get_lineno(),
            )

            # Deletes account's folder
            try:
                os.chdir(current_dir + cls.user_accounts_dir)
            except NotADirectoryError:
                # Logging line
                cls.log.critical_log(
                    "User accounts dir does not exist!", logger.get_lineno()
                )
                return cls.user_acc_dir_not_found_error
            try:
                shutil.rmtree(username)
            except FileNotFoundError:
                os.chdir(current_dir)
                # Logging line
                cls.log.warning_log(
                    f'The account folder for user "{username}" was not found, but the acc got deleted',
                    logger.get_lineno(),
                )
                return "user folder was not found"

            os.chdir(current_dir)
            return "account deleted"


class Locker:
    """
    Class with functions for user's Locker\n
    """

    log = logger.Logger(os.path.basename(__file__))  # Log object for making logs

    class AccFolders:
        """
        Locker functions related to account folders.
        """

        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        platform_separator = (
            Checker.check_platform()
        )  # Assigns either "/" or "\" depending on the platform
        # Common directories used in this functions
        user_accounts_dir = platform_separator + "user_accounts"
        file_extension = ".json"
        # Common errors used in this functions
        user_acc_dir_not_found_error = "user accounts dir does not exist"
        banned_chars_error = "banned chars in text"
        user_acc_folder_not_found_error = "user acc folder does not exist"
        folder_not_found_error = "folder not found"
        unknown_error = "unknown error occurred"

        def create_acc_folder(self, folder_name: str):
            """
            Function used in locker of a user to created account folders.

            :param folder_name: folder name for the new folder.
            :return: Returns "folder created" if folder was created successfully else return the error that occurred.
            """

            current_dir = os.getcwd()

            try:
                # Changes the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.critical_log(
                    "User's accounts dir does not exist!", logger.get_lineno()
                )
                return self.user_acc_dir_not_found_error

            if folder_name == "":
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried creating a folder with an empty name which is not '
                    f"allowed.",
                    logger.get_lineno(),
                )
                return "folder name can not be empty"
            elif Checker.check_chars(folder_name) == self.banned_chars_error:
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried creating a folder using OS banned chars which is not '
                    f"allowed.",
                    logger.get_lineno(),
                )
                return self.banned_chars_error

            file_name = folder_name + self.user + self.file_extension
            if file_name in str(os.listdir()):
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried creating folder "{folder_name}" which already exists.',
                    logger.get_lineno(),
                )
                return "folder already exists"
            else:
                # Creates a file and writes {} to it to make it loadable with json
                with open(file_name, "w") as f:
                    f.write("{}")

                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" successfully created acc folder "{folder_name}".',
                    logger.get_lineno(),
                )
                return "folder created"

        def get_acc_folders(self):
            """
            Gets the user's account folders.

            :return: Returns a string with the account folders of a user (it can empty).
            """

            current_dir = os.getcwd()

            try:
                # Changes dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.critical_log(
                    "User's accounts dir does not exist!", logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            all_acc_folder = os.listdir()
            folder_list = ""

            # Iterates the files in dir and adds them to a string followed by "/    "
            for acc_folder in all_acc_folder:
                if self.user in acc_folder and self.file_extension in acc_folder:
                    acc_folder = acc_folder.split(self.user + self.file_extension)[0]
                    folder_list += acc_folder + "/    "

            os.chdir(current_dir)
            # Logging line
            self.log.debug_log(
                f'Successfully got the list with folders of user "{self.user}".',
                logger.get_lineno(),
            )
            return folder_list

        def remove_acc_folder(self, folder: str):
            """
            Deletes the user's folder specified.

            :param folder: name of the folder to remove.
            :return: Returns "deleted acc folder" if the folder was deleted successfully else returns the error that
                     occurred.
            """

            current_dir = os.getcwd()

            try:
                # Changes the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.critical_log(
                    "User's accounts dir does not exist!", logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            file_name = folder + self.user + self.file_extension
            if (
                file_name not in str(os.listdir())
                or file_name == self.user + self.file_extension
            ):
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried deleting acc folder "{folder}" which does not exist.',
                    logger.get_lineno(),
                )
                os.chdir(current_dir)
                return self.folder_not_found_error
            elif file_name in str(os.listdir()):
                # Remove the accounts folder (json file) requested by user
                os.remove(file_name)
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" successfully removed acc folder "{folder}".',
                    logger.get_lineno(),
                )
                return "deleted acc folder"
            else:
                os.chdir(current_dir)
                # Logging line
                self.log.warning_log(
                    f'User "{self.user}" tried deleting folder "{folder}", but an unknown error '
                    f"occurred",
                    logger.get_lineno(),
                )
                return self.unknown_error

        def __init__(self, user):
            self.user = user

    class AccFoldersContent:
        """
        Locker functions related to account folders content.
        """

        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        platform_separator = (
            Checker.check_platform()
        )  # Assigns either "/" or "\" depending on the platform
        # Separators in file for writing more information on 1 line
        digit_separator = "///!@#$%^&*()\\\\\\"
        label_separator = "\\\\\\)(*&^%$#@!///"
        # Common directories used in this functions
        user_accounts_dir = platform_separator + "user_accounts"
        file_extension = ".json"
        # Common errors used in this functions
        folder_not_found_error = "folder not found"
        user_acc_folder_not_found_error = "user acc folder does not exist"
        unknown_error = "unknown error occurred"

        def add_acc_to_folder(
            self, label: str, folder: str, acc_username: str, acc_password: str
        ):
            """
            Adds the account to the specified folder.

            :param label: label/tag to show up in front of account.
            :param folder: folder to add the account to.
            :param acc_username: username for the account to add.
            :param acc_password: password for the account to add.
            :return: Returns "added acc to folder" if account was added successfully to the folder else returns the
                     error that occurred.
            """

            def get_digit(accounts_json: dict):
                """
                Gets the next account number, either 1 if there is no other account in the folder or the last account
                number in the folder + 1.

                :param accounts_json: the folder with the accounts.
                :return: Returns either the last account number + 1
                """
                # Tries to add 1 to the last account's number, if there is no acc it assigns the digit 1
                try:
                    last_digit = aes.decrypt(list(accounts_json.items())[-1][0])
                    acc_digit = int(last_digit.split(self.digit_separator)[0]) + 1
                    return acc_digit
                except IndexError:
                    acc_digit = 1
                    return acc_digit

            current_dir = os.getcwd()

            try:
                # Changes dir to the account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            file_name = folder + self.user + self.file_extension
            if (
                file_name not in str(os.listdir())
                or file_name == self.user + self.file_extension
            ):
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried adding an account to a non existing folder: "{folder}".',
                    logger.get_lineno(),
                )
                return self.folder_not_found_error
            elif folder == "":
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried adding an account to an empty name folder which is not '
                    f"possible to exist.",
                    logger.get_lineno(),
                )
                return "folder name can not be empty"
            elif self.digit_separator in acc_username:
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried adding an account containing the digit separator '
                    f"in the username which is not permitted.",
                    logger.get_lineno(),
                )
                return "username contains digit_separator"
            elif self.label_separator in acc_password:
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried adding an account containing the label separator '
                    f"in the username which is not permitted.",
                    logger.get_lineno(),
                )
                return "password contains label_separator"
            else:
                if label != "0":  # 0 Means no labels
                    with open(file_name, "r") as f:
                        accounts = json.load(f)
                    digit = get_digit(accounts)
                    self.log.debug_log(
                        f'Loaded the acc folder "{folder}" and the acc numbers.',
                        logger.get_lineno(),
                    )

                    # Concatenates the digit and username with the digit separator
                    # and the label and acc_password with label_separator
                    accounts[
                        aes.encrypt(str(digit) + self.digit_separator + acc_username)
                    ] = aes.encrypt(label + self.label_separator + acc_password)

                    with open(file_name, "w") as f:
                        json.dump(accounts, f, indent=4)  # Dumps the new acc folder
                        self.log.debug_log(
                            f'Successfully dumped the new account in folder "{folder}" '
                            f'of user "{self.user}".',
                            logger.get_lineno(),
                        )
                else:
                    with open(file_name, "r") as f:
                        accounts = json.load(f)
                    digit = get_digit(accounts)
                    self.log.debug_log(
                        f'Loaded the acc folder "{folder}" and the acc numbers.',
                        logger.get_lineno(),
                    )

                    # Only concatenates the digit with username with digit_separator
                    accounts[
                        aes.encrypt(str(digit) + self.digit_separator + acc_username)
                    ] = aes.encrypt(acc_password)

                    with open(file_name, "w") as f:
                        json.dump(accounts, f, indent=4)  # Dumps the new acc folder
                    # Logging line
                    self.log.debug_log(
                        f'Successfully dumped the new account in folder "{folder}" '
                        f'of user "{self.user}".',
                        logger.get_lineno(),
                    )

                os.chdir(current_dir)
                return "added acc to folder"

        def get_acc_in_folder(self, folder: str):
            """
            Gets the accounts in user's folder if any is present.

            :param folder: folder to get accounts in
            :return: Returns a formatted string with the accounts in the folder or if an error occurred it returns that
                     error.
            """

            current_dir = os.getcwd()

            try:
                # Changes the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            file_name = folder + self.user + self.file_extension
            if (
                file_name not in str(os.listdir())
                or file_name == self.user + self.file_extension
            ):
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User tried getting accounts in folder "{folder}" which does not exist',
                    logger.get_lineno(),
                )
                return self.folder_not_found_error
            elif file_name in str(os.listdir()):
                with open(file_name, "r") as f:
                    accounts = json.load(f)  # Loads the specified acc folder
                # Logging line
                self.log.debug_log(
                    f'Successfully loaded the acc folder "{folder}" of user "{self.user}".',
                    logger.get_lineno(),
                )
                accounts_list = ""
                # Checks for label and accordingly adds the account to accounts_list
                for username, password in accounts.items():
                    # If there is no label when splitting the string with label_separator it's length will be 1
                    if len(aes.decrypt(password).split(self.label_separator)) == 1:
                        digit = aes.decrypt(username).split(self.digit_separator)[0]
                        username = aes.decrypt(username).split(self.digit_separator)[-1]

                        accounts_list += (
                            digit
                            + ".\nusername: "
                            + username
                            + "\n"
                            + "password: "
                            + aes.decrypt(password)
                            + "\n\n"
                        )
                    else:
                        label = aes.decrypt(password).split(self.label_separator)[0]
                        password = aes.decrypt(password).split(self.label_separator)[-1]
                        digit = aes.decrypt(username).split(self.digit_separator)[0]
                        username = aes.decrypt(username).split(self.digit_separator)[-1]

                        accounts_list += (
                            digit
                            + "."
                            + label
                            + ":\n"
                            + "username: "
                            + username
                            + "\n"
                            + "password: "
                            + password
                            + "\n\n"
                        )
                # Logging line
                self.log.debug_log(
                    f'Successfully got a list with accounts in user "{self.user}" folder "{folder}".',
                    logger.get_lineno(),
                )
                os.chdir(current_dir)
                return accounts_list

        def remove_acc_in_folder(self, folder: str, number: str, account: str):
            """
            Removes an account from a folder.

            :param folder: folder to remove the account from.
            :param number: the number of the account to remove..
            :param account: the name of the account to remove.
            :return: Returns "account removed" if account was successfully removed else returns the error that occurred.
            """

            current_dir = os.getcwd()

            try:
                # Changes the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            file_name = folder + self.user + self.file_extension
            if (
                file_name not in str(os.listdir())
                or file_name == self.user + self.file_extension
            ):
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried removing an acc in folder "{folder}" which does not '
                    f"exist.",
                    logger.get_lineno(),
                )
                return self.folder_not_found_error
            elif file_name in str(os.listdir()):
                with open(file_name, "r") as f:
                    accounts = json.load(f)
                # Logging line
                self.log.debug_log(
                    f'Loaded accounts in user "{self.user}" folder "{folder}".',
                    logger.get_lineno(),
                )

                # Takes the account name encrypts and concatenates it to match with the entry in file
                account = aes.encrypt(number + self.digit_separator + account)

                if account not in accounts:
                    os.chdir(current_dir)
                    # Logging line
                    self.log.debug_log(
                        f'User "{self.user}" tried removing an account in folder "{folder}" which does '
                        f"not exist",
                        logger.get_lineno(),
                    )
                    return "account not found"
                else:
                    # Removes the specified accounts key from the dict
                    del accounts[account]

                    digit = 1
                    new_accounts = {}
                    # Recreates the acc folder in order to reorder the numbers
                    for username, password in accounts.items():
                        current_username = aes.decrypt(username).split(
                            self.digit_separator
                        )[1]
                        if digit == 1:
                            new_username = (
                                str(digit) + self.digit_separator + current_username
                            )
                            digit = 2
                        elif digit >= 2:
                            new_username = (
                                str(digit) + self.digit_separator + current_username
                            )
                            digit += 1

                        new_accounts[aes.encrypt(new_username)] = password

                    with open(file_name, "w") as f:
                        # Dumps the new acc folder
                        json.dump(new_accounts, f, indent=4)
                    # Logging line
                    self.log.debug_log(
                        f'Successfully remove the account from user "{self.user}" folder "{folder}".',
                        logger.get_lineno(),
                    )

                    os.chdir(current_dir)
                    return "account removed"
            else:
                os.chdir(current_dir)
                # Logging line
                self.log.warning_log(
                    f"An unknown error occurred while trying to delete an account from user "
                    f'"{self.user}" folder "{folder}".',
                    logger.get_lineno(),
                )
                return self.unknown_error

        def clear_acc_folder(self, folder: str):
            """
            Clears all the accounts in a folder (empties the folder).

            :param folder: folder to clear.
            :return: Returns "acc folder cleared" if folder was cleared successfully else returns the error that
                     occurred.
            """

            current_dir = os.getcwd()

            try:
                # Changes the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            file_name = folder + self.user + self.file_extension
            if (
                file_name not in str(os.listdir())
                or file_name == self.user + self.file_extension
            ):
                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'User "{self.user}" tried clearing acc folder "{folder}", but it does not exist.',
                    logger.get_lineno(),
                )
                return self.folder_not_found_error
            elif file_name in str(os.listdir()):
                # Writes to the specified file {} which cleans and it and makes it loadable as an empty dict
                with open(file_name, "w") as f:
                    f.write("{}")

                os.chdir(current_dir)
                # Logging line
                self.log.debug_log(
                    f'Successfully cleared user "{self.user}" acc folder "{folder}".',
                    logger.get_lineno(),
                )
                return "acc folder cleared"
            else:
                os.chdir(current_dir)
                # Logging line
                self.log.warning_log(
                    f'User "{self.user}" tried clearing acc folder "{folder}", but an unknown error '
                    f"occurred.",
                    logger.get_lineno(),
                )
                return self.unknown_error

        def __init__(self, user):
            self.user = user

    class AccManager:
        """
        Locker functions related to managing the account such as backup and restore.
        """

        log = logger.Logger(os.path.basename(__file__))  # Log object for making logs
        platform_separator = (
            Checker.check_platform()
        )  # Assigns either "/" or "\" depending on the platform
        # Separators in file for writing more information on 1 line
        digit_separator = "///!@#$%^&*()\\\\\\"
        label_separator = "\\\\\\)(*&^%$#@!///"
        # Common directories used in this functions
        user_accounts_dir = platform_separator + "user_accounts"
        file_extension = ".json"
        # Common errors used in this functions
        user_acc_folder_not_found_error = "user acc folder does not exist"

        def backup(self):
            """
            Backup all the accounts and folders of the current user to file on the desktop.

            :return: Returns nothing if backup was successful else returns the error that occurred.
            """

            current_dir = os.getcwd()

            # This gets the desktop path depending on platform
            if platform.system() == "Windows":
                desktop = os.path.join(
                    os.path.join(os.environ["USERPROFILE"]), "Desktop"
                )
            else:
                desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")

            try:
                # Change the dir to account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            all_acc_folder = os.listdir()
            folder_list = []

            # Checks if the file matches the requirements and adds it to the folder_list
            for acc_folder in all_acc_folder:
                if self.user in acc_folder and self.file_extension in acc_folder:
                    folder_list.append(acc_folder)

            acc_backup = ""
            temp_acc = ""
            for folder in folder_list:
                with open(folder, "r") as f:
                    temp = json.load(f)  # Loads every file in this temp value

                # For every file checks which accounts in that file have a label and which not and concatenates
                # the information of the account in a specific way to make it easier to iterate with regex
                for username, password in temp.items():
                    # When splitting a string with the label separator the length of the first item
                    # is 1 if there is no label
                    if len(aes.decrypt(password).split(self.label_separator)) == 1:
                        number = aes.decrypt(username).split(self.digit_separator)[0]
                        username = aes.decrypt(username).split(self.digit_separator)[1]
                        temp_acc += (
                            "number: <"
                            + number
                            + "> <--> username: <"
                            + username
                            + "> <--> "
                            + "password: <"
                            + aes.decrypt(password)
                            + ">,\n"
                        )
                    else:
                        label = aes.decrypt(password).split(self.label_separator)[0]
                        password = aes.decrypt(password).split(self.label_separator)[-1]
                        number = aes.decrypt(username).split(self.digit_separator)[0]
                        username = aes.decrypt(username).split(self.digit_separator)[1]
                        temp_acc += (
                            "number: <"
                            + number
                            + "> <--> label: <"
                            + label
                            + "> <--> username: <"
                            + username
                            + "> <--> "
                            + "password: <"
                            + password
                            + ">,\n"
                        )

                # Checks again if the file name is right and if it is the extension and the user's name are removed
                if self.user in folder and self.file_extension in folder:
                    folder = folder.split(self.user + self.file_extension)[0]

                # Adds the final product to the acc_backup string and spaces it out
                acc_backup += folder + ":\n" + temp_acc + "\n\n"
                # Empties the temp_acc value to make it available for next iteration
                temp_acc = ""

            os.chdir(desktop)

            file_name = self.user + "backup.txt"
            with open(file_name, "w") as f:
                # Writes the full backup to a file formatted as [user]+backup.txt
                f.write(acc_backup)

            # Logging line
            self.log.debug_log(
                f'Successfully backup all accounts of user "{self.user}".',
                logger.get_lineno(),
            )
            os.chdir(current_dir)

        def restore(self):
            """
            Restores the backup from the desktop if any in present.

            :return: Returns nothing if the account restore was successful else returns the error that occurred.
            """

            current_dir = os.getcwd()

            # This gets the desktop path depending of the platform
            if platform.system() == "Windows":
                desktop = os.path.join(
                    os.path.join(os.environ["USERPROFILE"]), "Desktop"
                )
            else:
                desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")

            os.chdir(desktop)

            # The file name that should be present on the desktop
            backup_file_name = self.user + "backup.txt"

            # Checks if the backup file exists on the desktop
            try:
                with open(backup_file_name, "r") as f:
                    backup_file = f.read()  # Loads the backup file if it exists
            except FileNotFoundError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" tried restoring a backup, but a backup.txt type file was not '
                    f"found on the desktop.",
                    logger.get_lineno(),
                )
                return "desktop no backup.txt"

            try:
                # Changes the dir to the account's dir
                os.chdir(
                    current_dir
                    + self.user_accounts_dir
                    + self.platform_separator
                    + self.user
                )
            except NotADirectoryError:
                # Logging line
                self.log.error_log(
                    f'User "{self.user}" dir is missing!', logger.get_lineno()
                )
                return self.user_acc_folder_not_found_error

            dir_files = os.listdir()
            # Removes all of the account's acc folders
            for each_file in dir_files:
                if self.user in each_file:
                    os.remove(each_file)
                    # Logging line
                    self.log.debug_log(
                        "Removed all of the present acc folders.", logger.get_lineno()
                    )

            # Splits the spaces in the backup file to get a list of each acc folder
            backup_file = backup_file.split("\n\n")

            folder_list = []
            # Uses regex to get a list of all the folder names
            for folder in backup_file:
                pattern = re.compile(r".*?(?=:)")
                try:
                    folder = pattern.findall(folder)[0]
                except IndexError:
                    pass

                if "\\n" in folder:
                    folder = folder.replace("\\n", "")
                if folder == "" or folder == "\n":
                    continue

                folder_list.append(folder)

            acc_content = []
            # Iterates the file to get content of each folder in the acc_content list
            for content in backup_file:
                content_index = backup_file.index(content)
                try:
                    folder_name = folder_list[content_index] + ":"
                except IndexError:
                    continue
                if folder_name in content:
                    content = content.replace(folder_name, "")
                    acc_content.append(content)
                else:
                    continue

            new_acc_content = []
            # Iterates over acc_content and remove all the \n
            for iteration in acc_content:
                iteration = iteration.replace("\n", "")
                new_acc_content.append(iteration)

            # The regex patterns for getting the needed content
            pattern_usernames = re.compile(r"(?<=username: <).*?(?=> <--)")
            pattern_passwords = re.compile(r"(?<= password: <).*?(?=>,)")
            pattern_label = re.compile(r"(?<=label: <).*?(?=> <--> username:)")
            pattern_number = re.compile(r"(?<=number: <).*?(?=> <--> )")
            pattern_make_acc_readable = re.compile(
                r"(?<=number:).*?(?= <--> password: <)"
            )
            pattern_acc_number = re.compile(r"(?<= <).*?(?=> <--> label:)")

            # Empty string to which the specified content will be added to
            username_list = ""
            password_list = ""
            label_list = ""
            number_list = ""
            acc_numbers_with_label = []

            each_acc_content = ""
            each_acc_numbers_with_label = ""
            # Iterates over every file and applies the regex
            for each in new_acc_content:
                usernames = pattern_usernames.findall(each)
                passwords = pattern_passwords.findall(each)
                labels = pattern_label.findall(each)
                numbers = pattern_number.findall(each)

                readable_acc = pattern_make_acc_readable.findall(each)
                for each_acc in readable_acc:
                    if "label:" in each_acc:
                        acc_number = pattern_acc_number.findall(each_acc)[0]
                        each_acc_numbers_with_label += acc_number + "&&"
                    else:
                        continue
                acc_numbers_with_label.append(each_acc_numbers_with_label)

                # Adds the content to the string lists separated by some separators
                for each_username in usernames:
                    username_list += "%<" + each_username + ">%"
                for password in passwords:
                    password_list += "!<" + password + ">!"
                for label in labels:
                    label_list += "#<" + label + ">#"
                for number in numbers:
                    number_list += "}<" + number + ">}!"

                # Concatenates the content together and separates the folder with &&
                each_acc_content += (
                    number_list + username_list + password_list + label_list + "&&"
                )

                # Empties the string list's content to make them available for next iteration
                username_list = ""
                password_list = ""
                label_list = ""
                number_list = ""
                each_acc_numbers_with_label = ""

            # Makes a list with the acc content for every file
            each_acc_content = each_acc_content.split("&&")

            # New regex pattern to find the needed data
            new_usernames_pattern = re.compile(r"(?<=%<).*?(?=>%)")
            new_passwords_pattern = re.compile(r"(?<=!<).*?(?=>!)")
            new_labels_pattern = re.compile(r"(?<=#<).*?(?=>#)")
            new_numbers_pattern = re.compile(r"(?<=}<).*?(?=>})")

            i = 0
            # Iterates over every file content and gets the needed data
            for full_acc in each_acc_content:
                new_usernames = new_usernames_pattern.findall(full_acc)
                new_passwords = new_passwords_pattern.findall(full_acc)
                new_labels = new_labels_pattern.findall(full_acc)
                new_numbers = new_numbers_pattern.findall(full_acc)

                # Based on this check the iteration stops
                try:
                    file_name = (
                        folder_list[i] + self.user + ".json"
                    )  # Complete file name
                except IndexError:
                    break

                # Creates file and loads it
                with open(file_name, "w") as f:
                    f.write("{}")
                with open(file_name, "r") as f:
                    accounts = json.load(f)

                # Splits the file content based on the number of iteration
                acc_numbers_for_label = acc_numbers_with_label[i].split("&&")

                x, y, z = 0, 0, 0
                # Based on iteration values decides if an account has or not a label
                for item in new_usernames:
                    if new_numbers[y] in acc_numbers_for_label:
                        accounts[
                            aes.encrypt(new_numbers[y] + self.digit_separator + item)
                        ] = aes.encrypt(
                            new_labels[z] + self.label_separator + new_passwords[x]
                        )
                        x += 1
                        y += 1
                        z += 1
                    else:
                        accounts[
                            aes.encrypt(new_numbers[y] + self.digit_separator + item)
                        ] = aes.encrypt(new_passwords[x])
                        x += 1
                        y += 1

                with open(file_name, "w") as f:
                    # Dumps the file data into the file
                    json.dump(accounts, f, indent=4)

                i += 1  # Increments the iteration

            # Logging line
            self.log.debug_log(
                f'Successfully restored the backup for user "{self.user}".',
                logger.get_lineno(),
            )
            os.chdir(current_dir)

        def __init__(self, user):
            self.user = user

    @classmethod
    def pass_gen(cls, length: str):
        """
        Generates a strong password with a specified length.

        :param length: the length for the password (max 2147483647).
        :return: Returns the password or "invalid length" if the input contains other chars then numbers.
        """

        i = 0
        password = ""

        # Checks if the length is an integer
        try:
            length = int(length)
        except ValueError:
            return "invalid length"

        # There are 3 type of chars and it generates a random number from 1 to 3 and based on that number
        # it chooses a random char from the category and adds it to the password string
        while i < length:
            char_type = random.randrange(1, 4)

            if char_type == 1:
                char_number = random.randrange(0, 52)
                password += string.ascii_letters[char_number]
            elif char_type == 2:
                char_number = random.randrange(0, 10)
                password += string.digits[char_number]
            elif char_type == 3:
                char_number = random.randrange(0, 32)
                password += string.punctuation[char_number]

            i += 1

        # Logging line
        cls.log.debug_log("Successfully generated a password.", logger.get_lineno())

        return password
