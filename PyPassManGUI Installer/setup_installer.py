import os
import window_init
import requests
import re
import wget
import zipfile
import winshell
import shutil
import threading
import pythoncom
import subprocess
import stat
from PyQt6.QtWidgets import QMessageBox

temp_folder = os.path.normpath(winshell.desktop() + os.sep + os.pardir) + '\\AppData\\Local\\Temp'


def get_app():
    current_dir = os.getcwd()

    content = requests.get('https://pastebin.com/f077vm8L').text
    pattern = re.compile(r'(?<===--&gt;&gt;).*?(?=&lt;--==)')
    release_link = pattern.findall(content)[0]

    os.chdir(temp_folder)
    os.mkdir('PyPassMan')
    os.chdir(temp_folder + '\\PyPassMan')

    try:
        os.remove('PyPassMan.GUI.Stable.Release.zip')
    except FileNotFoundError:
        pass

    path = temp_folder + '\\PyPassMan\\PyPassMan.GUI.Stable.Release.zip'
    wget.download(release_link, path)

    os.chdir(current_dir)


def unzip_app():
    current_dir = os.getcwd()
    os.chdir(temp_folder + '\\PyPassMan')

    try:
        shutil.rmtree('PyPassMan')
    except FileNotFoundError:
        pass

    with zipfile.ZipFile('PyPassMan.GUI.Stable.Release.zip', 'r') as zip_ref:
        zip_ref.extractall('PyPassMan')

    os.chdir(current_dir)


def copy_files_to_dir(directory):
    folder_path = temp_folder + '\\PyPassMan\\PyPassMan'
    os.chdir(folder_path)

    shutil.copytree(folder_path, directory)


def create_shortcut(directory, boolean):
    desktop = winshell.desktop()
    start_menu = winshell.start_menu()

    if boolean == 1:
        pythoncom.CoInitialize()
        winshell.CreateShortcut(
            Path=os.path.join(desktop, "PyPassMan.lnk"),
            Target=directory + '\\PyPassMan.exe',
            StartIn=directory,
            Description='PyPassMan'
        )
    elif boolean == 2:
        pythoncom.CoInitialize()
        winshell.CreateShortcut(
            Path=os.path.join(start_menu, "PyPassMan.lnk"),
            Target=directory + '\\PyPassMan.exe',
            StartIn=directory,
            Description='PyPassMan'
        )
    elif boolean == 3:
        pythoncom.CoInitialize()
        winshell.CreateShortcut(
            Path=os.path.join(desktop, "PyPassMan.lnk"),
            Target=directory + '\\PyPassMan.exe',
            StartIn=directory,
            Description='PyPassMan'
        )

        pythoncom.CoInitialize()
        winshell.CreateShortcut(
            Path=os.path.join(start_menu, "PyPassMan.lnk"),
            Target=directory + '\\PyPassMan.exe',
            StartIn=directory,
            Description='PyPassMan'
        )
    elif boolean == 0:
        pass


def cleanup():
    os.chdir(temp_folder)

    os.chmod('PyPassMan', stat.S_IWRITE)

    try:
        shutil.rmtree('PyPassMan', ignore_errors=True)
    except:
        pass

    try:
        os.remove('PyPassMan')
    except:
        pass


def get_app_size():
    content = requests.get('https://pastebin.com/f077vm8L').text
    pattern = re.compile(r'(?<=--==&gt;&gt;).*?(?=&lt;==--)')
    size = pattern.findall(content)[0]
    return size


def get_app_version():
    content = requests.get('https://pastebin.com/f077vm8L').text
    pattern = re.compile(r'(?<=-=-=&gt;&gt;).*?(?=&lt;=-=-)')
    version = pattern.findall(content)[0]
    return version


def uninstall(directory):
    try:
        del_dir = directory
        install_folder_name = directory.split('\\')[-1]
        directory = os.path.normpath(directory + os.sep + os.pardir)
        os.chdir(directory)

    except:
        return 'not a directory'

    os.chmod(del_dir, stat.S_IWRITE)

    try:
        shutil.rmtree(install_folder_name, ignore_errors=True)
    except:
        return 'error deleting a file'

    try:
        os.remove(install_folder_name)
    except:
        pass

    desktop = winshell.desktop()
    start_menu = winshell.start_menu()

    os.chdir(desktop)
    try:
        os.remove('PyPassMan.lnk')
    except:
        pass

    os.chdir(start_menu)
    try:
        os.remove('PyPassMan.lnk')
    except:
        pass


def setup():
    installer_first_form = window_init.InstallerFirstWindow()
    installer_second_form = window_init.InstallerSecondWindow()

    install_path = ''

    def start_uninstall():
        if installer_first_form.brUnins_dirC.isChecked():
            uninstall_path = 'C:\\PyPassMan'
        elif installer_first_form.brUnins_dirCProgramFiles.isChecked():
            uninstall_path = 'C:\\Program Files\\PyPassMan'
        elif installer_first_form.brUnins_CustomLocation.isChecked():
            uninstall_path = installer_first_form.Unins_CustomLocationInput.text()

        response = uninstall(uninstall_path)

        if response == 'not a directory':
            error = QMessageBox()
            error.setText('Not a valid directory!')
            error.exec()
        elif response == 'error deleting a file':
            error = QMessageBox()
            error.setText('Error while deleting a file, please refer to github page for how to manually uninstall!')
            error.exec()
        else:
            uninstalled = QMessageBox()
            uninstalled.setText('Successfully uninstalled the program!')
            uninstalled.exec()

    def validate_install():
        if installer_first_form.brDirC.isChecked():
            install_path = 'C:\\PyPassMan'
        elif installer_first_form.brDirCProgramFiles.isChecked():
            install_path = 'C:\\Program Files\\PyPassMan'
        elif installer_first_form.brCustomLocation.isChecked():
            install_path = installer_first_form.CustomLocationInput.text()

        installer_first_form.close()
        installer_second_form.OutputText.setPlainText('Install directory: ' + install_path)
        installer_second_form.show()

        def start_install():
            if installer_second_form.checkDesktopShortcut.isChecked() and installer_second_form.checkStartMenuShortcut.isChecked():
                boolean = 3
            elif installer_second_form.checkDesktopShortcut.isChecked():
                boolean = 1
            elif installer_second_form.checkStartMenuShortcut.isChecked():
                boolean = 2
            else:
                boolean = 0

            installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n')
            get_app()

            installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release.\n'
                                                          'Finished downloading PyPassMan.\n'
                                                          'Unzipping release...\n')
            unzip_app()

            installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                          'Finished downloading PyPassMan.\n'
                                                          'Unzipping release...\n'
                                                          'Finished unzipping release.\n'
                                                          'Copying files to requested directory...\n')
            copy_files_to_dir(install_path)
            installer_second_form.progressBar.setProperty('value', 40)

            if boolean == 1:
                installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                              'Finished downloading PyPassMan.\n'
                                                              'Unzipping release...\n'
                                                              'Finished unzipping release.\n'
                                                              'Copying files to requested directory...\n'
                                                              'Finished copying files to requested directory.\n'
                                                              'Creating desktop shortcut for app...\n')
                create_shortcut(install_path, boolean)
            elif boolean == 2:
                installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                              'Finished downloading PyPassMan.\n'
                                                              'Unzipping release...\n'
                                                              'Finished unzipping release.\n'
                                                              'Copying files to requested directory...\n'
                                                              'Finished copying files to requested directory.\n'
                                                              'Creating start menu shortcut for app...\n')
                create_shortcut(install_path, boolean)
            elif boolean == 3:
                installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                              'Finished downloading PyPassMan.\n'
                                                              'Unzipping release...\n'
                                                              'Finished unzipping release.\n'
                                                              'Copying files to requested directory...\n'
                                                              'Finished copying files to requested directory.\n'
                                                              'Creating desktop and start menu shortcut for app...\n')
                create_shortcut(install_path, boolean)
            elif boolean == 0:
                pass

            installer_second_form.progressBar.setProperty('value', 60)

            installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                          'Finished downloading PyPassMan.\n'
                                                          'Unzipping release...\n'
                                                          'Finished unzipping release.\n'
                                                          'Copying files to requested directory...\n'
                                                          'Finished copying files to requested directory.\n'
                                                          'Creating desktop shortcut for app...\n'
                                                          'Finished creating desktop shortcut for app.\n'
                                                          'Performing cleanup...\n')
            cleanup()
            installer_second_form.progressBar.setProperty('value', 80)

            installer_second_form.OutputText.setPlainText('Downloading latest PyPassMan release...\n'
                                                          'Finished downloading PyPassMan.\n'
                                                          'Unzipping release...\n'
                                                          'Finished unzipping release.\n'
                                                          'Copying files to requested directory...\n'
                                                          'Finished copying files to requested directory.\n'
                                                          'Creating desktop shortcut for app...\n'
                                                          'Finished creating desktop shortcut for app.\n'
                                                          'Performing cleanup...\n'
                                                          'Cleanup finished.\n'
                                                          'PyPassMan was successfully installed!\n')
            installer_second_form.progressBar.setProperty('value', 100)

            installer_second_form.checkRunAfterInstall.setEnabled(True)
            installer_second_form.bFinish.setEnabled(True)
            installer_second_form.checkStartMenuShortcut.setEnabled(False)
            installer_second_form.checkDesktopShortcut.setEnabled(False)
            installer_second_form.bInstall.setEnabled(False)

        start_install_thread = threading.Thread(target=start_install)

        def start():
            start_install_thread.start()
            start_install_thread.join()

        def validate_finish():
            if installer_second_form.checkRunAfterInstall.isChecked():
                os.chdir(install_path)
                installer_second_form.close()
                subprocess.call(['PyPassMan.exe'])
            else:
                installer_second_form.close()

        installer_second_form.bInstall.clicked.connect(start)
        installer_second_form.bFinish.clicked.connect(validate_finish)

    installer_first_form.SpaceRequiredLabel.setText('Space Required: ' + get_app_size())
    installer_first_form.VersionLabel.setText('Version: ' + get_app_version())
    installer_first_form.bInstall.clicked.connect(validate_install)
    installer_first_form.bClose.clicked.connect(installer_first_form.close)
    installer_first_form.bUninstall.clicked.connect(start_uninstall)
    return installer_first_form
