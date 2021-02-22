import sys
from others import window_init
from others import PyPassMan_init
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    login_form = window_init.LoginWindow()
    login_form.show()
    login_form.bRegister.clicked.connect(PyPassMan_init.register)
    login_form.bLogin.clicked.connect(PyPassMan_init.login)
    login_form.bRemoveAccount.clicked.connect(PyPassMan_init.remove_acc)
    PyPassMan_init.check_first_run()
    app.exec()
    PyPassMan_init.check_version()


if __name__ == '__main__':
    main()
