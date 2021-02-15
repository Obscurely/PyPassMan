import json
import os
import random
import string
import crypter
import re
from colorama import init, Fore

init(convert=True)

# Vars related to files
program_accounts_dir = 'accounts.json'
user_accounts_dir = '\\user_accounts'
file_extension = '.json'

# Some errors used more throughout the file
folder_not_found = Fore.RED + 'Folder does not exist, try again.' + Fore.WHITE
acc_folder_names_error = Fore.RED + 'Account folder names can not be empty, try again.' + Fore.WHITE
acc_names_error = Fore.RED + 'Accounts with empty usernames do not exist, try again with a different password.' \
                  + Fore.WHITE
passwords_error = Fore.RED + 'Accounts with empty passwords do not exist, try again with a different password.' \
                  + Fore.WHITE


def register_acc():
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'New username > 4 chars | 0 = Exit:' + Fore.WHITE, end=' ')
        username = input()
        if username == '0':
            loop_var = 1
            continue
        elif username == '':
            print(Fore.RED + 'Username can not be empty, try again with a different username.'
                  + Fore.WHITE)
            continue
        elif crypter.encode(username) in accounts:
            print(Fore.RED + 'An account with this username already exists, try again with another username'
                  + Fore.WHITE)
            continue
        print(Fore.BLUE + 'New password > 4 chars:' + Fore.WHITE, end=' ')
        password = input()
        if password == '':
            print(Fore.RED + 'Password can not be empty, try again with a different password.'
                  + Fore.WHITE)
            continue
        print(Fore.BLUE + 'Password again:' + Fore.WHITE, end=' ')
        again_password = input()
        print()  # Prints new line

        if password != again_password:
            print(Fore.RED + 'Passwords do not match!' + Fore.WHITE)
            continue
        elif password == again_password:
            loop_var = 1

        print('Are you sure you want to create a new account with username '
              + username + '? (yes/no):', end=' ')
        boolean = input()

        if boolean != 'yes':
            loop_var = 1
            continue

        print()  # Prints new line

        accounts[crypter.encode(username)] = crypter.encode(password)

        with open(program_accounts_dir, 'w') as f:
            json.dump(accounts, f, indent=4)

        print(Fore.GREEN + 'Successfully created account ' + username + '.' + Fore.WHITE)
    print('\n')  # Prints 2 new lines


def login():
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Username > 5 chars | 0 = Exit:' + Fore.WHITE, end=' ')
        username = input()
        if username == '':
            print(acc_names_error)
            continue
        if username == '0':
            loop_var = 1
            continue
        print(Fore.BLUE + 'Password > 5 chars:' + Fore.WHITE, end=' ')
        password = input()
        if password == '':
            print(passwords_error)
            continue
        print()  # Prints new line

        if crypter.encode(username) in accounts:
            if accounts[crypter.encode(username)] == crypter.encode(password):
                print(Fore.GREEN + 'Login successful.' + Fore.WHITE)
                print('\n')
                return ['login successful', username]
            else:
                print(Fore.RED + 'Password is incorrect!' + Fore.WHITE)
        else:
            print(Fore.RED + 'Username is incorrect!' + Fore.WHITE)
    print('\n')  # Prints 2 new lines


def remove_acc():
    current_dir = os.getcwd()
    with open(program_accounts_dir, 'r') as f:
        accounts = json.load(f)

    loop_var = 0
    while loop_var != 1:
        print(Fore.YELLOW + 'Username | 0 = Exit:' + Fore.WHITE, end=' ')
        username = input()
        if username == '0':
            loop_var = 1
            continue
        elif username == '':
            print(acc_names_error)
            continue
        elif crypter.encode(username) not in accounts:
            print(Fore.RED + 'An account with this username does not exist, try again.'
                  + Fore.WHITE)
            continue
        print(Fore.YELLOW + 'Password:', end=' ' + Fore.WHITE)
        password = input()
        print(Fore.YELLOW + 'Password again:' + Fore.WHITE, end=' ')
        password_again = input()
        print()  # Prints new line
        if password != password_again:
            print(Fore.RED + 'Passwords do not match, try again.' + Fore.WHITE)
            continue
        elif accounts[crypter.encode(username)] != crypter.encode(password):
            print(Fore.RED + 'Password is incorrect, try again.' + Fore.WHITE)
            continue
        print(Fore.YELLOW + 'Are you sure you want to delete account ' + username + '? (yes/no)'
              + Fore.WHITE, end=' ')
        boolean = input()
        print()  # Prints new line
        if boolean == 'yes':
            del accounts[crypter.encode(username)]

            with open(program_accounts_dir, 'w') as f:
                json.dump(accounts, f, indent=4)

            os.chdir(current_dir + user_accounts_dir)
            dir_files = os.listdir()
            for each_file in dir_files:
                if username in each_file:
                    os.remove(each_file)
            os.chdir(current_dir)

            print(Fore.GREEN + 'Successfully removed account ' + username + '.' + Fore.WHITE)
            loop_var = 1
        else:
            print(Fore.BLUE + 'Account did not get deleted.' + Fore.WHITE)
    print('\n')  # Prints 2 new lines


def create_acc_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Folder name | 0 = Exit:' + Fore.WHITE, end=' ')
        folder_name = input()
        print()  # Prints new line
        if folder_name == '0':
            loop_var = 1
            continue
        elif folder_name == '':
            print(Fore.RED + 'Folder name can not be empty, try again.' + Fore.WHITE)
            continue
        file_name = folder_name + user + file_extension
        if file_name in str(os.listdir()):
            print(Fore.RED + 'Folder already exists, try a different name.' + Fore.WHITE)
            continue

        with open(file_name, 'w') as f:
            f.write('{}')

        print(Fore.GREEN + 'Created folder ' + folder_name + '.' + Fore.WHITE)
        loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def get_acc_folders(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)
    all_acc_folder = os.listdir()

    print(Fore.CYAN + user + '\'s account folders:' + Fore.WHITE)

    for acc_folder in all_acc_folder:
        if user in acc_folder and file_extension in acc_folder:
            acc_folder = acc_folder.split(user + file_extension)[0]
            print(Fore.GREEN + acc_folder + ',' + Fore.WHITE, end=' ')

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def remove_acc_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Accounts folder to remove | 0 = Exit:' + Fore.WHITE)
        folder = input()
        if folder == '0':
            loop_var = 1
            continue
        elif folder == '':
            print(acc_folder_names_error)
            continue
        file_name = folder + user + file_extension

        if file_name not in str(os.listdir()):
            print(folder_not_found)
            continue
        else:
            print(Fore.YELLOW + 'Are you sure you want to delete accounts folder ' + folder
                  + '? (yes/no):', end=' ')
            boolean = input()
            print()  # Prints new line
            if boolean == 'yes':
                os.remove(file_name)
                print(Fore.GREEN + 'Remove acc folder ' + folder + '.' + Fore.WHITE)
                loop_var = 1
            else:
                loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def add_acc_to_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.YELLOW + 'Folder to add account to | 0 = Exit:' + Fore.WHITE, end=' ')
        folder = input()
        if folder == '0':
            loop_var = 1
            continue
        elif folder == '':
            print(acc_folder_names_error)
            continue

        file_name = folder + user + file_extension

        if file_name not in str(os.listdir()):
            print(folder_not_found)
            continue

        print(Fore.BLUE + 'Label for account (0 = None):' + Fore.WHITE, end=' ')
        label = input()
        print(Fore.BLUE + 'Username/email for the account:' + Fore.WHITE, end=' ')
        acc_username = input()
        print(Fore.BLUE + 'Password for the account:' + Fore.WHITE, end=' ')
        acc_password = input()
        print(Fore.BLUE + 'Type password again' + Fore.WHITE, end=' ')
        acc_password_again = input()
        print()  # Prints new line
        if acc_password != acc_password_again:
            print(Fore.RED + 'Passwords do not match, try again.' + Fore.WHITE)
            continue
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

                print(Fore.GREEN + 'Added acc ' + acc_username + ' to acc folder ' + folder + '.' + Fore.WHITE)
                loop_var = 1
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

                print(Fore.GREEN + 'Added acc ' + acc_username + ' to acc folder ' + folder + '.' + Fore.WHITE)
                loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def get_acc_in_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.YELLOW + 'Folder to get accounts in | 0 = Exit:' + Fore.WHITE, end=' ')
        folder = input()
        print()  # Prints new line
        if folder == '0':
            loop_var = 1
            continue
        elif folder == '':
            print(acc_folder_names_error)
            continue

        file_name = folder + user + file_extension
        if file_name not in str(os.listdir()):
            print(folder_not_found)
            continue

        with open(file_name, 'r') as f:
            accounts = json.load(f)

        for username, password in accounts.items():
            if len(crypter.decode(password).split('///\\')) == 1:
                digit = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[-1]
                print(Fore.BLUE + digit + '.\nusername: ' + username + '\n' + 'password: '
                      + crypter.decode(password) + '\n\n' + Fore.WHITE)

                loop_var = 1
            else:
                label = crypter.decode(password).split('///\\')[0]
                password = crypter.decode(password).split('///\\')[-1]
                digit = crypter.decode(username).split('.///|||///')[0]
                username = crypter.decode(username).split('.///|||///')[-1]

                print(Fore.BLUE + digit + '.' + label + ':\n' + 'username: ' + username + '\n' \
                      + 'password: ' + password + '\n\n' + Fore.WHITE)

                loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def remove_acc_in_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Folder to remove acc in | 0 = Exit:' + Fore.WHITE, end=' ')
        folder = input()
        if folder == '0':
            loop_var = 1
            continue
        elif folder == '':
            print(acc_folder_names_error)
            continue

        file_name = folder + user + file_extension
        if file_name not in str(os.listdir()):
            print(folder_not_found)
            continue

        with open(file_name, 'r') as f:
            accounts = json.load(f)

        print(Fore.BLUE + 'Account\'s number:' + Fore.WHITE, end=' ')
        number = input()
        print(Fore.BLUE + 'Account\'s username:' + Fore.WHITE, end=' ')
        account = input()
        if crypter.encode(account) not in accounts:
            print(Fore.RED + 'An account with username ' + account + ' was not found, try again.'
                  + Fore.WHITE)
        print(Fore.BLUE + 'Are you sure you want to delete account' + account
              + '? (yes/no):', end=' ')
        boolean = input()
        print()  # Prints new line

        if boolean == 'yes':
            account = crypter.encode(number + './//|||///' + account)

            if account not in accounts:
                os.chdir(current_dir)
                print(Fore.RED + 'Account ' + account + ' with number ' + number + ' was not found!' + Fore.WHITE)
                loop_var = 1
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

                print(Fore.GREEN + 'Removed acc ' + account + ' in acc folder ' + folder + '.' + Fore.WHITE)
                loop_var = 1
        else:
            loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def clear_acc_folder(user):
    current_dir = os.getcwd()
    os.chdir(current_dir + user_accounts_dir)

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Folder to clear accounts in | 0 = Exit:' + Fore.WHITE, end=' ')
        folder = input()
        if folder == '0':
            loop_var = 1
            continue
        elif folder == '':
            print(acc_folder_names_error)
            continue

        file_name = folder + user + file_extension
        if file_name not in str(os.listdir()):
            print(folder_not_found)
            continue

        print(Fore.BLUE + 'Are you sure you want to clear everything in ' + folder
              + '? (yes/no):', end=' ')
        boolean = input()

        if boolean == 'yes':
            with open(file_name, 'w') as f:
                f.write('{}')
            print(Fore.GREEN + 'Cleared all acc in acc folder' + folder + '.' + Fore.WHITE)
            loop_var = 1
        else:
            loop_var = 1

    os.chdir(current_dir)
    print('\n')  # Prints 2 new lines


def pass_gen():
    i = 0
    password = ''

    loop_var = 0
    while loop_var != 1:
        print(Fore.BLUE + 'Length:' + Fore.WHITE, end=' ')
        length = input()
        print()  # Prints new line
        try:
            length = int(length)
        except:
            print(Fore.RED + 'Please enter a valid value.' + Fore.WHITE)
            continue

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

        print(Fore.GREEN + 'Password: ' + password + Fore.WHITE)
        loop_var = 1

    print('\n')  # Prints 2 new lines


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
    print(Fore.BLUE + 'Saved everything in backup.txt (file is on the desktop).' + Fore.WHITE)
    print('\n')  # Prints 2 new lines

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
                accounts[crypter.encode(new_numbers[y] + './//|||///' + item)] = crypter.encode(
                    new_labels[z] + '///\\' + new_passwords[x])
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

# todo Future update: setup a paste bin for backups / access accounts over cloud when user exists
#   and sort functions using namespaces
