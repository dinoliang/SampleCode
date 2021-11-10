#######################################################
### One pixel std and avg.
### Save one pixel to every csv

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
    for g in range(nY, nY+nHeight):
        for h in range(nX, nX+nWidth):
            sSaveStdFile = sSavePath+sSaveStdTempFile.format(sFileTempTime, h, g)
            sSaveAvgFile = sSavePath+sSaveAvgTempFile.format(sFileTempTime, h, g)
            #print(sSaveStdFile)
            #print(sSaveAvgFile)
            lCsvStdRow.clear()
            lCsvAvgRow.clear()
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
            if os.path.exists(sSaveStdFile):
                os.remove(sSaveStdFile)
            Save_CSV(sSaveStdFile, lCsvStdRow)
            if os.path.exists(sSaveAvgFile):
                os.remove(sSaveAvgFile)
            Save_CSV(sSaveAvgFile, lCsvAvgRow)

            PixelTime = time.time()
            print("Durning Pixel[{}:{}] Time(sec): {}".format(g, h, PixelTime - StartTime))

if __name__ == "__main__":
    OrganizePixel()

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)