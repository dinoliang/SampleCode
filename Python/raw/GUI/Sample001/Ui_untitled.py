# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(722, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setGeometry(QtCore.QRect(590, 30, 89, 25))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 70, 241, 27))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_Width = QtWidgets.QLabel(self.layoutWidget)
        self.label_Width.setObjectName("label_Width")
        self.horizontalLayout.addWidget(self.label_Width)
        self.lineEdit_Width = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_Width.setObjectName("lineEdit_Width")
        self.horizontalLayout.addWidget(self.lineEdit_Width)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(30, 100, 241, 27))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_Height = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_Height.setObjectName("label_Height")
        self.horizontalLayout_2.addWidget(self.label_Height)
        self.lineEdit_Height = QtWidgets.QLineEdit(self.layoutWidget_2)
        self.lineEdit_Height.setObjectName("lineEdit_Height")
        self.horizontalLayout_2.addWidget(self.lineEdit_Height)
        self.layoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(30, 130, 241, 27))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_X = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_X.setObjectName("label_X")
        self.horizontalLayout_3.addWidget(self.label_X)
        self.lineEdit_X = QtWidgets.QLineEdit(self.layoutWidget_3)
        self.lineEdit_X.setObjectName("lineEdit_X")
        self.horizontalLayout_3.addWidget(self.lineEdit_X)
        self.layoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_4.setGeometry(QtCore.QRect(30, 160, 241, 27))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_Y = QtWidgets.QLabel(self.layoutWidget_4)
        self.label_Y.setObjectName("label_Y")
        self.horizontalLayout_4.addWidget(self.label_Y)
        self.lineEdit_Y = QtWidgets.QLineEdit(self.layoutWidget_4)
        self.lineEdit_Y.setObjectName("lineEdit_Y")
        self.horizontalLayout_4.addWidget(self.lineEdit_Y)
        self.layoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_5.setGeometry(QtCore.QRect(30, 220, 241, 27))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_ROIHeight = QtWidgets.QLabel(self.layoutWidget_5)
        self.label_ROIHeight.setObjectName("label_ROIHeight")
        self.horizontalLayout_5.addWidget(self.label_ROIHeight)
        self.lineEdit_ROIHeight = QtWidgets.QLineEdit(self.layoutWidget_5)
        self.lineEdit_ROIHeight.setObjectName("lineEdit_ROIHeight")
        self.horizontalLayout_5.addWidget(self.lineEdit_ROIHeight)
        self.layoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_6.setGeometry(QtCore.QRect(30, 190, 241, 27))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_ROIWidth = QtWidgets.QLabel(self.layoutWidget_6)
        self.label_ROIWidth.setObjectName("label_ROIWidth")
        self.horizontalLayout_6.addWidget(self.label_ROIWidth)
        self.lineEdit_ROIWidth = QtWidgets.QLineEdit(self.layoutWidget_6)
        self.lineEdit_ROIWidth.setObjectName("lineEdit_ROIWidth")
        self.horizontalLayout_6.addWidget(self.lineEdit_ROIWidth)
        self.layoutWidget_7 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_7.setGeometry(QtCore.QRect(30, 250, 241, 27))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.layoutWidget_7)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_ColumnIndex = QtWidgets.QLabel(self.layoutWidget_7)
        self.label_ColumnIndex.setObjectName("label_ColumnIndex")
        self.horizontalLayout_7.addWidget(self.label_ColumnIndex)
        self.lineEdit_ColumnIndex = QtWidgets.QLineEdit(self.layoutWidget_7)
        self.lineEdit_ColumnIndex.setObjectName("lineEdit_ColumnIndex")
        self.horizontalLayout_7.addWidget(self.lineEdit_ColumnIndex)
        self.layoutWidget_8 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_8.setGeometry(QtCore.QRect(30, 280, 241, 27))
        self.layoutWidget_8.setObjectName("layoutWidget_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.layoutWidget_8)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_RowIndex = QtWidgets.QLabel(self.layoutWidget_8)
        self.label_RowIndex.setObjectName("label_RowIndex")
        self.horizontalLayout_8.addWidget(self.label_RowIndex)
        self.lineEdit_RowIndex = QtWidgets.QLineEdit(self.layoutWidget_8)
        self.lineEdit_RowIndex.setObjectName("lineEdit_RowIndex")
        self.horizontalLayout_8.addWidget(self.lineEdit_RowIndex)
        self.layoutWidget_9 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_9.setGeometry(QtCore.QRect(30, 310, 241, 27))
        self.layoutWidget_9.setObjectName("layoutWidget_9")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.layoutWidget_9)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_FileCounts = QtWidgets.QLabel(self.layoutWidget_9)
        self.label_FileCounts.setObjectName("label_FileCounts")
        self.horizontalLayout_9.addWidget(self.label_FileCounts)
        self.lineEdit_FileCounts = QtWidgets.QLineEdit(self.layoutWidget_9)
        self.lineEdit_FileCounts.setObjectName("lineEdit_FileCounts")
        self.horizontalLayout_9.addWidget(self.lineEdit_FileCounts)
        self.layoutWidget_10 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_10.setGeometry(QtCore.QRect(30, 340, 241, 27))
        self.layoutWidget_10.setObjectName("layoutWidget_10")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.layoutWidget_10)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_FileTimestamp = QtWidgets.QLabel(self.layoutWidget_10)
        self.label_FileTimestamp.setObjectName("label_FileTimestamp")
        self.horizontalLayout_10.addWidget(self.label_FileTimestamp)
        self.lineEdit_FileTimestamp = QtWidgets.QLineEdit(self.layoutWidget_10)
        self.lineEdit_FileTimestamp.setObjectName("lineEdit_FileTimestamp")
        self.horizontalLayout_10.addWidget(self.lineEdit_FileTimestamp)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 370, 661, 27))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lineEdit_InputFolder = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_InputFolder.setObjectName("lineEdit_InputFolder")
        self.horizontalLayout_11.addWidget(self.lineEdit_InputFolder)
        self.pushButton_InputFolder = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_InputFolder.setObjectName("pushButton_InputFolder")
        self.horizontalLayout_11.addWidget(self.pushButton_InputFolder)
        self.layoutWidget_11 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_11.setGeometry(QtCore.QRect(30, 400, 661, 27))
        self.layoutWidget_11.setObjectName("layoutWidget_11")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.layoutWidget_11)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.lineEdit_OutputFolder = QtWidgets.QLineEdit(self.layoutWidget_11)
        self.lineEdit_OutputFolder.setObjectName("lineEdit_OutputFolder")
        self.horizontalLayout_12.addWidget(self.lineEdit_OutputFolder)
        self.pushButton_OutputFolder = QtWidgets.QPushButton(self.layoutWidget_11)
        self.pushButton_OutputFolder.setObjectName("pushButton_OutputFolder")
        self.horizontalLayout_12.addWidget(self.pushButton_OutputFolder)
        self.layoutWidget_12 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_12.setGeometry(QtCore.QRect(30, 430, 661, 27))
        self.layoutWidget_12.setObjectName("layoutWidget_12")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.layoutWidget_12)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lineEdit_Condition = QtWidgets.QLineEdit(self.layoutWidget_12)
        self.lineEdit_Condition.setObjectName("lineEdit_Condition")
        self.horizontalLayout_13.addWidget(self.lineEdit_Condition)
        self.pushButton_Condition = QtWidgets.QPushButton(self.layoutWidget_12)
        self.pushButton_Condition.setObjectName("pushButton_Condition")
        self.horizontalLayout_13.addWidget(self.pushButton_Condition)
        self.lineEdit_Msg = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Msg.setGeometry(QtCore.QRect(340, 30, 241, 25))
        self.lineEdit_Msg.setReadOnly(True)
        self.lineEdit_Msg.setObjectName("lineEdit_Msg")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 20, 241, 27))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_Evaluate = QtWidgets.QLabel(self.layoutWidget2)
        self.label_Evaluate.setObjectName("label_Evaluate")
        self.horizontalLayout_14.addWidget(self.label_Evaluate)
        self.comboBox_Evaluate = QtWidgets.QComboBox(self.layoutWidget2)
        self.comboBox_Evaluate.setObjectName("comboBox_Evaluate")
        self.horizontalLayout_14.addWidget(self.comboBox_Evaluate)
        self.layoutWidget_13 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_13.setGeometry(QtCore.QRect(290, 280, 241, 27))
        self.layoutWidget_13.setObjectName("layoutWidget_13")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.layoutWidget_13)
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_RowIndex_2 = QtWidgets.QLabel(self.layoutWidget_13)
        self.label_RowIndex_2.setObjectName("label_RowIndex_2")
        self.horizontalLayout_15.addWidget(self.label_RowIndex_2)
        self.lineEdit_RowIndex_2 = QtWidgets.QLineEdit(self.layoutWidget_13)
        self.lineEdit_RowIndex_2.setObjectName("lineEdit_RowIndex_2")
        self.horizontalLayout_15.addWidget(self.lineEdit_RowIndex_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.label_Width.setText(_translate("MainWindow", "Image Width:"))
        self.label_Height.setText(_translate("MainWindow", "Image Height:"))
        self.label_X.setText(_translate("MainWindow", "start X:"))
        self.label_Y.setText(_translate("MainWindow", "start Y:"))
        self.label_ROIHeight.setText(_translate("MainWindow", "ROI Height:"))
        self.label_ROIWidth.setText(_translate("MainWindow", "ROI Width:"))
        self.label_ColumnIndex.setText(_translate("MainWindow", "Column Index:"))
        self.label_RowIndex.setText(_translate("MainWindow", "Row Index:"))
        self.label_FileCounts.setText(_translate("MainWindow", "File Counts:"))
        self.label_FileTimestamp.setText(_translate("MainWindow", "File Timestamp:"))
        self.pushButton_InputFolder.setText(_translate("MainWindow", "Input"))
        self.pushButton_OutputFolder.setText(_translate("MainWindow", "Output"))
        self.pushButton_Condition.setText(_translate("MainWindow", "CSV"))
        self.label_Evaluate.setText(_translate("MainWindow", "Evaluate:"))
        self.label_RowIndex_2.setText(_translate("MainWindow", "Row Index:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
