import json
import os
import random
import string
import re
import shutil
from others import aes

# Vars related to files
program_accounts_dir = 'PyPassMan_Files\\accounts.json'
user_accounts_dir = '\\user_accounts'
file_extension = '.json'

# separator vars
digit_separator = './//|||///'
label_separator = '///\\'

# error vars
folder_not_found = 'folder not found'
unknown_error = 'unknown error occurred'
banned_chars_error = 'banned chars in text'


def check_chars(text):
    banned_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in banned_chars:
        if char in text:
            return banned_chars_error
    return 'Good'


def register_acc(username, password):
    current_dir = os.getcwd()
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if aes.encrypt(username) in accounts:
        return 'username exists'
    elif username == '':
        return 'username empty'
    elif check_chars(username) == banned_chars_error:
        return banned_chars_error
    else:
        accounts[aes.encrypt(username)] = aes.encrypt(password)

        with open(program_accounts_dir, 'w', encoding='utf8') as f:
            json.dump(accounts, f, indent=4)

        os.chdir(current_dir + user_accounts_dir)
        os.mkdir(username)
        os.chdir(current_dir + user_accounts_dir + '\\' + username)
        aes.gen_keys()
        os.chdir(current_dir)

        return 'created account'


def login(username, password):
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if aes.encrypt(username) in accounts:
        if accounts[aes.encrypt(username)] == aes.encrypt(password):
            return 'login successful'
        else:
            return 'incorrect password'
    else:
        return 'account not exist'


def remove_acc(username, password):
    current_dir = os.getcwd()
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if aes.encrypt(username) not in accounts:
        return 'account with this username not exist'
    elif accounts[aes.encrypt(username)] != aes.encrypt(password):
        return 'password incorrect'
    else:
        del accounts[aes.encrypt(username)]

        with open(program_accounts_dir, 'w') as f:
            json.dump(accounts, f, indent=4)

        os.chdir(current_dir + user_accounts_dir)
        shutil.rmtree(username)
        os.chdir(current_dir)

        return 'account deleted'


def create_acc_folder(user, folder_name):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    if folder_name == '':
        os.chdir(current_dir)
        return 'folder name can not be empty'
    elif check_chars(folder_name) == banned_chars_error:
        os.chdir(current_dir)
        return banned_chars_error

    file_name = folder_name + user + file_extension
    if file_name in str(os.listdir()):
        os.chdir(current_dir)
        return 'folder already exists'
    else:
        with open(file_name, 'w') as f:
            f.write('{}')
            os.chdir(current_dir)
            return 'folder created'


def get_acc_folders(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)
    all_acc_folder = os.listdir()

    folder_list = ''

    for acc_folder in all_acc_folder:
        if user in acc_folder and file_extension in acc_folder:
            acc_folder = acc_folder.split(user + file_extension)[0]
            folder_list += acc_folder + '/    '

    os.chdir(current_dir)
    return folder_list


def remove_acc_folder(user, folder):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found
    elif file_name in str(os.listdir()):
        os.remove(file_name)
        os.chdir(current_dir)
        return 'deleted acc folder'
    else:
        os.chdir(current_dir)
        return unknown_error


def add_acc_to_folder(user, label, folder, acc_username, acc_password):
    def get_digit(accounts_json):
        try:
            last_digit = aes.decrypt(list(accounts_json.items())[-1][0])
            acc_digit = int(last_digit.split(digit_separator)[0]) + 1
            return acc_digit
        except IndexError:
            acc_digit = 1
            return acc_digit

    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()):
        os.chdir(current_dir)
        return folder_not_found
    elif folder == '':
        os.chdir(current_dir)
        return 'folder name can not be empty'
    else:
        if label != '0':
            with open(file_name, 'r') as f:
                accounts = json.load(f)
            digit = get_digit(accounts)

            accounts[aes.encrypt(str(digit) + digit_separator + acc_username)] = aes.encrypt(
                label + label_separator + acc_password)

            with open(file_name, 'w') as f:
                json.dump(accounts, f, indent=4)
        else:
            with open(file_name, 'r') as f:
                accounts = json.load(f)
            digit = get_digit(accounts)

            accounts[aes.encrypt(str(digit) + digit_separator + acc_username)] = aes.encrypt(acc_password)

            with open(file_name, 'w') as f:
                json.dump(accounts, f, indent=4)

        os.chdir(current_dir)
        return 'added acc to folder'


def get_acc_in_folder(user, folder):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found
    elif file_name in str(os.listdir()):
        with open(file_name, 'r') as f:
            accounts = json.load(f)

        accounts_list = ''

        for username, password in accounts.items():
            if len(aes.decrypt(password).split(label_separator)) == 1:
                digit = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[-1]
                accounts_list += digit + '.\nusername: ' + username + '\n' + 'password: ' \
                    + aes.decrypt(password) + '\n\n'

            else:
                label = aes.decrypt(password).split(label_separator)[0]
                password = aes.decrypt(password).split(label_separator)[-1]
                digit = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[-1]

                accounts_list += digit + '.' + label + ':\n' + 'username: ' + username + '\n' \
                    + 'password: ' + password + '\n\n'

        os.chdir(current_dir)
        return accounts_list


def remove_acc_in_folder(user, folder, number, account):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found
    elif file_name in str(os.listdir()):
        with open(file_name, 'r') as f:
            accounts = json.load(f)

        account = aes.encrypt(number + digit_separator + account)

        if account not in accounts:
            os.chdir(current_dir)
            return 'account not found'
        else:

            del accounts[account]

            digit = 1
            new_accounts = {}
            for username, password in accounts.items():
                current_username = aes.decrypt(username).split(digit_separator)[1]
                if digit == 1:
                    new_username = str(digit) + digit_separator + current_username
                    digit = 2
                elif digit >= 2:
                    new_username = str(digit) + digit_separator + current_username
                    digit += 1

                new_accounts[aes.encrypt(new_username)] = password

            with open(file_name, 'w') as f:
                json.dump(new_accounts, f, indent=4)

            os.chdir(current_dir)
            return 'account removed'

    else:
        os.chdir(current_dir)
        return unknown_error


def clear_acc_folder(user, folder):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return folder_not_found
    elif file_name in str(os.listdir()):
        with open(file_name, 'w') as f:
            f.write('{}')

        os.chdir(current_dir)
        return 'acc folder cleared'
    else:
        os.chdir(current_dir)
        return unknown_error


def pass_gen(length):
    i = 0
    password = ''

    try:
        length = int(length)
    except ValueError:
        return 'invalid length'

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


def backup(user):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir + '\\' + user)
    all_acc_folder = os.listdir()

    folder_list = []

    for acc_folder in all_acc_folder:
        if user in acc_folder and file_extension in acc_folder:
            folder_list.append(acc_folder)

    acc_backup = ''
    temp_acc = ''

    for folder in folder_list:
        with open(folder, 'r') as f:
            temp = json.load(f)

        for username, password in temp.items():
            if len(aes.decrypt(password).split(label_separator)) == 1:
                number = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[1]
                temp_acc += 'number: <' + number + '> <--> username: <' + username + '> <--> ' + 'password: <' \
                            + aes.decrypt(password) + '>,\n'
            else:
                label = aes.decrypt(password).split(label_separator)[0]
                password = aes.decrypt(password).split(label_separator)[-1]
                number = aes.decrypt(username).split(digit_separator)[0]
                username = aes.decrypt(username).split(digit_separator)[1]
                temp_acc += 'number: <' + number + '> <--> label: <' + label + '> <--> username: <' + username \
                            + '> <--> ' + 'password: <' + password + '>,\n'

        if user in folder and file_extension in folder:
            folder = folder.split(user + file_extension)[0]

        acc_backup += folder + ':\n' + temp_acc + '\n\n'
        temp_acc = ''

    os.chdir(desktop)

    file_name = user + 'backup.txt'
    with open(file_name, 'w') as f:
        f.write(acc_backup)

    os.chdir(current_dir)


def restore(username):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    current_dir = os.getcwd()
    os.chdir(desktop)

    backup_file_name = username + 'backup.txt'
    try:
        with open(backup_file_name, 'r') as f:
            backup_file = f.read()

    except FileNotFoundError:
        return 'desktop no backup.txt'

    os.chdir(current_dir + user_accounts_dir + '\\' + username)

    dir_files = os.listdir()
    for each_file in dir_files:
        if username in each_file:
            os.remove(each_file)

    backup_file = backup_file.split('\n\n')
    folder_list = []

    for folder in backup_file:
        pattern = re.compile(r'.*?(?=:)')
        try:
            folder = pattern.findall(folder)[0]
        except IndexError:
            pass

        if '\\n' in folder:
            folder = folder.replace('\\n', '')
        if folder == '' or folder == '\n':
            continue

        folder_list.append(folder)

    acc_content = []

    for content in backup_file:
        content_index = backup_file.index(content)
        try:
            folder_name = folder_list[content_index] + ':'
        except IndexError:
            continue
        if folder_name in content:
            content = content.replace(folder_name, '')
            acc_content.append(content)
        else:
            continue

    new_acc_content = []
    for iteration in acc_content:
        iteration = iteration.replace('\n', '')
        new_acc_content.append(iteration)

    pattern_usernames = re.compile(r'(?<=username: <).*?(?=> <--)')
    pattern_passwords = re.compile(r'(?<= password: <).*?(?=>,)')
    pattern_label = re.compile(r'(?<=label: <).*?(?=> <--> username:)')
    pattern_number = re.compile(r'(?<=number: <).*?(?=> <--> )')
    pattern_make_acc_readable = re.compile(r'(?<=number:).*?(?= <--> password: <)')
    pattern_acc_number = re.compile(r'(?<= <).*?(?=> <--> label:)')

    username_list = ''
    password_list = ''
    label_list = ''
    number_list = ''
    acc_numbers_with_label = []

    each_acc_content = ''
    each_acc_numbers_with_label = ''

    for each in new_acc_content:
        usernames = pattern_usernames.findall(each)
        passwords = pattern_passwords.findall(each)
        labels = pattern_label.findall(each)
        numbers = pattern_number.findall(each)

        readable_acc = pattern_make_acc_readable.findall(each)
        for each_acc in readable_acc:
            if 'label:' in each_acc:
                acc_number = pattern_acc_number.findall(each_acc)[0]
                each_acc_numbers_with_label += acc_number + '&&'
            else:
                continue
        acc_numbers_with_label.append(each_acc_numbers_with_label)

        for each_username in usernames:
            username_list += '%<' + each_username + '>%'
        for password in passwords:
            password_list += '!<' + password + '>!'
        for label in labels:
            label_list += '#<' + label + '>#'
        for number in numbers:
            number_list += '}<' + number + '>}!'
        each_acc_content += number_list + username_list + password_list + label_list + '&&'

        username_list = ''
        password_list = ''
        label_list = ''
        number_list = ''
        each_acc_numbers_with_label = ''

    each_acc_content = each_acc_content.split('&&')

    new_usernames_pattern = re.compile(r'(?<=%<).*?(?=>%)')
    new_passwords_pattern = re.compile(r'(?<=!<).*?(?=>!)')
    new_labels_pattern = re.compile(r'(?<=#<).*?(?=>#)')
    new_numbers_pattern = re.compile(r'(?<=}<).*?(?=>})')
    i = 0
    for full_acc in each_acc_content:
        new_usernames = new_usernames_pattern.findall(full_acc)
        new_passwords = new_passwords_pattern.findall(full_acc)
        new_labels = new_labels_pattern.findall(full_acc)
        new_numbers = new_numbers_pattern.findall(full_acc)

        try:
            file_name = folder_list[i] + username + '.json'
        except IndexError:
            break

        with open(file_name, 'w') as f:
            f.write('{}')
        with open(file_name, 'r') as f:
            accounts = json.load(f)

        acc_numbers_for_label = acc_numbers_with_label[i].split('&&')
        x, y, z = 0, 0, 0
        for item in new_usernames:
            if new_numbers[y] in acc_numbers_for_label:
                accounts[aes.encrypt(new_numbers[y] + digit_separator + item)] = aes.encrypt(
                    new_labels[z] + label_separator + new_passwords[x])
                x += 1
                y += 1
                z += 1
            else:
                accounts[aes.encrypt(new_numbers[y] + digit_separator + item)] = aes.encrypt(new_passwords[x])
                x += 1
                y += 1

        with open(file_name, 'w') as f:
            json.dump(accounts, f, indent=4)

        i += 1

    os.chdir(current_dir)
