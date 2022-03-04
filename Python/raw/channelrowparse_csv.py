#######################################################
### Get one row data to calculate.
### Calculate block(R1~4/Gr1~4/Gb1~4/B1~4) std and avg.
### If R1/Gr1/Gb1/B1 only has only 1 pixel, the result is like to calculate one pixel. (nROI_W <= 4 && nROI_H <= 4)
### If R1/Gr1/Gb1/B1 only has more 1 pixel, the result is to calculate all pixels of every R1~4/Gr1~4/Gb1~4/B1~4 channel.
### If bCalMergeROIChannel is True, the result is to calculate all pixels of R(1+2+3+4)/Gr(1+2+3+4)/Gb(1+2+3+4)/B(1+2+3+4) channel.

import numpy as np
from matplotlib import pyplot as plt
import time
import csv
import datetime
#import enum
import os
import re
from enum import Enum

class ActionType(Enum):
    ShowStdHistogram    = 1
    ShowDiffHistogram   = 2
    CaluTwoDiff         = 3
    CaluStdOneFile      = 4
    CaluColumnStd       = 5
    CaluRowStd          = 6
    CaluFPN             = 7
    ActionNone          = 100

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
nWidth = 8000
nHeight = 6000

#Color TEG
#nWidth = 9728
#nHeight = 8192

g_sFilePath = '/home/dino/RawShared/Output/2022030416_DS/Output/'
g_sFileName1 = '2022030416_1_Avg.csv'
g_sFileName2 = '2022030416_500_Avg.csv'

g_sOutputFileName = '2022030416_500_1_Diff.csv'

g_ActionType = ActionType.CaluTwoDiff

nROI_W = nWidth
nROI_H = nHeight

#Debug or not
bShowDebugOutput = True

### Change the parameters to match the settings
#######################################################

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
#print(TimeInfo)

def SaveArrayToCSV(SaveArray, strFileName, fmtType, delimiterType):
    sFile = '{}{}'.format(g_sFilePath, strFileName)
    np.savetxt(sFile, SaveArray, fmt = fmtType, delimiter = delimiterType)

def LoadFileFromCSV(strFileName):
    sFile = '{}{}'.format(g_sFilePath, strFileName)
    sLoadArray = np.loadtxt(sFile, delimiter=',')
    print('Load File:{}, Array:{} Shape:{}'.format(sFile, sLoadArray, sLoadArray.shape))
    return sLoadArray

def ShowHistogram(ShowArray):
    plt.hist(ShowArray) 
    plt.title("histogram") 
    plt.show()

def ShowStdHistogram():
    LoadArray = LoadFileFromCSV(g_sFileName1)
    ShowHistogram(LoadArray)
    pass

def ShowDiffHistogram():
    LoadArray = LoadFileFromCSV(g_sFileName1)
    ShowHistogram(LoadArray)
    pass

def CaluTwoDiff():
    LoadArray1 = LoadFileFromCSV(g_sFileName1)
    LoadArray2 = LoadFileFromCSV(g_sFileName2)

    num_rows, num_cols = LoadArray1.shape
    BaseArray = np.zeros((2, num_rows, num_cols))
    BaseArray[0,:,:] = LoadArray1
    BaseArray[1,:,:] = LoadArray2

    DiffArray = np.diff(BaseArray, axis=0)
    DiffArray = np.reshape(DiffArray, (nROI_H, nROI_W))

    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(DiffArray, np.size(DiffArray), DiffArray.shape))
    #Save
    SaveArrayToCSV(DiffArray, g_sOutputFileName, '%.2f', ',')
    pass

def CaluStdOneFile(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    AllPixel_STD = np.std(LoadArray)
    if bShowDebugOutput:
        print('AllPixel_STD: {0}'.format(AllPixel_STD))
    return AllPixel_STD

def CaluColumnStd(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    num_rows, num_cols = LoadArray.shape
    ColumnArray = np.zeros((1, num_cols))
    for i in range(0, num_cols):
        ColumnPixel_Std = np.std(LoadArray[:, i])
        ColumnArray[0, i] = ColumnPixel_Std

    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(ColumnArray, np.size(ColumnArray), ColumnArray.shape))
    return ColumnArray

def CaluRowStd(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    num_rows, num_cols = LoadArray.shape
    RowArray = np.zeros((num_rows, 1))
    for i in range(0, num_rows):
        Row_Std = np.std(LoadArray[i, :])
        RowArray[i, 0] = Row_Std

    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(RowArray, np.size(RowArray), RowArray.shape))
    return RowArray

def CaluFPN(LoadArray):
    AllPixel_STD = CaluStdOneFile(LoadArray)
    ColumnArray = CaluColumnStd(LoadArray)
    column_rows, column_cols = ColumnArray.shape
    RowArray = CaluRowStd(LoadArray)
    row_rows, row_cols = RowArray.shape

    FPNArray = np.zeros((row_rows, column_cols))
    for i in range(0, row_rows):
        for j in range(0, column_cols):
            #print('AllPixel_STD:{0}, ColumnArray[0, {1}]:{2}, RowArray[{3}, 0]:{4}'.format(AllPixel_STD, j, ColumnArray[0, j], i, RowArray[i, 0]))
            #FPN = ((AllPixel_STD)**2 - (ColumnArray[0, j])**2 - (RowArray[i, 0])**2) ** 0.5
            #print('FPN: {0}'.format(FPN))

            FPN = ((AllPixel_STD)**2 - (ColumnArray[0, j])**2 - (RowArray[i, 0])**2)
            #print('FPN: {0}'.format(FPN))
            FPNArray[i,j] = FPN

    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(FPNArray, np.size(FPNArray), FPNArray.shape))
    #Save
    SaveArrayToCSV(FPNArray, g_sOutputFileName, '%.8f', ',')
    pass


if __name__ == "__main__":
    if g_ActionType == ActionType.ShowStdHistogram:
        ShowStdHistogram()
        pass
    elif g_ActionType == ActionType.ShowDiffHistogram:
        ShowDiffHistogram()
        pass
    elif g_ActionType == ActionType.CaluTwoDiff:
        CaluTwoDiff()
        pass
    elif g_ActionType == ActionType.CaluStdOneFile:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluStdOneFile(LoadArray)
        pass
    elif g_ActionType == ActionType.CaluColumnStd:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluColumnStd(LoadArray)
        pass
    elif g_ActionType == ActionType.CaluRowStd:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluRowStd(LoadArray)
        pass
    elif g_ActionType == ActionType.CaluFPN:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluFPN(LoadArray)
        pass
    elif g_ActionType == ActionType.ActionNone:
        pass

    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
