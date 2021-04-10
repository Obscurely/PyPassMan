import sys
from others import window_init, PyPassMan_init, accounts, logger
from PyQt6.QtWidgets import QApplication


def main():
    """
    Main code of the app.

    :return: Nothing.
    """
    logger.Logger.create_log_file()
    app = QApplication(sys.argv)
    login_form = window_init.LoginWindow()
    # Initialized style_manager here because it doesn't work for some reasons inside the function
    style_manager_form = window_init.StyleManagerWindow()
    login_form.bRegister.clicked.connect(PyPassMan_init.MainForm.register)
    login_form.bLogin.clicked.connect(PyPassMan_init.MainForm.login)
    login_form.bRemoveAccount.clicked.connect(PyPassMan_init.MainForm.remove_acc)
    login_form.bStyleManager.clicked.connect(
        lambda: PyPassMan_init.MainForm.style_manager(style_manager_form)
    )
    login_form.show()
    # Checks for first run for knowing to generate encryption keys or not
    accounts.Checker.check_first_run()
    app.exec()
    # Prompts user after closing if there is a new version
    accounts.Checker.check_version()


if __name__ == "__main__":
    main()
