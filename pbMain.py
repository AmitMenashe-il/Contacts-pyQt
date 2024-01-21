import sys
from PyQt5.QtWidgets import QApplication
from pbGUI import MainWindow


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == '__main__':
    run()
