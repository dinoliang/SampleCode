import numpy as np
import time
import csv
import datetime

StartTime = time.time()


#######################################################
nWidth = 8000
nHeight = 6000

nFileCount = 20
sFilePath = '/home/dino/RawShared/DtSample80006000Raw002/'
sFileTempTime = '20211104112051'
sFileTempFormat = 'P10'

nROI_X = 3900
nROI_Y = 2900
nROI_W = 200
nROI_H = 200

sSavePath = '/home/dino/RawShared/Output/'
#######################################################


sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}.raw'
sSaveStdFile = 'test_std_{}.csv'
sSaveAvgFile = 'test_avg_{}.csv'

Pixel_array = np.zeros(nFileCount)
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

def Cal_Information(x, y, PixelArray):
    Pixel_STD = np.std(PixelArray)
    Pixel_AVG = np.average(PixelArray)
    print('Pixel [{},{}]: STD:{} AVG:{}'.format(j, i, Pixel_STD, Pixel_AVG))
    lCsvStdRow.append(Pixel_STD)
    lCsvAvgRow.append(Pixel_AVG)

for i in range(nROI_Y, nROI_Y+nROI_H):
    lCsvStdRow.clear()
    lCsvAvgRow.clear()
    for j in range(nROI_X, nROI_X+nROI_W):
        for k in range(0, nFileCount):
            sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k)
            #print('File: ' + sFileTemp)
            nPixelOffset = nWidth * i + j*2
            #print(nPixelOffset)
            input_file = open(sFileTemp, 'rb')
            input_array = np.fromfile(input_file, dtype=np.uint16, count=1, sep="", offset=nPixelOffset)
            input_file.close()
            Pixel_array[k] = input_array[0]
            #print(Pixel_array[k])
        Cal_Information(j, i, Pixel_array)
    Save_CSV(sSaveStdFile, lCsvStdRow)
    Save_CSV(sSaveAvgFile, lCsvAvgRow)
    RowTime = time.time()
    print("Durning Row Time(sec): ", RowTime - StartTime)

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)