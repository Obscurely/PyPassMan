import accounts
from colorama import init, Fore

init(convert=True)


def after_login(username):
    print(Fore.GREEN + 'Welcome to your locker ' + username + '!' + Fore.WHITE)

    loop_var = 0
    while loop_var != 1:
        print(Fore.LIGHTBLUE_EX + '1 = Create Acc Folder | 2 = List Acc Folder | 3 = Remove Acc Folder'
              + ' | 4 = Add Acc to Folder\n5 = Get Acc in Folder | 6 = Remove Acc in Folder'
              + ' | 7 = Clear Acc in Folder | 8 = Generate Strong Pass\n9 = Backup | 10 = Restore | 0 = Exit:' + Fore.WHITE, end=' ')
        try:
            var = int(input())
            print()  # Prints new line

        except:
            print(Fore.RED + 'Please input a valid value' + Fore.WHITE)

        if var == 1:
            accounts.create_acc_folder(username)
        elif var == 2:
            accounts.get_acc_folders(username)
        elif var == 3:
            accounts.remove_acc_folder(username)
        elif var == 4:
            accounts.add_acc_to_folder(username)
        elif var == 5:
            accounts.get_acc_in_folder(username)
        elif var == 6:
            accounts.remove_acc_in_folder(username)
        elif var == 7:
            accounts.clear_acc_folder(username)
        elif var == 8:
            accounts.pass_gen()
        elif var == 9:
            accounts.backup(username)
        elif var == 10:
            response = accounts.restore(username)
            if response == 'desktop no backup.txt':
                print(Fore.RED + 'Backup.txt was not found on desktop!')
            else:
                print(Fore.GREEN + 'Successfully restored backup!')
        elif var == 0:
            exit('User asked to do so')
            loop_var = 1


loop_var = 0
while loop_var != 1:
    print(Fore.LIGHTBLUE_EX + '1 = Login | 2 = Register | 3 = Remove Acc | 0 = Exit :'
          + Fore.WHITE, end=' ')
    try:
        opt_var = int(input())
        print()  # Prints new line
    except:
        print(Fore.RED + 'Please input a valid value' + Fore.WHITE)
        continue

    if opt_var == 1:
        var = accounts.login()

        try:
            if var[0] == 'login successful':
                after_login(var[1])
        except:
            continue

    if opt_var == 2:
        accounts.register_acc()
    elif opt_var == 3:
        accounts.remove_acc()
    elif opt_var == 0:
        exit('User asked to do so')

# todo add some comments for easier to understand code
# todo after everything is finished and ready to upload version on github use python code style
