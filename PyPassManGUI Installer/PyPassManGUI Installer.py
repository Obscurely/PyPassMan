import sys
from setup_installer import *
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    form = setup()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()
