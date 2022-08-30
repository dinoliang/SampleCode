#######################################################
### Get all pixel information by multi-images
### Calculate the value by different block (g_nCalRows)
### Merge all block to one calculated image
### Get ROI by (g_nRowIndex、g_nRowBound、g_nColumnIndex、g_nColumnBound)
### Save ROI result to csv or bin file

import numpy as np
from matplotlib import pyplot as plt
import time
import csv
import datetime
#import enum
import os
import re

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
#nWidth = 8000
#nHeight = 6000

#g_nRowIndex = 240
#g_nRowBound  = 9540
#g_nColumnIndex = 0
#g_nColumnBound = 7000

'''
#ES1
nWidth = 9248
nHeight = 6944

g_nRowIndex = 10
g_nRowBound  = 170
g_nColumnIndex = 20
g_nColumnBound = 6920
'''

#Color TEG
nWidth = 9728
nHeight = 8192

g_nRowIndex = 300
g_nRowBound  = 6470
g_nColumnIndex = 100
g_nColumnBound = 6950


nFileCount = 25
#sFilePath = '/home/dino/RawShared/2022031816_P8N533_1813_DC/{}/'
#sFilePath = '/home/dino/RawShared/Temp/Temp6/{}/'
#sFilePath = '/home/dino/IMX586_Raw2/2022082514_HTOL_T168_0117/DC/{}/'
sFilePath = '/home/dino/IMX586_Bin/TEG_HTOL_T0/N0117/2022050615_HTOL_T0_DC_N0117_OK/{}/'
#sFilePath = '/home/dino/RawShared/2022082216_ES1_HOPB_60DC/Left/{}/'

#There is header data, and the extenstion file name is *.bin in AYA file
g_bAYAFile = True

#Subfolder
#Normal
g_sFilePathFolder = [
                    #'50_1', '50_500', '55_1', '55_500', '60_1', '60_500', '65_1', '65_500', '70_1', '70_500', \
                    #'1X', '2X', '4X', '8X', '16X', \
                    #'0008', '0100', '0200', '0300', '0400', '0500', '0600', '0700', '07FD', \
                    #'Room_0x0008_24db', 'Room_0x07FD_24db', '60DC_0x0008_24db', '60DC_0x07FD_24db', \
                    'Room_0x0008_24db', \
                    ]

#nROI_W = nWidth
#nROI_H = nHeight
nROI_W = g_nRowBound - g_nRowIndex
nROI_H = g_nColumnBound - g_nColumnIndex

g_nCalRows = 1000

#Saving output file or not
g_bSaveFile = True

#The path of saving file
sFileTempTime = '2022082514'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021111810/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021112914/4000_3000/600/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/Temp/{}/'
sSavePath = '/home/dino/RawShared/Output/2022082514_HTOL_T168_0117_testpy2/DC/{}/'

#Debug or not
bShowDebugOutput = True

#Delete the over Max/Min number or not
bDeleteMaxMin = False
nDeleteMaxCount = 3
nDeleteMinCount = 3

#(Test TEG)
#TEG Bad Pixel
g_bDeleteBadPixel = False
g_nBadPixelLevel = 64


### Change the parameters to match the settings
#######################################################
# Set Callback Information
gCaller = None
gCallbackMessageFunc = None

g_nRawBeginIndex = 0

if not g_bAYAFile:
    g_nRawBeginIndex = 0
else:
    g_nRawBeginIndex = 4    # header (width + height)

#reference by np.zeros
g_nArrayDefaultValue = 0

#PixelRow_array = np.zeros((nFileCount, nROI_W))
StdArray = []
AvgArray = []

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
TimeInfo = sFileTempTime
#print(TimeInfo)

def Cal_Pixel_Avg(ChannelArray, x, y):
    PixelArray = ChannelArray[:,x,y].flatten()
    PixelArray = np.delete(PixelArray, np.where(PixelArray == g_nArrayDefaultValue))
    #if bShowDebugOutput:
    #    print(PixelArray)
    Pixel_AVG = np.average(PixelArray)
    return Pixel_AVG

def Cal_Pixel_Std(ChannelArray, x, y):
    PixelArray = ChannelArray[:,x,y].flatten()
    PixelArray = np.delete(PixelArray, np.where(PixelArray == g_nArrayDefaultValue))
    #if bShowDebugOutput:
    #    print(PixelArray)
    Pixel_STD = np.std(PixelArray)
    return Pixel_STD

def SaveAvgToCSV(Avg_Array, folder):
    #sAvgFile = sSavePath.format(folder) + sFileTempTime + '_Avg.csv'
    sAvgFile = '{}{}_{}_Avg.csv'.format(sSavePath.format(folder), sFileTempTime, folder)
    np.savetxt(sAvgFile, Avg_Array[0:nROI_H, 0:nROI_W], fmt = '%.2f', delimiter=',')

    sAvgInfoFile = '{}{}_{}_AvgInfo.txt'.format(sSavePath.format(folder), sFileTempTime, folder)
    if os.path.exists(sAvgInfoFile):
        os.remove(sAvgInfoFile)
    with open(sAvgInfoFile, "a") as f:
        f.write('========== Average Array Shape:{} ==========\n'.format(Avg_Array[0:nROI_H, 0:nROI_W].shape))
        f.write('================== The average of AVG ==================\n')
        f.write('The average of AVG: {}\n'.format(np.average(Avg_Array[0:nROI_H, 0:nROI_W])))
        f.write('================== The std of AVG ==================\n')
        f.write('The std of AVG: {}\n'.format(np.std(Avg_Array[0:nROI_H, 0:nROI_W])))

def SaveStdToCSV(Std_Array, folder):
    #sStdFile = sSavePath.format(folder) +  sFileTempTime + '_Std.csv'
    sStdFile = '{}{}_{}_Std.csv'.format(sSavePath.format(folder), sFileTempTime, folder)
    np.savetxt(sStdFile, Std_Array[0:nROI_H, 0:nROI_W], fmt = '%.8f', delimiter=',')

    sStdInfoFile = '{}{}_{}_StdInfo.txt'.format(sSavePath.format(folder), sFileTempTime, folder)
    if os.path.exists(sStdInfoFile):
        os.remove(sStdInfoFile)
    with open(sStdInfoFile, "a") as f:
        f.write('========== Average Array Shape:{} ==========\n'.format(Std_Array[0:nROI_H, 0:nROI_W].shape))
        f.write('================== The average of STD ==================\n')
        f.write('The average of STD: {}\n'.format(np.average(Std_Array[0:nROI_H, 0:nROI_W])))
        f.write('================== The std of AVG ==================\n')
        f.write('The median of STD: {}\n'.format(np.median(Std_Array[0:nROI_H, 0:nROI_W])))

def LoadAvgFromCSV(folder):
    #sAvgFile = sSavePath.format(folder) + sFileTempTime + '_Avg.csv'
    sAvgFile = '{}{}_{}_Avg.csv'.format(sSavePath.format(folder), sFileTempTime, folder)
    sLoadAvgArray = np.loadtxt(sAvgFile, delimiter=',')
    print('Load AVG:{}, Shape:{}'.format(sLoadAvgArray, sLoadAvgArray.shape))
    return sLoadAvgArray
        
def LoadStdFromCSV(folder):
    #sStdFile = sSavePath.format(folder) +  sFileTempTime + '_Std.csv'
    sStdFile = '{}{}_{}_Std.csv'.format(sSavePath.format(folder), sFileTempTime, folder)
    sLoadStdArray = np.loadtxt(sStdFile, delimiter=',')
    print('Load STD:{}, Shape:{}'.format(sLoadStdArray, sLoadStdArray.shape))
    return sLoadStdArray

def ShowHistogram(ShowArray):
    plt.hist(ShowArray) 
    plt.title("histogram") 
    plt.show()

def SaveAvgToBin(Avg_Array, folder):
    #sAvgFile = sSavePath.format(folder) + sFileTempTime + '_Avg.csv'
    sAvgFile = '{}{}_{}_Avg.bin'.format(sSavePath.format(folder), sFileTempTime, folder)
    print('SaveArray to Bin file ({})'.format(sAvgFile))
    nTotalFileSize = ((nROI_H) * (nROI_W) + 2)
    SaveArray = np.zeros((1, nTotalFileSize))
    SaveArray[0, 0] = nROI_W
    SaveArray[0, 1] = nROI_H
    AvgArray = Avg_Array[0:nROI_H, 0:nROI_W].flatten()
    SaveArray[0, 2:nTotalFileSize] = AvgArray
    #print('SaveArray:{}, Shape:{}'.format(SaveArray, SaveArray.shape))
    print('SaveArray Shape:{}'.format(SaveArray.shape))
    SaveArray.astype(np.uint16).tofile(sAvgFile)


def ParsingPixel():
    nCount = nFileCount
    nRawBeginIndex = g_nRawBeginIndex

    #Check file
    #if os.path.exists(sSaveOrgRFile):
    #    os.remove(sSaveOrgRFile)

    for x in g_sFilePathFolder:
        sTempFilePath = sFilePath.format(x)
        
        AvgArray = np.zeros((nROI_H, nROI_W))
        StdArray = np.zeros((nROI_H, nROI_W))

        #Every row
        for i in range(g_nColumnIndex, g_nColumnIndex+nROI_H, g_nCalRows):

            nCalRows = g_nCalRows
            if nROI_H - i < g_nCalRows:
                nCalRows = g_nColumnIndex + nROI_H - i
            if bShowDebugOutput:
                print('Pixel_array Size[{},{},{}]'.format(nCount, nCalRows, nROI_W))
            Pixel_array = None
            Pixel_array = np.zeros((nCount, nCalRows, nROI_W))

            k = 0
            for root, dirs, files in os.walk(sTempFilePath):
                for sFile in files:
                    if k >= nCount:
                        continue

                    sFileTemp = sFile
                    sFileTemp = root + '/' + sFileTemp
                    if bShowDebugOutput:
                        print('sFileTemp: ', sFileTemp)

                    OneCalArray = np.zeros((nCalRows, nROI_W))

                    nPixelOffset = nWidth * i * 2 + nRawBeginIndex
                    input_file = open(sFileTemp, 'rb')
                    input_array = np.fromfile(input_file, dtype=np.uint16, count=nWidth*nCalRows, sep="", offset=nPixelOffset)
                    input_file.close()
                    #print('input_array:{}, {}'.format(np.size(input_array), input_array.shape))

                    for ColIdx in range(0, nCalRows):
                        input_array_Idx = nWidth * ColIdx + g_nRowIndex
                        OneCalArray[ColIdx,:] = input_array[input_array_Idx:input_array_Idx+nROI_W]

                    ## Dino test
                    #print('OneCalArray[0, 0]: {0}'.format(OneCalArray[0, 0]))

                    #input_file = open(sFileTemp, 'rb')
                    ##Get all pixel of one range row
                    #input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W * nCalRows, sep="", offset=nPixelOffset)
                    #input_file.close()
                    ##print('input_array: {0}, Len:{1}'.format(input_array, np.size(input_array)))

                    #for m in range(0, nCalRows):
                    #    for n in range(0, nROI_W):
                    #        if g_bDeleteBadPixel and input_array[m*nCalRows + n] < g_nBadPixelLevel:
                    #        #    print('Bad Pixel {0}, {1}'.format(m*nCalRows + n, input_array[m*nCalRows + n]))
                    #            continue
                    #
                    #        #if bShowDebugOutput:
                    #        #    print('Pixel_array[{},{},{}]: Value:{}'.format(k,m,n,input_array[m*nCalRows + n]))
                    #        Pixel_array[k,m,n] = input_array[m*nCalRows + n]

                    #Pixel_array[k,:,:] = np.reshape(input_array, (nCalRows, nROI_W))
                    ##print('Pixel_array: {0}, Len:{1}, shape:{2}'.format(Pixel_array[k,:,:], np.size(Pixel_array[k,:,:]), Pixel_array[k,:,:].shape))
                    Pixel_array[k,:,:] = OneCalArray
                    #print('Pixel_array: {0}, Len:{1}, shape:{2}'.format(Pixel_array[k,:,:], np.size(Pixel_array[k,:,:]), Pixel_array[k,:,:].shape))

                    k = k + 1

                ## Dino test
                #return

            if bShowDebugOutput:
                print('Pixel_array[{}:{}]: Length:{}'.format(i, i+nCalRows-1, np.size(Pixel_array)))

            #for m in range(0, nCalRows):
            #    for n in range(0, nROI_W):
            #        Pixel_AVG = Cal_Pixel_Avg(Pixel_array, m, n)
            #        AvgArray[i+m, n] = Pixel_AVG
            #        Pixel_STD = Cal_Pixel_Std(Pixel_array, m, n)
            #        StdArray[i+m, n] = Pixel_STD
            #        #if bShowDebugOutput:
            #        #    print('Site[{},{}]: AVG:{}, STD:{}'.format(i+m,l,Pixel_AVG,Pixel_STD))
            AvgTempArray = np.average(Pixel_array, axis=0)
            AvgArray[i-g_nColumnIndex:i-g_nColumnIndex+nCalRows,0:nROI_W] = AvgTempArray
            StdTempArray = np.std(Pixel_array, axis=0)
            StdArray[i-g_nColumnIndex:i-g_nColumnIndex+nCalRows,0:nROI_W] = StdTempArray
            #print('AVG:{}, STD:{}'.format(np.size(AvgArray), np.size(StdArray)))
            print('NonZero AVG:{}, STD:{}'.format(np.count_nonzero(AvgArray), np.count_nonzero(StdArray)))
            #print('Temp AVG:{}, Count:{}'.format(np.size(AvgTempArray), AvgTempArray.shape))
            #print('Temp STD:{}, Count:{}'.format(np.size(StdTempArray), StdTempArray.shape))
            #print('AVG:{}'.format(AvgArray[i:i+nCalRows,0:nROI_W]))
            #print('STD:{}'.format(StdArray[i:i+nCalRows,0:nROI_W]))

            nEachRoIIntervalTime = time.time()
            print("Durning ROI Interval[{}] Time(sec): {}".format(i, nEachRoIIntervalTime - StartTime))

        #Normalize Array
        #Keep float number to txt file, do not normalize array

        #Save image
        #sAvgFile = sSavePath.format('Total') + sFileTempTime + '_Avg.csv'
        #np.savetxt(sAvgFile, AvgArray, fmt = '%.2f', delimiter=',')
        #sStdFile = sSavePath.format('Total') +  sFileTempTime + '_Std.csv'
        #np.savetxt(sStdFile, StdArray, fmt = '%.8f', delimiter=',')
        if g_bSaveFile:
            SaveAvgToCSV(AvgArray, x)
        print('========== Average Array Shape:{} =========='.format(AvgArray[0:nROI_H, 0:nROI_W].shape))
        print("================== The average of AVG ==================")
        print("The average of AVG: {}".format(np.average(AvgArray[0:nROI_H, 0:nROI_W])))
        print("================== The std of AVG ==================")
        print("The std of AVG: {}".format(np.std(AvgArray[0:nROI_H, 0:nROI_W])))

        if g_bSaveFile and nCount > 1:
            SaveAvgToBin(AvgArray, x)

        if g_bSaveFile:
            SaveStdToCSV(StdArray, x)
        print('========== Average Array Shape:{} =========='.format(StdArray[0:nROI_H, 0:nROI_W].shape))
        print("================== The average of STD ==================")
        print("The average of STD: {}".format(np.average(StdArray[0:nROI_H, 0:nROI_W])))
        print("================== The median of STD ==================")
        print("The median of STD: {}".format(np.median(StdArray[0:nROI_H, 0:nROI_W])))

        nEachIntervalTime = time.time()
        print("Durning Interval[{}] Time(sec): {}".format(x, nEachIntervalTime - StartTime))


def SetParameters(nWidth, nHeight, nX, nY, nROI_W, nROI_H, bIsAYABin, nFileCounts, FileTimeStamp, InputFolder, OutputFolder, ArrayFolder, Caller, CallbackMsgFunc):
    listVarOfGlobals = globals()
    listVarOfGlobals['nWidth']                      = nWidth
    listVarOfGlobals['nHeight']                     = nHeight
    #nROI_W = nWidth
    #nROI_H = nHeight
    listVarOfGlobals['nROI_W']                      = nROI_W
    listVarOfGlobals['nROI_H']                      = nROI_H

    listVarOfGlobals['g_nRowIndex']                 = nX
    listVarOfGlobals['g_nColumnIndex']              = nY
    listVarOfGlobals['g_nRowBound']                 = nX + nROI_W
    listVarOfGlobals['g_nColumnBound']              = nY + nROI_H

    listVarOfGlobals['g_bAYAFile']                  = bIsAYABin
    if not listVarOfGlobals['g_bAYAFile']:
        listVarOfGlobals['g_nRawBeginIndex'] = 0
    else:
        listVarOfGlobals['g_nRawBeginIndex'] = 4    # header (width + height)

    listVarOfGlobals['nFileCount']                  = nFileCounts
    listVarOfGlobals['sFilePath']                   = InputFolder
    listVarOfGlobals['sFileTempTime']               = FileTimeStamp
    listVarOfGlobals['TimeInfo']                    = FileTimeStamp

    listVarOfGlobals['sSavePath']                   = OutputFolder

    #print(listVarOfGlobals['g_sFilePathFolder'])
    listVarOfGlobals['g_sFilePathFolder']           = ArrayFolder
    #print(listVarOfGlobals['g_sFilePathFolder'])

    listVarOfGlobals['gCaller']                     = Caller
    listVarOfGlobals['gCallbackMessageFunc']        = CallbackMsgFunc
    gCallbackMessageFunc(gCaller, 'Pixel Test Message')
    pass

def StartParse():
    ParsingPixel()
    pass

if __name__ == "__main__":
    ParsingPixel()

    ##Test
    #for x in g_sFilePathFolder:
    #    LoadAvgFromCSV(x)
    #    LoadStdFromCSV(x)
    #    LoadArray = LoadStdFromCSV(x)
    #    ShowHistogram(LoadArray)

    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
