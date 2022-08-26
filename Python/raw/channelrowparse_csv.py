#######################################################
### Calculate the information by pixel csv file (not origin bin file (raw image))

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
    CaluTwoDiff         = 3         # *Avg.csv - *Avg.csv = *Avg_Diff.csv
    CaluStdOneFile      = 4
    CaluColumnStd       = 5
    CaluRowStd          = 6
    CaluFPN             = 7         # One *Avg.csv
    ChangeDiffBase      = 8
    CaluRN              = 9         # One *Std.csv
    CaluFPN_RowHis      = 10        # One *Avg.csv
    ActionNone          = 100

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
#nWidth = 8000
#nHeight = 6000
#g_nRowIndex = 0
#g_nRowBound  = 8000
#g_nColumnIndex = 0
#g_nColumnBound = 6000

#Color TEG
nWidth = 150
nHeight = 6880
g_nRowIndex = 0
g_nRowBound  = 150
g_nColumnIndex = 0
g_nColumnBound = 6880

g_sFilePath = '/home/dino/RawShared/Output/2022082216_ES1_HOPB_60DC/Left/'
g_sFileName1 = 'LongExposure/2022082216_LongExposure_Avg.csv'
g_sFileName2 = 'LongExposure/2022082216_LongExposure_Avg.csv'

g_sOutputFileName = '2022082216_HOPB_RIGHT_60DC_Avg_Diff.csv'
g_sOutputBinName = '2022082216_HOPB_RIGHT_60DC_Avg_Diff.bin'

g_sOutputFPNRowHisName = 'LongExposure/2022082216_HOPB_LEFT_Room_0x0008_24db_FPN_RowHis.csv'

g_ActionType = ActionType.CaluFPN_RowHis

#nROI_W = nWidth
#nROI_H = nHeight
nROI_W = g_nRowBound - g_nRowIndex
nROI_H = g_nColumnBound - g_nColumnIndex

g_fTwoDiffBenchmark = 1.0 #Sec

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
    BaseArray = np.zeros((2, g_nColumnBound-g_nColumnIndex, g_nRowBound-g_nRowIndex))
    BaseArray[0,:,:] = LoadArray1[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound]
    BaseArray[1,:,:] = LoadArray2[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound]

    DiffArray = np.diff(BaseArray, axis=0)
    DiffArray = np.reshape(DiffArray, (nROI_H, nROI_W))
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(DiffArray, np.size(DiffArray), DiffArray.shape))

    if g_fTwoDiffBenchmark != 1.0:
        DiffArray = DiffArray/float(g_fTwoDiffBenchmark)
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}'.format(DiffArray, np.size(DiffArray), DiffArray.shape))

    print("The average of Diff: {}".format(np.average(DiffArray)))
    
    #Save
    SaveArrayToCSV(DiffArray, g_sOutputFileName, '%.6f', ',')
    
    sFile = '{}{}'.format(g_sFilePath, g_sOutputBinName)
    Save2DArrayToBin(DiffArray, sFile)
    pass

def CaluStdOneFile(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    AllPixel_STD = np.std(LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound])
    if bShowDebugOutput:
        print('AllPixel_STD: {0}'.format(AllPixel_STD))
    return AllPixel_STD

def CaluColumnStd(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    num_rows, num_cols = LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound].shape
    ColumnArray = np.zeros((1, num_cols))
    for i in range(0, num_cols):
        ColumnPixel_Avg = np.average(LoadArray[g_nColumnIndex:g_nColumnBound, i])
        ColumnArray[0, i] = ColumnPixel_Avg
    AllColumnPixel_Std = np.std(ColumnArray)
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}, STD:{3}'.format(ColumnArray, np.size(ColumnArray), ColumnArray.shape, AllColumnPixel_Std))

    AllColumnPixel_Avg = np.average(ColumnArray)
    if bShowDebugOutput:
        print('AllColumnPixel (Avg): {0}'.format(AllColumnPixel_Avg))

    square = np.square(ColumnArray)
    MSE = square.mean()
    RMSE = np.sqrt(MSE)
    if bShowDebugOutput:
        print('AllColumnPixel (RMS): {0}'.format(RMSE))
    return AllColumnPixel_Std

def CaluRowStd(LoadArray):
    #LoadArray = LoadFileFromCSV(g_sFileName1)
    num_rows, num_cols = LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound].shape
    RowArray = np.zeros((num_rows, 1))
    for i in range(0, num_rows):
        RowPixel_Std = np.average(LoadArray[i, g_nRowIndex:g_nRowBound])
        RowArray[i, 0] = RowPixel_Std
    AllRowPixel_Std = np.std(RowArray)
    if bShowDebugOutput:
        print('Array: {0}, Len:{1}, shape:{2}, STD:{3}'.format(RowArray, np.size(RowArray), RowArray.shape, AllRowPixel_Std))

    AllRowPixel_Avg = np.average(RowArray)
    if bShowDebugOutput:
        print('AllRowPixel (Avg): {0}'.format(AllRowPixel_Avg))

    square = np.square(RowArray)
    MSE = square.mean()
    RMSE = np.sqrt(MSE)
    if bShowDebugOutput:
        print('AllRowPixel (RMS): {0}'.format(RMSE))
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

    if bShowDebugOutput:
        print('AllPixel (STD): {0}'.format(AllPixel_STD))

    AllPixel_square = np.square(LoadArray)
    AllPixel_MSE = AllPixel_square.mean()
    AllPixel_RMSE = np.sqrt(AllPixel_MSE)
    if bShowDebugOutput:
        print('AllPixel (RMS): {0}'.format(AllPixel_RMSE))

    return FPN

def ChangeDiffBase(LoadArray):
    #np.around(LoadArray, 6)
    if g_fTwoDiffBenchmark != 1.0:
        LoadArray = LoadArray/float(g_fTwoDiffBenchmark)
    #np.around(LoadArray, 6)
    print('Diff Array:{} Shape:{}'.format(LoadArray, LoadArray.shape))
    SaveArrayToCSV(LoadArray, g_sOutputFileName, '%.6f', ',')
    return

def CaluRN(LoadArray):
    AVG = np.average(LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound])
    if bShowDebugOutput:
        print('RN (Average): {0}'.format(AVG))

    RN = np.median(LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound])
    if bShowDebugOutput:
        print('RN (Median): {0}'.format(RN))

    STD = np.std(LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound])
    if bShowDebugOutput:
        print('RN (STD): {0}'.format(STD))

    square = np.square(LoadArray[g_nColumnIndex:g_nColumnBound, g_nRowIndex:g_nRowBound])
    MSE = square.mean()
    RMSE = np.sqrt(MSE)
    if bShowDebugOutput:
        print('RN (RMS): {0}'.format(RMSE))

    return RN

def CaluFPN_RowHis(LoadArray):
    SaveArray = np.zeros((nROI_H, 1))
    for RowIdx in range(0, nROI_H):
        SaveArray[RowIdx, 0] = np.average(LoadArray[RowIdx, g_nRowIndex:g_nRowBound])
        #print('SaveArray Array[{},0] ={}'.format(RowIdx, SaveArray[RowIdx, 0]))
    #print('FPN_RowHis Array:{} Shape:{}'.format(SaveArray, SaveArray.shape))
    SaveArrayToCSV(SaveArray, g_sOutputFPNRowHisName, '%.6f', ',')
    return


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
    elif g_ActionType == ActionType.ChangeDiffBase:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        ChangeDiffBase(LoadArray)
        pass
    elif g_ActionType == ActionType.CaluRN:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluRN(LoadArray)
    elif g_ActionType == ActionType.CaluFPN_RowHis:
        LoadArray = LoadFileFromCSV(g_sFileName1)
        CaluFPN_RowHis(LoadArray)
    elif g_ActionType == ActionType.ActionNone:
        pass

    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
