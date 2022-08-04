# UI Command: pyuic5 -x untitled.ui -o ui_untitled.py
# Installer Command: pyinstaller -F start.py

from PyQt5 import QtWidgets
from controller import MainWindow
import sys

# import in advance for pyinstaller package
from PyQt5.QtWidgets import QFileDialog
import numpy as np
import csv

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())