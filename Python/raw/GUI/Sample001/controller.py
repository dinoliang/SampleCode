from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5 import QtCore

from ui_untitled import Ui_MainWindow
import sys
import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.pushButton_Start.clicked.connect(self.buttonClick_Start)
        self.ui.pushButton_InputFolder.clicked.connect(self.buttonClick_InputFolder)
        self.ui.pushButton_OutputFolder.clicked.connect(self.buttonClick_OutputFolder)
        self.ui.pushButton_Condition.clicked.connect(self.buttonClick_Condition)
        return

    def buttonClick_Start(self):
        textWidth = self.ui.lineEdit_Width.text()
        print("Image Width: {:d}".format(np.int64(int(textWidth, 10))))

        textHeight = self.ui.lineEdit_Height.text()
        print("Image Height: {:d}".format(np.int64(int(textHeight, 10))))

        textX = self.ui.lineEdit_X.text()
        print("X: {:d}".format(np.int64(int(textX, 10))))

        textY = self.ui.lineEdit_Y.text()
        print("Y: {:d}".format(np.int64(int(textY, 10))))

        textROIWidth = self.ui.lineEdit_ROIWidth.text()
        print("ROI Width: {:d}".format(np.int64(int(textROIWidth, 10))))

        textROIHeight = self.ui.lineEdit_ROIHeight.text()
        print("ROI Height: {:d}".format(np.int64(int(textROIHeight, 10))))

        textColumnIndex = self.ui.lineEdit_ColumnIndex.text()
        print("Column Index: {:d}".format(np.int64(int(textColumnIndex, 10))))

        textRowIndex = self.ui.lineEdit_RowIndex.text()
        print("Row Index: {:d}".format(np.int64(int(textRowIndex, 10))))

        textFileCounts = self.ui.lineEdit_FileCounts.text()
        print("File Counts: {:d}".format(np.int64(int(textFileCounts, 10))))

        textFileTimestamp = self.ui.lineEdit_FileTimestamp.text()
        print("File Timestamp: {}".format(textFileTimestamp))

        return

    def buttonClick_InputFolder(self):
        input_Folder = QFileDialog.getExistingDirectory(self, 'Choose Input Folder', '/home/dino/IMX586_Bin/')
        self.ui.lineEdit_InputFolder.setText(input_Folder)
        return

    def buttonClick_OutputFolder(self):
        output_Folder = QFileDialog.getExistingDirectory(self, 'Choose Output Folder', '/home/dino/RawShared/Output/')
        self.ui.lineEdit_OutputFolder.setText(output_Folder)
        return

    def buttonClick_Condition(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        CSV_fileName, _ = QFileDialog.getOpenFileName(self, 'Choose Condition CSV', '', 'CSV File (*.csv)', options=options)
        self.ui.lineEdit_Condition.setText(CSV_fileName)
        return
