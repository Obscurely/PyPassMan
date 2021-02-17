import json
import os
import random
import string
import re
from others import crypter

# Vars related to files
program_accounts_dir = 'passmanager_files\\accounts.json'
user_accounts_dir = '\\user_accounts'
file_extension = '.json'


def register_acc(username, password):
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if crypter.encode(username) in accounts:
        return 'username exists'
    elif username == '':
        return 'username empty'
    else:
        accounts[crypter.encode(username)] = crypter.encode(password)

        with open(program_accounts_dir, 'w') as f:
            json.dump(accounts, f, indent=4)

        return 'created account'


def login(username, password):
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if crypter.encode(username) in accounts:
        if accounts[crypter.encode(username)] == crypter.encode(password):
            return 'login successful'
    else:
        return 'account not exist'


def remove_acc(username, password):
    current_dir = os.getcwd()
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    if crypter.encode(username) not in accounts:
        return 'account with this username not exist'
    elif accounts[crypter.encode(username)] != crypter.encode(password):
        return 'password incorrect'
    else:
        del accounts[crypter.encode(username)]

        with open(program_accounts_dir, 'w') as f:
            json.dump(accounts, f, indent=4)

        os.chdir(current_dir + user_accounts_dir)
        dir_files = os.listdir()
        for each_file in dir_files:
            if username in each_file:
                os.remove(each_file)
        os.chdir(current_dir)

        return 'account deleted'


def create_acc_folder(user, folder_name):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    if folder_name == '':
        os.chdir(current_dir)
        return 'folder name can not be empty'

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
    os.chdir(current_dir + user_accounts_dir)
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
    os.chdir(current_dir + user_accounts_dir)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()):
        os.chdir(current_dir)
        return 'folder not found'
    elif file_name in str(os.listdir()):
        os.remove(file_name)
        os.chdir(current_dir)
        return 'deleted acc folder'
    else:
        os.chdir(current_dir)
        return 'unknown error occurred'


def add_acc_to_folder(user, label, folder, acc_username, acc_password):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()):
        os.chdir(current_dir)
        return 'folder not found'
    elif folder == '':
        os.chdir(current_dir)
        return 'folder name can not be empty'
    else:
        if label != '0':
            with open(file_name, 'r') as f:
                accounts = json.load(f)
            try:
                last_digit = crypter.decode(list(accounts.items())[-1][0])
                digit = int(last_digit.split('.///|||///')[0]) + 1
            except:
                digit = 1

            accounts[crypter.encode(str(digit) + './//|||///' + acc_username)] = crypter.encode(label + '///\\' + acc_password)

            with open(file_name, 'w') as f:
                json.dump(accounts, f, indent=4)
        else:
            with open(file_name, 'r') as f:
                accounts = json.load(f)
            try:
                last_digit = crypter.decode(list(accounts.items())[-1][0])
                digit = int(last_digit.split('.///|||///')[0]) + 1
            except:
                digit = 1
            accounts[crypter.encode(str(digit) + './//|||///' + acc_username)] = crypter.encode(acc_password)

            with open(file_name, 'w') as f:
                json.dump(accounts, f, indent=4)

        os.chdir(current_dir)
        return 'added acc to folder'


def get_acc_in_folder(user, folder):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return 'folder not found'
    elif file_name in str(os.listdir()):
        with open(file_name, 'r') as f:
            accounts = json.load(f)

        accounts_list = ''

        for username, password in accounts.items():
            if len(crypter.decode(password).split('///\\')) == 1:
                digit = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[-1]
                accounts_list += digit + '.\nusername: ' + username + '\n' + 'password: ' \
                                 + crypter.decode(password) + '\n\n'

            else:
                label = crypter.decode(password).split('///\\')[0]
                password = crypter.decode(password).split('///\\')[-1]
                digit = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[-1]

                accounts_list += digit + '.' + label + ':\n' + 'username: ' + username + '\n' \
                                 + 'password: ' + password + '\n\n'

        os.chdir(current_dir)
        return accounts_list


def remove_acc_in_folder(user, folder, number, account):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    file_name = folder + user + file_extension

    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return 'folder not found'
    elif file_name in str(os.listdir()):
        with open(file_name, 'r') as f:
            accounts = json.load(f)

        account = crypter.encode(number + './//|||///' + account)

        if account not in accounts:
            os.chdir(current_dir)
            return 'account not found'
        else:

            del accounts[account]

            digit = 1
            new_accounts = {}
            for username, password in accounts.items():
                current_username = crypter.decode(username).split('.')[1]
                if digit == 1:
                    new_username = str(digit) + './//|||///' + current_username
                    digit = 2
                elif digit >= 2:
                    new_username = str(digit) + './//|||///' + current_username
                    digit += 1

                new_accounts[crypter.encode(new_username)] = password

            with open(file_name, 'w') as f:
                json.dump(new_accounts, f, indent=4)

            os.chdir(current_dir)
            return 'account removed'

    else:
        os.chdir(current_dir)
        return 'unknown error occurred'


def clear_acc_folder(user, folder):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    file_name = folder + user + file_extension
    if file_name not in str(os.listdir()) or file_name == user + file_extension:
        os.chdir(current_dir)
        return 'folder not found'
    elif file_name in str(os.listdir()):
        with open(file_name, 'w') as f:
            f.write('{}')

        os.chdir(current_dir)
        return 'acc folder cleared'
    else:
        os.chdir(current_dir)
        return 'unknown error occurred'


def pass_gen(length):
    i = 0
    password = ''

    try:
        length = int(length)
    except:
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
    os.chdir(current_dir + user_accounts_dir)
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
            if len(crypter.decode(password).split('///\\')) == 1:
                number = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[1]
                temp_acc += 'number: <' + number + '> <--> username: <' + username + '> <--> ' + 'password: <' \
                            + crypter.decode(password) + '>,\n'
            else:
                label = crypter.decode(password).split('///\\')[0]
                password = crypter.decode(password).split('///\\')[-1]
                number = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[1]
                temp_acc += 'number: <' + number + '> <--> label: <' + label + '> <--> username: <' + username + '> <--> ' \
                            + 'password: <' + password + '>,\n'

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

    os.chdir(current_dir + user_accounts_dir)

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
    pattern_make_acc_checkable = re.compile(r'(?<=number:).*?(?= <--> password: <)')
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

        checkable_acc = pattern_make_acc_checkable.findall(each)
        for each_acc in checkable_acc:
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
                accounts[crypter.encode(new_numbers[y] + './//|||///' + item)] = crypter.encode(new_labels[z] + '///\\' + new_passwords[x])
                x += 1
                y += 1
                z += 1
            else:
                accounts[crypter.encode(new_numbers[y] + './//|||///' + item)] = crypter.encode(new_passwords[x])
                x += 1
                y += 1

        with open(file_name, 'w') as f:
            json.dump(accounts, f, indent=4)

        i += 1

    os.chdir(current_dir)
