import numpy as np
import time
import csv
import datetime
import enum

StartTime = time.time()

class PixelSelect(enum.IntEnum):
    AllPixel = 0
    OnlyRPixel = 1
    OnlyGrPixel = 2
    OnlyGbPixel = 3
    OnlyBPixel = 4
    AutoSplit = 5


#######################################################
nWidth = 8000
nHeight = 6000

nFileCount = 10
sFilePath = '/home/dino/RawShared/ExposureRaw001/'
sFileTempTime = '20211104173158'
sFileTempFormat = 'P10'

nFileExposureIM = 1
nFileExposureID = 30
nFileExposureCount = 10

nROI_X = 3900
nROI_Y = 2900
nROI_W = 200
nROI_H = 200

sSavePath = '/home/dino/RawShared/Output/'

nPixelSelect = PixelSelect.AllPixel
#######################################################

# Normal
#sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}.raw'
# Exposure
sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}_{5:d}_{6:d}.raw'
sSaveStdFile = 'test_std_{}.csv'
sSaveAvgFile = 'test_avg_{}.csv'

#PixelRow_array = np.zeros((nFileCount, nROI_W))
lCsvStdRow = []
lCsvAvgRow = []

NowDate = datetime.datetime.now()
TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
#print(TimeInfo)
sSaveStdFile = sSavePath+sSaveStdFile.format(TimeInfo)
sSaveAvgFile = sSavePath+sSaveAvgFile.format(TimeInfo)
#print(sSaveStdFile)
#print(sSaveAvgFile)

def Save_CSV(FileName, RowInfo):
    with open(FileName, 'a+') as f:
        # create the csv writer
        csv_writer = csv.writer(f)
        # write a row to the csv file
        #print(RowInfo)
        csv_writer.writerow(RowInfo)

def Cal_Information(y, PixelRowArray):
    #print(PixelRowArray)
    Pixel_STD = np.std(PixelRowArray, 0)
    Pixel_AVG = np.average(PixelRowArray, 0)
    #print('Pixel [{}]: STD:{} AVG:{}'.format(y, Pixel_STD, Pixel_AVG))
    #lCsvStdRow.append(Pixel_STD)
    #lCsvAvgRow.append(Pixel_AVG)
    lCsvStdRow.extend(Pixel_STD.tolist())
    lCsvAvgRow.extend(Pixel_AVG.tolist())
    #print(lCsvStdRow)
    #print(lCsvAvgRow)

def ParsingPixel():
    for i in range(nROI_Y, nROI_Y+nROI_H):
        lCsvStdRow.clear()
        lCsvAvgRow.clear()
        bNeedCal = False
        if nPixelSelect == PixelSelect.AllPixel:
            # do nothing
            #pass
            #None
            PixelRow_array = np.zeros((nFileCount, nROI_W))
        elif (nPixelSelect == PixelSelect.OnlyRPixel) and (i%4!=0 and i%4!=1):
            continue
        elif (nPixelSelect == PixelSelect.OnlyGrPixel) and (i%4!=0 and i%4!=1):
            continue
        elif (nPixelSelect == PixelSelect.OnlyGbPixel) and (i%4!=2 and i%4!=3):
            continue
        elif (nPixelSelect == PixelSelect.OnlyBPixel) and (i%4!=2 and i%4!=3):
            continue
        else:
            PixelRow_array = np.zeros((nFileCount, nROI_W//2))

        for k in range(0, nFileCount):
            bNeedCal = True
            #sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k)
            sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k+((nFileExposureIM-1)*nFileExposureCount), nFileExposureIM, nFileExposureID)
            #print('File: ' + sFileTemp)
            nPixelOffset = nWidth * i + nROI_X * 2
            #print(nPixelOffset)
            input_file = open(sFileTemp, 'rb')
            input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W, sep="", offset=nPixelOffset)
            input_file.close()
            
            RemoveList = []
            if nPixelSelect == PixelSelect.AllPixel:
                # do nothing
                #pass
                #None
                PixelRow_array[k] = input_array
            elif nPixelSelect == PixelSelect.OnlyRPixel:
                if (i%4==0 or i%4==1):
                    for l in range(0, nROI_W):
                        nIndex = nROI_X + l
                        if (nIndex%4==2 or nIndex%4==3):   #Gr
                            RemoveList.append(l)
                    PixelRow_array[k] = np.delete(input_array, RemoveList)
            elif nPixelSelect == PixelSelect.OnlyGrPixel:
                if (i%4==0 or i%4==1):
                    for l in range(0, nROI_W):
                        nIndex = nROI_X + l
                        if (nIndex%4==0 or nIndex%4==1):   #R
                            RemoveList.append(l)
                    PixelRow_array[k] = np.delete(input_array, RemoveList)
            elif nPixelSelect == PixelSelect.OnlyGbPixel:
                if (i%4==2 or i%4==3):
                    for l in range(0, nROI_W):
                        nIndex = nROI_X + l
                        if (nIndex%4==2 or nIndex%4==3):   #B
                            RemoveList.append(l)
                    PixelRow_array[k] = np.delete(input_array, RemoveList)
            elif nPixelSelect == PixelSelect.OnlyBPixel:
                if (i%4==2 or i%4==3):
                    for l in range(0, nROI_W):
                        nIndex = nROI_X + l
                        if (nIndex%4==0 or nIndex%4==1):   #Gb
                            RemoveList.append(l)
                    PixelRow_array[k] = np.delete(input_array, RemoveList)
            #print(PixelRow_array[k])

        if bNeedCal:
            #print(PixelRow_array)
            Cal_Information(i, PixelRow_array)
            Save_CSV(sSaveStdFile, lCsvStdRow)
            Save_CSV(sSaveAvgFile, lCsvAvgRow)
            RowTime = time.time()
            print("Durning Row Time(sec): ", RowTime - StartTime)

if __name__ == "__main__":
    ParsingPixel()

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)