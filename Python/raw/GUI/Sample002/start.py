# UI Command: pyuic5 -x untitled.ui -o ui_untitled.py
# Installer Command: pyinstaller -F ui_untitled.py

from PyQt5 import QtWidgets
from controller import MainWindow
import sys


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())