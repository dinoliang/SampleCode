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

def Save2DArrayToBin(Save_Array, strFileName):
    rows, cols = Save_Array.shape
    SaveArray = np.zeros((1, rows * cols + 2))
    SaveArray[0, 0] = cols
    SaveArray[0, 1] = rows
    SArray = Save_Array[:,:].flatten()
    SaveArray[0, 2:cols * rows + 2] = SArray
    print('SaveArray:{}, Shape:{}'.format(SaveArray, SaveArray.shape))
    SaveArray.astype(np.uint16).tofile(strFileName)


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

    #DiffArray = DiffArray/float(8405.0)
    #if bShowDebugOutput:
    #    print('Array: {0}, Len:{1}, shape:{2}'.format(DiffArray, np.size(DiffArray), DiffArray.shape))
    
    #Save
    SaveArrayToCSV(DiffArray, g_sOutputFileName, '%.6f', ',')
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
        ColumnPixel_Avg = np.average(LoadArray[:, i])
        ColumnArray[0, i] = ColumnPixel_Avg
    AllColumnPixel_Std = np.std(ColumnArray)
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}, STD:{3}'.format(ColumnArray, np.size(ColumnArray), ColumnArray.shape, AllColumnPixel_Std))
    return AllColumnPixel_Std

def CaluRowStd(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    num_rows, num_cols = LoadArray.shape
    RowArray = np.zeros((num_rows, 1))
    for i in range(0, num_rows):
        RowPixel_Std = np.average(LoadArray[i, :])
        RowArray[i, 0] = RowPixel_Std
    AllRowPixel_Std = np.std(RowArray)
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}, STD:{3}'.format(RowArray, np.size(RowArray), RowArray.shape, AllRowPixel_Std))
    return AllRowPixel_Std

def CaluFPN(LoadArray):
    AllPixel_STD = CaluStdOneFile(LoadArray)
    ColumnStd = CaluColumnStd(LoadArray)
    RowStd = CaluRowStd(LoadArray)
    FPN = ((AllPixel_STD)**2 - (ColumnStd)**2 - (RowStd**2))
    if bShowDebugOutput:
        print('AllPixelStd: {0}, ColumnStd: {1}, RowStd: {2}, FPN: {3}'.format(AllPixel_STD, ColumnStd, RowStd, FPN))

    FPN = (FPN)**0.5
    if bShowDebugOutput:
        print('FPN^0.5: {0}'.format(FPN))

    return FPN


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
