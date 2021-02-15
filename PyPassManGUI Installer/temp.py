import os
import winshell
import shutil

temp_folder = os.path.normpath(winshell.desktop() + os.sep + os.pardir) + '\\AppData\\Local\\Temp'
os.chdir(temp_folder)


shutil.rmtree('test.txt')

