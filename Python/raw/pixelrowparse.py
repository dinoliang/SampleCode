import numpy as np
import time
import csv
import datetime

StartTime = time.time()


#######################################################
nWidth = 8000
nHeight = 6000

nFileCount = 100
sFilePath = '/home/dino/RawShared/DtSample80006000Raw002/'
sFileTempTime = '20211104112051'
sFileTempFormat = 'P10'

nROI_X = 0
nROI_Y = 0
nROI_W = 8000
nROI_H = 1

sSavePath = '/home/dino/RawShared/Output/'
#######################################################


sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}.raw'
sSaveStdFile = 'test_std_{}.csv'
sSaveAvgFile = 'test_avg_{}.csv'

PixelRow_array = np.zeros((nFileCount, nROI_W))
lCsvStdRow = []
lCsvAvgRow = []

NowDate = datetime.datetime.now()
TimeInfo = '{}{}{}{}{}{}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
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
        csv_writer.writerow(RowInfo)

def Cal_Information(y, PixelRowArray):
    Pixel_STD = np.std(PixelRowArray, 1)
    Pixel_AVG = np.average(PixelRowArray, 1)
    #print('Pixel [{}]: STD:{} AVG:{}'.format(y, Pixel_STD, Pixel_AVG))
    lCsvStdRow.append(Pixel_STD)
    lCsvAvgRow.append(Pixel_AVG)

for i in range(nROI_Y, nROI_Y+nROI_H):
    lCsvStdRow.clear()
    lCsvAvgRow.clear()
    for k in range(0, nFileCount):
        sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k)
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