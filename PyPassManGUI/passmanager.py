import sys
from others import window_init
from others import passmanager_init
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    login_form = window_init.LoginWindow()
    login_form.show()
    login_form.bRegister.clicked.connect(passmanager_init.register)
    login_form.bLogin.clicked.connect(passmanager_init.login)
    login_form.bRemoveAccount.clicked.connect(passmanager_init.remove_acc)
    app.exec()


if __name__ == '__main__':
    main()

# todo add a yes/no prompt when doing important stuff like deleting or registering account
