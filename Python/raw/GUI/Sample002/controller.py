from ui_untitled import Ui_MainWindow
import sys
import csv
import os

sys.path.append('/home/dino/PythonShared/raw/')
import cp_wafermap as cpwafer


class MainWindow(QtWidgets.QMainWindow):
    cp_Folder = ''

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.ui.pushButton_Start.clicked.connect(self.buttonClick_Start)
        self.ui.pushButton_CPFolder.clicked.connect(self.buttonClick_CPFolder)

        return

    # UI Display
    def ShowAllUI(self):
        return

    # Botton Action
    def buttonClick_Start(self):
        strResultFolder = self.cp_Folder
        strResultOutFile = self.ui.lineEdit_OutputName.text()
        if strResultFolder == '':
            return

        result = cpwafer.ResultHandler()
        result.SetCallback(self, MainWindow.Message_Callback)
        result.StartCombine(strResultFolder, strResultOutFile)
        return

    def buttonClick_CPFolder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.cp_Folder = QFileDialog.getExistingDirectory(self, 'Choose CP Result Folder', '/home/dino/PythonShared/raw/STDFResult/Test001/', options=options)
        if self.cp_Folder != '':
            self.ui.lineEdit_CPFolder.setText(self.cp_Folder)
        return

    # Callback
    def Message_Callback(self, strMessage):
        strShowMsg = 'Msg: ' + strMessage
        print(strShowMsg)
        return
