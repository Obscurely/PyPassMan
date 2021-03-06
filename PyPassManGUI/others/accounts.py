import json
import os
import random
import string
import re
import shutil
import platform
from others import aes

# Platform check (for file location)
if platform.system() == "Windows":
    platform_separator = "\\"
else:
    platform_separator = "/"

# Files directories and extensions
program_accounts_dir = "PyPassMan_Files" + platform_separator + "accounts.json"
user_accounts_dir = platform_separator + "user_accounts"
file_extension = ".json"

# Text separator vars (used when storing and reading json files etc)
digit_separator = "///!@#$%^&*()\\\\\\"
label_separator = "\\\\\\)(*&^%$#@!///"

# Most used errors
folder_not_found_error = "folder not found"
unknown_error = "unknown error occurred"
banned_chars_error = "banned chars in text"
app_acc_dir_not_found_error = "PyPassMan accounts dir does not exist"
user_acc_dir_not_found_error = "user accounts dir does not exist"
user_acc_folder_not_found_error = "user acc folder does not exist"


def check_chars(text: str):
    # This are char not supported by os as file names
    banned_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for char in banned_chars:
        if char in text:
            return banned_chars_error
    return "Good"


def register_acc(username: str, password: str):
    current_dir = os.getcwd()

    try:
        with open(program_accounts_dir, "r") as f:
            accounts = json.load(f)  # Loads the PyPassMan accounts file
    except FileNotFoundError:
        return app_acc_dir_not_found_error

    if aes.encrypt(username) in accounts:
        return "username exists"
    elif username == "":
        return "username empty"
    elif check_chars(username) == banned_chars_error:
        return banned_chars_error
    else:
        accounts[aes.encrypt(username)] = aes.encrypt(password)

        with open(program_accounts_dir, "w", encoding="utf8") as f:
            json.dump(accounts, f, indent=4)  # Adds PyPassMan account to file

        # Creates a new folder to store account's data
        try:
            os.chdir(current_dir + user_accounts_dir)
        except NotADirectoryError:
            return user_acc_dir_not_found_error

        try:
            os.mkdir(username)
        except FileExistsError:
            return "acc folder already exists"

        # Generates encryption key in the account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + username)
        aes.gen_keys()

        os.chdir(current_dir)
        return "created account"


def login(username: str, password: str):
    try:
        with open(program_accounts_dir, "r") as f:
            accounts = json.load(f)  # Loads PyPassMan accounts file
    except FileNotFoundError:
        return app_acc_dir_not_found_error

    if aes.encrypt(username) in accounts:
        if accounts[aes.encrypt(username)] == aes.encrypt(password):
            # If username in file and password match, authorization is accepted
            return "login successful"
        else:
            return "incorrect password"
    else:
        return "account not exist"


def remove_acc(username: str, password: str):
    current_dir = os.getcwd()

    try:
        with open(program_accounts_dir, "r") as f:
            accounts = json.load(f)  # Loads the PyPassMan accounts file
    except FileNotFoundError:
        return app_acc_dir_not_found_error

    if aes.encrypt(username) not in accounts:
        return "account with this username not exist"
    elif accounts[aes.encrypt(username)] != aes.encrypt(password):
        return "password incorrect"
    elif accounts[aes.encrypt(username)] == aes.encrypt(password):
        # Deletes the json entry with the specific username in file
        del accounts[aes.encrypt(username)]

        with open(program_accounts_dir, "w") as f:
            json.dump(accounts, f, indent=4)  # Dumps the new json in file

        # Deletes account's folder
        try:
            os.chdir(current_dir + user_accounts_dir)
        except NotADirectoryError:
            return user_acc_dir_not_found_error
        try:
            shutil.rmtree(username)
        except FileNotFoundError:
            return "user folder was not found"

        os.chdir(current_dir)
        return "account deleted"


def create_acc_folder(user: str, folder_name: str):
    current_dir = os.getcwd()

    try:
        # Changes the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_dir_not_found_error

    if folder_name == "":
        os.chdir(current_dir)
        return "folder name can not be empty"
    elif check_chars(folder_name) == banned_chars_error:
        os.chdir(current_dir)
        return banned_chars_error

    file_name = folder_name + user + file_extension
    if file_name in str(os.listdir()):
        os.chdir(current_dir)
        return "folder already exists"
    else:
        # Creates a file and writes {} to it to make it loadable with json
        with open(file_name, "w") as f:
            f.write("{}")

        os.chdir(current_dir)
        return "folder created"


def get_acc_folders(user: str):
    current_dir = os.getcwd()

    try:
        # Changes dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    all_acc_folder = os.listdir()
    folder_list = ""

    # Iterates to files in dir and adds them do a string followed by "/    "
    for acc_folder in all_acc_folder:
        if user in acc_folder and file_extension in acc_folder:
            acc_folder = acc_folder.split(user + file_extension)[0]
            folder_list += acc_folder + "/    "

    os.chdir(current_dir)
    return folder_list


def remove_acc_folder(user: str, folder: str):
    current_dir = os.getcwd()

    try:
        # Changes the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found_error
    elif file_name in str(os.listdir()):
        # Remove the accounts folder (json file) requested by user
        os.remove(file_name)
        os.chdir(current_dir)
        return "deleted acc folder"
    else:
        os.chdir(current_dir)
        return unknown_error


def add_acc_to_folder(
    user: str, label: str, folder: str, acc_username: str, acc_password: str
):
    def get_digit(accounts_json):
        # Tries to add 1 to the last account's number, if there is no acc it assigns the digit 1
        try:
            last_digit = aes.decrypt(list(accounts_json.items())[-1][0])
            acc_digit = int(last_digit.split(digit_separator)[0]) + 1
            return acc_digit
        except IndexError:
            acc_digit = 1
            return acc_digit

    current_dir = os.getcwd()

    try:
        # Changes dir to the account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found_error
    elif folder == "":
        os.chdir(current_dir)
        return "folder name can not be empty"
    elif digit_separator in acc_username:
        os.chdir(current_dir)
        return "username contains digit_separator"
    elif label_separator in acc_password:
        os.chdir(current_dir)
        return "password contains label_separator"
    else:
        if label != "0":  # 0 Means no labels
            with open(file_name, "r") as f:
                accounts = json.load(f)
            digit = get_digit(accounts)

            # Concatenates the digit and username with the digit separator
            # and the label and acc_password with label_separator
            accounts[
                aes.encrypt(str(digit) + digit_separator + acc_username)
            ] = aes.encrypt(label + label_separator + acc_password)

            with open(file_name, "w") as f:
                json.dump(accounts, f, indent=4)  # Dumps the new acc folder
        else:
            with open(file_name, "r") as f:
                accounts = json.load(f)
            digit = get_digit(accounts)

            # Only concatenates the digit with username with digit_separator
            accounts[
                aes.encrypt(str(digit) + digit_separator + acc_username)
            ] = aes.encrypt(acc_password)

            with open(file_name, "w") as f:
                json.dump(accounts, f, indent=4)  # Dumps the new acc folder

        os.chdir(current_dir)
        return "added acc to folder"


def get_acc_in_folder(user: str, folder: str):
    current_dir = os.getcwd()

    try:
        # Changes the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found_error
    elif file_name in str(os.listdir()):
        with open(file_name, "r") as f:
            accounts = json.load(f)  # Loads the specified acc folder

        accounts_list = ""
        # Checks for label and accordingly adds the account to accounts_list
        for username, password in accounts.items():
            # If there is no label when splitting the string with label_separator it's length will be 1
            if len(aes.decrypt(password).split(label_separator)) == 1:
                digit = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[-1]

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
                label = aes.decrypt(password).split(label_separator)[0]
                password = aes.decrypt(password).split(label_separator)[-1]
                digit = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[-1]

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

        os.chdir(current_dir)
        return accounts_list


def remove_acc_in_folder(user: str, folder: str, number: str, account: str):
    current_dir = os.getcwd()

    try:
        # Changes the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found_error
    elif file_name in str(os.listdir()):
        with open(file_name, "r") as f:
            accounts = json.load(f)

        # Takes the account name encrypts and concatenates it to match with the entry in file
        account = aes.encrypt(number + digit_separator + account)

        if account not in accounts:
            os.chdir(current_dir)
            return "account not found"
        else:
            # Removes the specified accounts key from the dict
            del accounts[account]

            digit = 1
            new_accounts = {}
            # Recreates the acc folder in order to reorder the numbers
            for username, password in accounts.items():
                current_username = aes.decrypt(username).split(digit_separator)[1]
                if digit == 1:
                    new_username = str(digit) + digit_separator + current_username
                    digit = 2
                elif digit >= 2:
                    new_username = str(digit) + digit_separator + current_username
                    digit += 1

                new_accounts[aes.encrypt(new_username)] = password

            with open(file_name, "w") as f:
                # Dumps the new acc folder
                json.dump(new_accounts, f, indent=4)

            os.chdir(current_dir)
            return "account removed"
    else:
        os.chdir(current_dir)
        return unknown_error


def clear_acc_folder(user: str, folder: str):
    current_dir = os.getcwd()

    try:
        # Changes the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found_error
    elif file_name in str(os.listdir()):
        # Writes to the specified file {} which cleans and it and makes it loadable as an empty dict
        with open(file_name, "w") as f:
            f.write("{}")

        os.chdir(current_dir)
        return "acc folder cleared"
    else:
        os.chdir(current_dir)
        return unknown_error


def pass_gen(length: str):
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

    return password


def backup(user: str):
    current_dir = os.getcwd()

    # This gets the desktop path depending on platform
    if platform.system() == "Windows":
        desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")

    try:
        # Change the dir to account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + user)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    all_acc_folder = os.listdir()
    folder_list = []

    # Checks if the file matches the requirements and adds it to the folder_list
    for acc_folder in all_acc_folder:
        if user in acc_folder and file_extension in acc_folder:
            folder_list.append(acc_folder)

    acc_backup = ""
    temp_acc = ""
    for folder in folder_list:
        with open(folder, "r") as f:
            temp = json.load(f)  # Loads every file in this temp value

        # For every file checks which accounts in that file have a label and which not
        # and concatenates the information of which account in a specific way to make it easier to iterate with regex
        for username, password in temp.items():
            # When splitting a string with the label separator the length of the first item
            # is 1 if there is no label
            if len(aes.decrypt(password).split(label_separator)) == 1:
                number = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[1]
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
                label = aes.decrypt(password).split(label_separator)[0]
                password = aes.decrypt(password).split(label_separator)[-1]
                number = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[1]
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

        # Checks again if the file name is right and if it is ir remove the extension and the user's name from it
        if user in folder and file_extension in folder:
            folder = folder.split(user + file_extension)[0]

        # Adds the final product to the acc_backup string and spaces it out
        acc_backup += folder + ":\n" + temp_acc + "\n\n"
        # Empties the temp_acc value to make it available for next iteration
        temp_acc = ""

    os.chdir(desktop)

    file_name = user + "backup.txt"
    with open(file_name, "w") as f:
        # Writes the full backup to a file formatted as [user]+backup.txt
        f.write(acc_backup)

    os.chdir(current_dir)


def restore(username: str):
    current_dir = os.getcwd()

    # This gets the desktop path depending of the platform
    if platform.system() == "Windows":
        desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    else:
        desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")

    os.chdir(desktop)

    # The file name that should be present on the desktop
    backup_file_name = username + "backup.txt"

    # Checks if the backup file exists on the desktop
    try:
        with open(backup_file_name, "r") as f:
            backup_file = f.read()  # Loads the backup file if it exists
    except FileNotFoundError:
        return "desktop no backup.txt"

    try:
        # Changes the dir to the account's dir
        os.chdir(current_dir + user_accounts_dir + platform_separator + username)
    except NotADirectoryError:
        return user_acc_folder_not_found_error

    dir_files = os.listdir()
    # Removes all of the account's acc folders
    for each_file in dir_files:
        if username in each_file:
            os.remove(each_file)

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
    pattern_make_acc_readable = re.compile(r"(?<=number:).*?(?= <--> password: <)")
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
            file_name = folder_list[i] + username + ".json"  # Complete file name
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
                    aes.encrypt(new_numbers[y] + digit_separator + item)
                ] = aes.encrypt(new_labels[z] + label_separator + new_passwords[x])
                x += 1
                y += 1
                z += 1
            else:
                accounts[
                    aes.encrypt(new_numbers[y] + digit_separator + item)
                ] = aes.encrypt(new_passwords[x])
                x += 1
                y += 1

        with open(file_name, "w") as f:
            # Dumps the file data into the file
            json.dump(accounts, f, indent=4)

        i += 1  # Increments the iteration

    os.chdir(current_dir)
