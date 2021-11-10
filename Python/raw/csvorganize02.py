#######################################################
### One pixel std and avg.
### Save one pixel to one total csv

import numpy as np
import time
import csv
import enum
import os

StartTime = time.time()

class PixelSelect(enum.IntEnum):
    AllPixel = 0
    OnlyRPixel = 1
    OnlyGrPixel = 2
    OnlyGbPixel = 3
    OnlyBPixel = 4


#######################################################
### Change the parameters to match the settings
nX = 0
nY = 0
nWidth = 4
nHeight = 4

sFilePath = '/home/dino/RawShared/Output/'
sFileTempTime = '20211109110205'

nFileExposureIM = 1
nFileExposureID = 30
nFileExposureInterval = 1
nFileExposureIntervalNum = 9

sSavePath = '/home/dino/RawShared/Output/'

nPixelSelect = PixelSelect.OnlyGrPixel
### Change the parameters to match the settings
#######################################################


# Exposure
sStdFileTempName = 'STD_{0:s}_{1:d}_{2:d}_{3:s}.csv'
sAvgFileTempName = 'AVG_{0:s}_{1:d}_{2:d}_{3:s}.csv'
sSaveStdTempFile = 'PixelStd_{0:s}_{1:d}_{2:d}.csv'
sSaveAvgTempFile = 'PixelAvg_{0:s}_{1:d}_{2:d}.csv'
sSaveTotalTempFile = 'Pixel_{0:s}_{1:s}.csv'

lCsvStdRow = []
lCsvAvgRow = []

def Save_CSV(FileName, RowInfo):
    with open(FileName, 'a+') as f:
        # create the csv writer
        csv_writer = csv.writer(f)
        # write a row to the csv file
        #print(RowInfo)
        csv_writer.writerow(RowInfo)

def OrganizePixel():
    if (nPixelSelect == PixelSelect.OnlyRPixel):
        sSaveTotalFile = sSavePath+sSaveTotalTempFile.format(sFileTempTime, 'R')
    elif (nPixelSelect == PixelSelect.OnlyGrPixel):
        sSaveTotalFile = sSavePath+sSaveTotalTempFile.format(sFileTempTime, 'Gr')
    elif (nPixelSelect == PixelSelect.OnlyGbPixel):
        sSaveTotalFile = sSavePath+sSaveTotalTempFile.format(sFileTempTime, 'Gb')
    elif (nPixelSelect == PixelSelect.OnlyBPixel):
        sSaveTotalFile = sSavePath+sSaveTotalTempFile.format(sFileTempTime, 'B')
    if os.path.exists(sSaveTotalFile):
        os.remove(sSaveTotalFile)
    
    for g in range(nY, nY+nHeight):
        for h in range(nX, nX+nWidth):
            #print(sSaveStdFile)
            #print(sSaveAvgFile)
            lCsvAvgRow.clear()
            lCsvStdRow.clear()
            lCsvAvgRow.append('{0:d}_{1:d}_Avg'.format(h, g))
            lCsvStdRow.append('{0:d}_{1:d}_Std'.format(h, g))
            for i in range(0, nFileExposureIntervalNum):
                nFileIndex = nFileExposureIM + i*nFileExposureInterval
                if nPixelSelect == PixelSelect.AllPixel:
                    sStdFileName = sFilePath + sStdFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'All')
                    sAvgFileName = sFilePath + sAvgFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'All')
                elif (nPixelSelect == PixelSelect.OnlyRPixel):
                    sStdFileName = sFilePath + sStdFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'R')
                    sAvgFileName = sFilePath + sAvgFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'R')
                elif (nPixelSelect == PixelSelect.OnlyGrPixel):
                    sStdFileName = sFilePath + sStdFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'Gr')
                    sAvgFileName = sFilePath + sAvgFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'Gr')
                elif (nPixelSelect == PixelSelect.OnlyGbPixel):
                    sStdFileName = sFilePath + sStdFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'Gb')
                    sAvgFileName = sFilePath + sAvgFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'Gb')
                elif (nPixelSelect == PixelSelect.OnlyBPixel):
                    sStdFileName = sFilePath + sStdFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'B')
                    sAvgFileName = sFilePath + sAvgFileTempName.format(sFileTempTime, nFileIndex, nFileExposureID, 'B')
                #print(sStdFileName)

                lCsvRow = []
                with open(sStdFileName, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    lCsvRow = [row[g] for row in reader]
                    #print('STD: ', lCsvRow)
                #print('STD: ', lCsvRow[h])
                lCsvStdRow.append(lCsvRow[h])

                lCsvRow.clear()
                with open(sAvgFileName, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    lCsvRow = [row[g] for row in reader]
                    #print('AVG: ', lCsvRow)
                #print('AVG: ', lCsvRow[h])
                lCsvAvgRow.append(lCsvRow[h])

            #print(lCsvStdRow)
            #print(lCsvAvgRow)
            Save_CSV(sSaveTotalFile, lCsvAvgRow)
            Save_CSV(sSaveTotalFile, lCsvStdRow)

            PixelTime = time.time()
            print("Durning Pixel[{}:{}] Time(sec): {}".format(g, h, PixelTime - StartTime))

if __name__ == "__main__":
    OrganizePixel()

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)