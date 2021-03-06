import sys
from others import window_init
from others import PyPassMan_init
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    login_form = window_init.LoginWindow()
    # Initialized style_manager here because it doesn't work for some reasons inside the function
    style_manager_form = window_init.StyleManagerWindow()
    login_form.bRegister.clicked.connect(PyPassMan_init.register)
    login_form.bLogin.clicked.connect(PyPassMan_init.login)
    login_form.bRemoveAccount.clicked.connect(PyPassMan_init.remove_acc)
    login_form.bStyleManager.clicked.connect(
        lambda: PyPassMan_init.style_manager(style_manager_form)
    )
    login_form.show()
    # Checks for first run for knowing to generate encryption keys or not
    PyPassMan_init.check_first_run()
    app.exec()
    # Prompts user after closing if there is a new version
    PyPassMan_init.check_version()


if __name__ == "__main__":
    main()
