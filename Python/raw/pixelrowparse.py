import numpy as np
import time
import csv
import datetime

StartTime = time.time()


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
#######################################################

# Normal
#sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}.raw'
# Exposure
sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}_{5:d}_{6:d}.raw'
sSaveStdFile = 'test_std_{}.csv'
sSaveAvgFile = 'test_avg_{}.csv'

PixelRow_array = np.zeros((nFileCount, nROI_W))
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
    Pixel_STD = np.std(PixelRowArray, 0)
    Pixel_AVG = np.average(PixelRowArray, 0)
    #print('Pixel [{}]: STD:{} AVG:{}'.format(y, Pixel_STD, Pixel_AVG))
    #lCsvStdRow.append(Pixel_STD)
    #lCsvAvgRow.append(Pixel_AVG)
    lCsvStdRow.extend(Pixel_STD.tolist())
    #print(lCsvStdRow)
    lCsvAvgRow.extend(Pixel_AVG.tolist())
    #print(lCsvAvgRow)

for i in range(nROI_Y, nROI_Y+nROI_H):
    lCsvStdRow.clear()
    lCsvAvgRow.clear()
    for k in range(0, nFileCount):
        #sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k)
        sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k+((nFileExposureIM-1)*nFileExposureCount), nFileExposureIM, nFileExposureID)
        #print('File: ' + sFileTemp)
        nPixelOffset = nWidth * i + nROI_X * 2
        #print(nPixelOffset)
        input_file = open(sFileTemp, 'rb')
        input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W, sep="", offset=nPixelOffset)
        input_file.close()
        PixelRow_array[k] = input_array
        #print(PixelRow_array[k])
    Cal_Information(i, PixelRow_array)
    Save_CSV(sSaveStdFile, lCsvStdRow)
    Save_CSV(sSaveAvgFile, lCsvAvgRow)
    RowTime = time.time()
    print("Durning Row Time(sec): ", RowTime - StartTime)

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)