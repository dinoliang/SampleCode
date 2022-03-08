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

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
nWidth = 8000
nHeight = 6000

#Color TEG
#nWidth = 9728
#nHeight = 8192

nFileCount = 25
#sFilePath = '/home/dino/RawShared/2022020816/{}/'
#sFilePath = '/home/dino/RawShared/Temp/Temp6/{}/'
#sFilePath = '/home/dino/IMX586_Raw2/2022012517/{}/'
sFilePath = '/home/dino/IMX586_Bin/2022030416_DS/{}/'

#There is header data, and the extenstion file name is *.bin in AYA file
g_bAYAFile = True

#Subfolder
#Normal
g_sFilePathFolder = [
                    '1', '500', \
                    ]

nROI_W = nWidth
nROI_H = nHeight

#Saving output file or not
bSaveCSV = True

#The path of saving file
sFileTempTime = '2022030416'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021111810/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021112914/4000_3000/600/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/Temp/{}/'
sSavePath = '/home/dino/RawShared/Output/2022030416_DS/Output/{}/'

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
g_nRawBeginIndex = 0

if not g_bAYAFile:
    g_nRawBeginIndex = 0
else:
    g_nRawBeginIndex = 4    # header (width + height)

#reference by np.zeros
g_nArrayDefaultValue = 0

#PixelRow_array = np.zeros((nFileCount, nROI_W))
BaseArray = []
DiffArray = []

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
TimeInfo = sFileTempTime
#print(TimeInfo)

def SaveDiffToCSV(Diff_Array, folder, no):
    #sDiffFile = '{}{}_Diff_{}.csv'.format(sSavePath.format('Total'), sFileTempTime, no)
    sDiffFile = '{}{}_{}_Diff_{}.csv'.format(sSavePath.format(folder), sFileTempTime, folder, no)
    np.savetxt(sDiffFile, Diff_Array, fmt = '%d', delimiter=',')

def LoadDiffFromCSV(folder, no):
    #sDiffFile = '{}{}_Diff_{}.csv'.format(sSavePath.format('Total'), sFileTempTime, no)
    sDiffFile = '{}{}_{}_Diff_{}.csv'.format(sSavePath.format(folder), sFileTempTime, folder, no)
    sLoadDiffArray = np.loadtxt(sDiffFile, delimiter=',')
    print('Load AVG:{}, Shape:{}'.format(sLoadDiffArray, sLoadDiffArray.shape))
    return sLoadDiffArray

def ShowHistogram(ShowArray):
    plt.hist(ShowArray) 
    plt.title("histogram") 
    plt.show()


def ParsingPixel():
    nCount = nFileCount
    nRawBeginIndex = g_nRawBeginIndex

    #Check file
    #if os.path.exists(sSaveOrgRFile):
    #    os.remove(sSaveOrgRFile)

    for x in g_sFilePathFolder:
        sTempFilePath = sFilePath.format(x)

        BaseArray = np.zeros((2, nROI_H, nROI_W))
        DiffArray = np.zeros((nROI_H, nROI_W))

        nPixelOffset = nRawBeginIndex
        if bShowDebugOutput:
            print('nPixelOffset: ', nPixelOffset)

        k = 0
        for root, dirs, files in os.walk(sTempFilePath):
            for sFile in files:
                if k >= nCount:
                    continue

                sFileTemp = sFile
                sFileTemp = root + '/' + sFileTemp
                if bShowDebugOutput:
                    print('sFileTemp: ', sFileTemp)

                input_file = open(sFileTemp, 'rb')
                #Get all pixel of one range row
                input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W * nROI_H, sep="", offset=nPixelOffset)
                input_file.close()
                #print('input_array: {0}, Len:{1}'.format(input_array, np.size(input_array)))

                if k == 0:
                    BaseArray[0,:,:] = np.reshape(input_array, (nROI_H, nROI_W))
                else:
                    BaseArray[1,:,:] = np.reshape(input_array, (nROI_H, nROI_W))

                if k > 0:
                    DiffArray = np.diff(BaseArray, axis=0)
                    DiffArray = np.reshape(DiffArray, (nROI_H, nROI_W))
                    print('DiffArray: {0}, Len:{1}, shape:{2}'.format(DiffArray, np.size(DiffArray), DiffArray.shape))
                    ##Save image
                    SaveDiffToCSV(DiffArray, x, k)
                    nEachDiffTime = time.time()
                    print("Durning Diff[{}] Time(sec): {}".format(x, nEachDiffTime - StartTime))
                
                k = k + 1

        nEachIntervalTime = time.time()
        print("Durning Interval[{}] Time(sec): {}".format(x, nEachIntervalTime - StartTime))

if __name__ == "__main__":
    ParsingPixel()

    ##Test
    #for x in g_sFilePathFolder:
    #    for i in range(0, nFileCount):
    #        LoadArray = LoadDiffFromCSV(x, i)
    #        ShowHistogram(LoadArray)
    
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
