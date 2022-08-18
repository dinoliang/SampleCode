from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5 import QtCore

from ui_untitled import Ui_MainWindow
import sys
import numpy as np
import csv
import os

sys.path.append('/home/dino/PythonShared/raw/')
import channelrowparse_zett as zettmain
import channelrowparse_pdaf as pdafmain
import channelrowparse_pixel as pixelmain


class MainWindow(QtWidgets.QMainWindow):
    input_Folder = ''
    output_Folder = ''
    condition_Array = ''
    evaluation_Item = 0

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

        #Select Evaluation
        self.ui.comboBox_Evaluate.addItems(['QE', 'PDAF', 'Pixel'])
        self.ui.comboBox_Evaluate.currentIndexChanged.connect(self.onComboBoxChanged)
        self.ShowAllUI()
        self.HideUIbyQE()
        return

    # UI Display
    def ShowAllUI(self):
        self.ui.label_Width.setHidden(False)
        self.ui.lineEdit_Width.setHidden(False)

        self.ui.label_Height.setHidden(False)
        self.ui.lineEdit_Height.setHidden(False)

        self.ui.label_X.setHidden(False)
        self.ui.lineEdit_X.setHidden(False)

        self.ui.label_Y.setHidden(False)
        self.ui.lineEdit_Y.setHidden(False)

        self.ui.label_ROIWidth.setHidden(False)
        self.ui.lineEdit_ROIWidth.setHidden(False)

        self.ui.label_ROIHeight.setHidden(False)
        self.ui.lineEdit_ROIHeight.setHidden(False)

        self.ui.label_ColumnIndex.setHidden(False)
        self.ui.lineEdit_ColumnIndex.setHidden(False)

        self.ui.label_RowIndex.setHidden(False)
        self.ui.lineEdit_RowIndex.setHidden(False)

        self.ui.label_RowIndex_2.setHidden(False)
        self.ui.lineEdit_RowIndex_2.setHidden(False)

        self.ui.label_FileCounts.setHidden(False)
        self.ui.lineEdit_FileCounts.setHidden(False)

        self.ui.label_FileTimestamp.setHidden(False)
        self.ui.lineEdit_FileTimestamp.setHidden(False)

        self.ui.lineEdit_InputFolder.setHidden(False)
        self.ui.pushButton_InputFolder.setHidden(False)

        self.ui.lineEdit_OutputFolder.setHidden(False)
        self.ui.pushButton_OutputFolder.setHidden(False)

        self.ui.lineEdit_Condition.setHidden(False)
        self.ui.pushButton_Condition.setHidden(False)

        self.ui.checkBox_AYABin.setHidden(False)

        self.ui.label_RowIndex.setText('Row Index:')
        return

    def HideUIbyQE(self):
        self.ui.label_RowIndex_2.setHidden(True)
        self.ui.lineEdit_RowIndex_2.setHidden(True)
        self.ui.checkBox_AYABin.setHidden(True)
        return

    def HideUIbyPDAF(self):
        self.ui.checkBox_AYABin.setHidden(True)
        self.ui.label_RowIndex.setText('Row(Gb3) Index:')
        self.ui.label_RowIndex_2.setText('Row(B3) Index:')
        return

    def HideUIbyPixel(self):
        self.ui.label_ColumnIndex.setHidden(True)
        self.ui.lineEdit_ColumnIndex.setHidden(True)

        self.ui.label_RowIndex.setHidden(True)
        self.ui.lineEdit_RowIndex.setHidden(True)

        self.ui.label_RowIndex_2.setHidden(True)
        self.ui.lineEdit_RowIndex_2.setHidden(True)
        return

    # Botton Action
    def buttonClick_Start(self):
        if self.ui.lineEdit_Width.isVisible():
            try:
                textWidth = self.ui.lineEdit_Width.text()
                print("Image Width: {:d}".format(np.int64(int(textWidth, 10))))
            except ValueError as error:
                print(error)
            else:
                pass
            finally:
                pass

        if self.ui.lineEdit_Height.isVisible():
            textHeight = self.ui.lineEdit_Height.text()
            print("Image Height: {:d}".format(np.int64(int(textHeight, 10))))

        if self.ui.lineEdit_X.isVisible():
            textX = self.ui.lineEdit_X.text()
            print("X: {:d}".format(np.int64(int(textX, 10))))

        if self.ui.lineEdit_Y.isVisible():
            textY = self.ui.lineEdit_Y.text()
            print("Y: {:d}".format(np.int64(int(textY, 10))))

        if self.ui.lineEdit_ROIWidth.isVisible():
            textROIWidth = self.ui.lineEdit_ROIWidth.text()
            print("ROI Width: {:d}".format(np.int64(int(textROIWidth, 10))))

        if self.ui.lineEdit_ROIHeight.isVisible():
            textROIHeight = self.ui.lineEdit_ROIHeight.text()
            print("ROI Height: {:d}".format(np.int64(int(textROIHeight, 10))))

        if self.ui.lineEdit_ColumnIndex.isVisible():
            textColumnIndex = self.ui.lineEdit_ColumnIndex.text()
            print("Column Index: {:d}".format(np.int64(int(textColumnIndex, 10))))

        if self.ui.lineEdit_RowIndex.isVisible():
            textRowIndex = self.ui.lineEdit_RowIndex.text()
            print("Row Index: {:d}".format(np.int64(int(textRowIndex, 10))))

        if self.ui.lineEdit_RowIndex_2.isVisible():
            textRow2Index = self.ui.lineEdit_RowIndex_2.text()
            print("Row2 Index: {:d}".format(np.int64(int(textRow2Index, 10))))

        if self.ui.lineEdit_FileCounts.isVisible():
            textFileCounts = self.ui.lineEdit_FileCounts.text()
            print("File Counts: {:d}".format(np.int64(int(textFileCounts, 10))))

        if self.ui.lineEdit_FileTimestamp.isVisible():
            textFileTimestamp = self.ui.lineEdit_FileTimestamp.text()
            print("File Timestamp: {}".format(textFileTimestamp))

        if self.ui.checkBox_AYABin.isVisible():
            bAYABin = self.ui.checkBox_AYABin.isChecked()
            print("Is AYA Bin: {}".format(bAYABin))

        print(self.input_Folder)
        print(self.output_Folder)
        print(self.condition_Array)

        if self.evaluation_Item == 0: #QE
            zettmain.SetParameters( nWidth=np.int64(int(textWidth, 10)), \
                                    nHeight=np.int64(int(textHeight, 10)), \
                                    nX=np.int64(int(textX, 10)), \
                                    nY=np.int64(int(textY, 10)), \
                                    nROI_W=np.int64(int(textROIWidth, 10)), \
                                    nROI_H=np.int64(int(textROIHeight, 10)), \
                                    nColIndex=np.int64(int(textColumnIndex, 10)), \
                                    nRowIndex=np.int64(int(textRowIndex, 10)), \
                                    nFileCounts=np.int64(int(textFileCounts, 10)), \
                                    FileTimeStamp=textFileTimestamp, \
                                    InputFolder=self.input_Folder, \
                                    OutputFolder=self.output_Folder, \
                                    ArrayFolder=self.condition_Array, \
                                    Caller = self, \
                                    CallbackMsgFunc = MainWindow.Message_Callback)
            zettmain.StartParse()
        elif self.evaluation_Item == 1: #PDAF
            pdafmain.SetParameters( nWidth=np.int64(int(textWidth, 10)), \
                                    nHeight=np.int64(int(textHeight, 10)), \
                                    nX=np.int64(int(textX, 10)), \
                                    nY=np.int64(int(textY, 10)), \
                                    nROI_W=np.int64(int(textROIWidth, 10)), \
                                    nROI_H=np.int64(int(textROIHeight, 10)), \
                                    nColIndex=np.int64(int(textColumnIndex, 10)), \
                                    nRowGb3Index=np.int64(int(textRowIndex, 10)), \
                                    nRowB3Index=np.int64(int(textRow2Index, 10)), \
                                    nFileCounts=np.int64(int(textFileCounts, 10)), \
                                    FileTimeStamp=textFileTimestamp, \
                                    InputFolder=self.input_Folder, \
                                    OutputFolder=self.output_Folder, \
                                    ArrayFolder=self.condition_Array, \
                                    Caller = self, \
                                    CallbackMsgFunc = MainWindow.Message_Callback)
            pdafmain.StartParse()

        elif self.evaluation_Item == 2: #Pixel
            pixelmain.SetParameters( nWidth=np.int64(int(textWidth, 10)), \
                                    nHeight=np.int64(int(textHeight, 10)), \
                                    nX=np.int64(int(textX, 10)), \
                                    nY=np.int64(int(textY, 10)), \
                                    nROI_W=np.int64(int(textROIWidth, 10)), \
                                    nROI_H=np.int64(int(textROIHeight, 10)), \
                                    bIsAYABin=bAYABin, \
                                    nFileCounts=np.int64(int(textFileCounts, 10)), \
                                    FileTimeStamp=textFileTimestamp, \
                                    InputFolder=self.input_Folder, \
                                    OutputFolder=self.output_Folder, \
                                    ArrayFolder=self.condition_Array, \
                                    Caller = self, \
                                    CallbackMsgFunc = MainWindow.Message_Callback)
            pixelmain.StartParse()
        
        #print(zettmain.g_sFilePathFolder)
        print("Evaluate Finish!!!")

        return

    def buttonClick_InputFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.input_Folder = QFileDialog.getExistingDirectory(self, 'Choose Input Folder', '/home/dino/IMX586_Bin/', options=options)
        if self.input_Folder != '':
            self.input_Folder = self.input_Folder + '/{}/'
            self.ui.lineEdit_InputFolder.setText(self.input_Folder)
        return

    def buttonClick_OutputFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.output_Folder = QFileDialog.getExistingDirectory(self, 'Choose Output Folder', '/home/dino/RawShared/Output/', options=options)
        if self.output_Folder != '':
            self.output_Folder = self.output_Folder + '/{}/'
            self.ui.lineEdit_OutputFolder.setText(self.output_Folder)

        #self.CreateFolder()
        return

    def buttonClick_Condition(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        CSV_fileName, _ = QFileDialog.getOpenFileName(self, 'Choose Condition CSV', '', 'CSV File (*.csv)', options=options)
        if CSV_fileName != '':
            self.ui.lineEdit_Condition.setText(CSV_fileName)
            with open(CSV_fileName, newline='') as csvfile:
                # 讀取 CSV 檔案內容
                rows = csv.reader(csvfile)

                # 以迴圈輸出每一列
                for row in rows:
                    self.condition_Array = row
                    print(self.condition_Array)

        return

    def onComboBoxChanged(self):
        self.ShowAllUI()
        self.evaluation_Item = self.ui.comboBox_Evaluate.currentIndex() #self.ui.comboBox_Evaluate.currentText()
        if self.evaluation_Item == 0: #QE
            self.HideUIbyQE()
        elif self.evaluation_Item == 1: #PDAF
            self.HideUIbyPDAF()
        elif self.evaluation_Item == 2: #Pixel
            self.HideUIbyPixel()
        return

    # Callback
    def Message_Callback(self, strMessage):
        print(strMessage)
        strShowMsg = 'Msg: ' + strMessage
        self.ui.lineEdit_Msg.setText(strShowMsg)
        return

    # Other function
    def CreateFolder(self):
        if self.output_Folder == '' or np.size(self.condition_Array) <= 0:
            return

        for foldername in self.condition_Array:
            #folder = os.path.join(self.output_Folder, foldername)
            folder = self.output_Folder.format(foldername)
            if os.path.exists(folder):
                continue
            try:
                os.mkdir(folder)
            except OSError as error:
                print(error)
            else:
                pass
            finally:
                pass

        #folder = os.path.join(self.output_Folder, 'Output')
        folder = self.output_Folder.format('Output')
        if os.path.exists(folder):
            return
        try:
            os.mkdir(folder)
        except OSError as error:
            print(error)
        else:
            pass
        finally:
            pass

        return
