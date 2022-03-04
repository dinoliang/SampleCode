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
sFilePath = '/home/dino/RawShared/Temp/Temp6/{}/'
#sFilePath = '/home/dino/IMX586_Raw2/2022012517/{}/'
#sFilePath = '/home/dino/IMX586_Bin/2022030116_color_EQE_NoCG_1713/{}/'

#There is header data, and the extenstion file name is *.bin in AYA file
g_bAYAFile = True

#Subfolder
#Normal
g_sFilePathFolder = [
                    '250_Bin'
                    ]

#LightIntensity
#g_sFilePathFolder = [
#                    '20211118093237', '20211118094433', '20211118094925', '20211118095420', '20211118095940' \
#                    ]

#ExposureTime
#g_sFilePathFolder = [
#                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
#                    ]
                    
#AngulerResponse
#g_sFilePathFolder = [
#                    '-40', \
#                    '-39', '-38', '-37', '-36','-35', '-34', '-33', '-32', '-31', '-30', \
#                   '-29', '-28', '-27', '-26','-25', '-24', '-23', '-22', '-21', '-20', \
#                    '-19', '-18', '-17', '-16','-15', '-14', '-13', '-12', '-11', '-10', \
#                    '-9', '-8', '-7', '-6','-5', '-4', '-3', '-2', '-1', \
#                    '0', \
#                    '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', \
#                    '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20', \
#                   '+21', '+22', '+23', '+24', '+25', '+26', '+27', '+28', '+29', '+30', \
#                    '+31', '+32', '+33', '+34', '+35', '+36', '+37', '+38', '+39', '+40' \
#                    ]

#QuantumEfficiency
#g_sFilePathFolder = [
#                    '400', \
#                    '410', '420', '430', '440', '450',  '460', '470', '480', '490', '500', \
#                    '510', '520', '530', '540', '550',  '560', '570', '580', '590', '600', \
#                   '610', '620', '630', '640', '650',  '660', '670', '680', '690', '700', \
#                   '710', '720', '730', '740', '750',  '760', '770', '780' \
#                  ]

#DarkCurrent
#g_sFilePathFolder = [
#                    '80_1_10', '80_2_10', '80_3_10', '80_4_10', '80_5_10', '80_6_10', '80_7_10', '80_8_10', '80_9_10', '80_10_10', \
#                    '75_1_10', '75_2_10', '75_3_10', '75_4_10', '75_5_10', '75_6_10', '75_7_10', '75_8_10', '75_9_10', '75_10_10', \
#                    '70_1_10', '70_2_10', '70_3_10', '70_4_10', '70_5_10', '70_6_10', '70_7_10', '70_8_10', '70_9_10', '70_10_10', \
#                    '65_1_10', '65_2_10', '65_3_10', '65_4_10', '65_5_10', '65_6_10', '65_7_10', '65_8_10', '65_9_10', '65_10_10', \
#                    '60_1_10', '60_2_10', '60_3_10', '60_4_10', '60_5_10', '60_6_10', '60_7_10', '60_8_10', '60_9_10', '60_10_10', \
#                    '55_1_10', '55_2_10', '55_3_10', '55_4_10', '55_5_10', '55_6_10', '55_7_10', '55_8_10', '55_9_10', '55_10_10', \
#                    '50_1_10', '50_2_10', '50_3_10', '50_4_10', '50_5_10', '50_6_10', '50_7_10', '50_8_10', '50_9_10', '50_10_10', \
#                    '25_1_10', '25_2_10', '25_3_10', '25_4_10', '25_5_10', '25_6_10', '25_7_10', '25_8_10', '25_9_10', '25_10_10', \
#                     '25', '50', '75', '100', '125', '150',
#                   ]

nROI_W = nWidth
nROI_H = nHeight

#Saving output file or not
bSaveCSV = True

#The path of saving file
sFileTempTime = '20220303'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021111810/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021112914/4000_3000/600/{}/'
sSavePath = '/home/dino/RawShared/Output/Temp/Temp/{}/'
#sSavePath = '/home/dino/RawShared/Output/2022030116_color_EQE_NoCG_1713/{}/'

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

def SaveDiffToCSV(Diff_Array, no):
    sDiffFile = '{}{}_Diff_{}.csv'.format(sSavePath.format('Total'), sFileTempTime, no)
    np.savetxt(sDiffFile, Diff_Array, fmt = '%d', delimiter=',')

def LoadDiffFromCSV(no):
    sDiffFile = '{}{}_Diff_{}.csv'.format(sSavePath.format('Total'), sFileTempTime, no)
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
                    SaveDiffToCSV(DiffArray, k)
                    nEachDiffTime = time.time()
                    print("Durning Diff[{}] Time(sec): {}".format(x, nEachDiffTime - StartTime))
                
                k = k + 1

        nEachIntervalTime = time.time()
        print("Durning Interval[{}] Time(sec): {}".format(x, nEachIntervalTime - StartTime))

if __name__ == "__main__":
    ParsingPixel()

    ##Test
    #for i in range(0, nFileCount):
    #    LoadArray = LoadDiffFromCSV(i)
    #    ShowHistogram(LoadArray)
    
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
