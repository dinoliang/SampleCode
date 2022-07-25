#######################################################
### Get one row data to calculate.
### Calculate block(R1~4/Gr1~4/Gb1~4/B1~4) std and avg.
### If R1/Gr1/Gb1/B1 only has only 1 pixel, the result is like to calculate one pixel. (nROI_W <= 4 && nROI_H <= 4)
### If R1/Gr1/Gb1/B1 only has more 1 pixel, the result is to calculate all pixels of every R1~4/Gr1~4/Gb1~4/B1~4 channel.
### If bCalMergeROIChannel is True, the result is to calculate all pixels of R(1+2+3+4)/Gr(1+2+3+4)/Gb(1+2+3+4)/B(1+2+3+4) channel.

import numpy as np
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

#Color TEG
nWidth = 9728
nHeight = 8192

nFileCount = 7
#sFilePath = '/home/dino/RawShared/2022020816/{}/'
#sFilePath = '/home/dino/RawShared/Temp/Temp5/{}/'
#sFilePath = '/home/dino/IMX586_Raw2/2022012517/{}/'
sFilePath = '/home/dino/IMX586_Bin/2022042009_P8533_EQE_#2/{}/'

#There is header data, and the extenstion file name is *.bin in AYA file
g_bAYAFile = True

#Subfolder
#Normal
#g_sFilePathFolder = [
#                    '540'
#                    ]

#LightIntensity
#g_sFilePathFolder = [
#                    '20211118093237', '20211118094433', '20211118094925', '20211118095420', '20211118095940' \
#                    ]

#ExposureTime
#g_sFilePathFolder = [
#                    '0x0010', '0x0020', '0x0030', '0x0040', '0x0050', '0x0060', '0x0070', '0x0080', '0x0090', '0x00A0', '0x00B0', '0x00C0', \
#                    '0x010', '0x080', '0x100', '0x180', '0x200', '0x280', '0x300', \
#                    '0x310', '0x320', '0x330', '0x340', '0x350', '0x360', '0x370', '0x380', '0x390', '0x3A0', '0x3B0', '0x3C0', '0x3D0', '0x3E0', '0x3F0', '0x400', \
#                    '0x480', '0x500', \
#                    ]
                    
#AngulerResponse
#g_sFilePathFolder = [
#                    '-40', '-39', '-38', '-37', '-36',\
#                    '-35', '-34', '-33', '-32', '-31', '-30', \
#                    '-29', '-28', '-27', '-26','-25', '-24', '-23', '-22', '-21', '-20', \
#                    '-26', '-25', '-24', '-23', '-22', '-21', '-20', \
#                    '-19', '-18', '-17', '-16','-15', '-14', '-13', '-12', '-11', '-10', \
#                    '-9', '-8', '-7', '-6','-5', '-4', '-3', '-2', '-1', \
#                    '0', \
#                    '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', \
#                    '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20', \
#                    '+21', '+22', '+23', '+24', \
#                    '+21', '+22', '+23', '+24', '+25', '+26', '+27', '+28', '+29', '+30', \
#                    '+31', '+32', '+33', '+34', '+35', \
#                    '+36', '+37', '+38', '+39', '+40' \
#                    ]
#AngulerResponse_VisEra
#g_sFilePathFolder = [
#                    '-34', '-32', '-30', \
#                    '-28', '-26', '-24', '-22', '-20', \
#                    '-18', '-16', '-14', '-12', '-10', \
#                    '-8', '-6', '-4', '-2', \
#                    '0', \
#                    '+2', '+4', '+6', '+8', '+10', \
#                    '+12', '+14', '+16', '+18', '+20', \
#                    '+22', '+24', '+26', '+28', '+30', \
#                    '+32', '+34', \
#                    ]

#QuantumEfficiency
g_sFilePathFolder = [
                    '400', \
                    '410', '420', '430', '440', '450',  '460', '470', '480', '490', '500', \
                    '510', '520', '530', '540', '550',  '560', '570', '580', '590', '600', \
                    '610', '620', '630', '640', '650',  '660', '670', '680', '690', '700', \
                    '710', '720', '730', '740', '750',  '760', '770', '780' \
                    ]

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

#Center R1: 4000,3000
#nROI_X = 3900
#nROI_Y = 2900

#Color TEG
#Center R1: 4866,4096
nROI_X = 4766
nROI_Y = 3996
#nROI_X = 3167
#nROI_Y = 2397
#PDAF: B3+Gb4
#Center
#Center
#nROI_X = 4764
#nROI_Y = 3998
#Top-Left
#nROI_X = 272
#nROI_Y = 32
#Top-Right
#nROI_X = 9260
#nROI_Y = 32
#Bottom-Right
#nROI_X = 9196
#nROI_Y = 6796
#Bottom-Left
#nROI_X = 272
#nROI_Y = 6796

#Special
#nROI_X = 535
#nROI_Y = 983

nROI_W = 200    #multiple of 4
nROI_H = 200    #multiple of 4

gCol1_Index = 0     #R1、R2、Gr1、Gr2
gCol2_Index = 1     #R3、R4、Gr3、Gr4
gCol3_Index = 2     #Gb1、Gb2、B1、B2
gCol4_Index = 3     #Gb3、Gb4、B3、B4
#IMX586:
#gRow1_Index = 0     #R1、R3、Gb1、Gb3
#gRow2_Index = 1     #R2、R4、Gb2、Gb4
#gRow3_Index = 2     #Gr1、Gr3、B1、B3
#gRow4_Index = 3     #Gr2、Gr4、B2、B4
#TEG:
gRow1_Index = 2     #R1、R3、Gb1、Gb3
gRow2_Index = 3     #R2、R4、Gb2、Gb4
gRow3_Index = 0     #Gr1、Gr3、B1、B3
gRow4_Index = 1     #Gr2、Gr4、B2、B4

#Regular Expression for parsing file
g_re_FilePattern = ""
g_nSelect_HSValue = 100 #0:select 0, -1:select -1, 1:select 1, 100:not select

#Saving output file or not
bSaveCSV = True

#The path of saving file
sFileTempTime = '2022072510'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021111810/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021112914/4000_3000/600/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/Temp/{}/'
sSavePath = '/home/dino/RawShared/Output/2022042009_P8533_EQE_#2_Python/{}/'

#CalROI: R:R1+R2+R3+R4 / Gr:Gr1+Gr2+Gr3+Gr4 / Gb:Gb1+Gb2+Gb3+Gb4 / B:B1+B2+B3+B4
bCalMergeROIChannel = False
bSaveCSV_ROI = False

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

gCaller = None
gCallbackMessageFunc = None

#Regular Expression of raw file
g_re_FilePattern_raw = "[a-zA-Z0-9-_]+(.raw)"
#Regular Expression of AYA(bin) file
g_re_FilePattern_bin = "[a-zA-Z0-9-_]+(.bin)"

g_FilePattern_HS0 = "(HS0)"
g_FilePattern_HSN1 = "(HS-1)"
g_FilePattern_HSP1 = "(HS1)"

g_nRawBeginIndex = 0

sSaveTempFile = '{}_Single_{}.csv'
sSaveOrganizeTempFile = '{}_{}.csv'

if not g_bAYAFile:
    g_re_FilePattern = g_re_FilePattern_raw
    g_nRawBeginIndex = 0
else:
    g_re_FilePattern = g_re_FilePattern_bin
    g_nRawBeginIndex = 4    # header (width + height)

#reference by np.zeros
g_nArrayDefaultValue = 0

#PixelRow_array = np.zeros((nFileCount, nROI_W))
lCsvStdRow = []
lCsvAvgRow = []

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
TimeInfo = sFileTempTime
#print(TimeInfo)

#Check the file is raw/bin file
def Check_File(sFileName, rePattern):
    if re.fullmatch(rePattern, sFileName):
        #if bShowDebugOutput:
        #    print("{0} Is right file.. (RE:{1})".format(sFileName, rePattern))
        return True
    else:
        if bShowDebugOutput:
            print("{0} Is Not right file.. (RE:{1})".format(sFileName, rePattern))
    return False

def Check_FileHS(sFileName, rePattern):
    if re.search(rePattern, sFileName):
        #if bShowDebugOutput:
        #    print("{0} Is right file.. (RE:{1})".format(sFileName, rePattern))
        return True
    else:
        if bShowDebugOutput:
            print("{0} Is Not right file.. (RE:{1})".format(sFileName, rePattern))
    return False

#Save output file
def Save_CSV(FileName, RowInfo):
    if not bSaveCSV:
        return
    with open(FileName, 'a+') as f:
        # create the csv writer
        csv_writer = csv.writer(f)
        # write a row to the csv file
        #print(RowInfo)
        csv_writer.writerow(RowInfo)

#Calculate AVG/STD 
def Cal_Information(y, nCount, ChannelArray, sColor):
    for i in range(0, nCount+1):
        if i < nCount:
            for j in range(0, 4):
                lCsvStdRow.append('{}_STD_{}{}'.format(i, sColor, j+1))
                #print(lCsvStdRow)
                Channel_STD = np.std(ChannelArray[i,j])
                lCsvStdRow.append(Channel_STD.tolist())
                #print(lCsvStdRow)
                lCsvAvgRow.append('{}_AVG_{}{}'.format(i, sColor, j+1))
                Channel_AVG = np.average(ChannelArray[i,j])
                lCsvAvgRow.append(Channel_AVG.tolist())
                #print(lCsvStdRow)
                #print(lCsvAvgRow)
        elif i == nCount: # Total
            for j in range(0, 4):
                ChannelAllPixel = ChannelArray[:,j,:].flatten()
                ChannelAllPixel = np.delete(ChannelAllPixel, np.where(ChannelAllPixel == g_nArrayDefaultValue))
                lCsvStdRow.append('Total_STD_{}{}'.format(sColor, j+1))
                Channel_STD = np.std(ChannelAllPixel)
                lCsvStdRow.append(Channel_STD.tolist())
                lCsvAvgRow.append('Total_AVG_{}{}'.format(sColor, j+1))
                Channel_AVG = np.average(ChannelAllPixel)
                lCsvAvgRow.append(Channel_AVG.tolist())
        #print(lCsvStdRow)
        #print(lCsvAvgRow)


def Cal_Save_AllInformation(y, nCount, ChannelArray, sColor, sSaveFileName, sSaveOrgFile):
    #print(ChannelArray)
    #print('')
    lRawInfo = []
    lRawInfo.clear()
    if not bSaveCSV_ROI:
        lRawInfo = ['', 'Ch1_AVG', 'Ch1_STD', 'Ch2_AVG', 'Ch2_STD', 'Ch3_AVG', 'Ch3_STD', 'Ch4_AVG', 'Ch4_STD']
    else:
        lRawInfo = ['', 'Ch_AVG', 'Ch_STD']
    Save_CSV(sSaveFileName, lRawInfo)
    for i in range(0, nCount+1):
        if i < nCount:
            lRawInfo.clear()
            lRawInfo.append('Frame{}'.format(i))
            for j in range(0, 4):
                #print(ChannelArray[i,j])
                ChannelAllPixel = ChannelArray[i,j].flatten()
                ChannelAllPixel = np.delete(ChannelAllPixel, np.where(ChannelAllPixel == g_nArrayDefaultValue))
                #if sColor == 'B':
                #    print('Frame{:03d}_{}{}: {}:{}'.format(i, sColor, j+1, np.size(ChannelAllPixel), ChannelAllPixel))
                #    for z in range(0, np.size(ChannelAllPixel)):
                #        print('Frame{:03d}_{}{}: Pixel:{}'.format(i, sColor, j+1, ChannelAllPixel[z]))
                #if bShowDebugOutput:
                #    print('Frame{:03d}_{}{}: {}'.format(i, sColor, j+1, ChannelAllPixel))
                #print(ChannelAllPixel)
                #Channel_AVG = np.average(ChannelArray[i,j])
                Channel_AVG = np.average(ChannelAllPixel)
                lRawInfo.append(Channel_AVG.tolist())
                #Channel_STD = np.std(ChannelArray[i,j])
                Channel_STD = np.std(ChannelAllPixel)
                lRawInfo.append(Channel_STD.tolist())
            Save_CSV(sSaveFileName, lRawInfo)
        elif i == nCount: # Total
            lRawOrglInfo = []
            lRawOrglInfo.clear()
            lRawOrglInfo.append('{}'.format(g_sFilePathFolder[y]))
            lRawInfo.clear()
            lRawInfo.append('FrameTotal')
            for j in range(0, 4):
                #print("({},{},{})".format(i, j, sColor))
                ChannelAllPixel = ChannelArray[:,j,:].flatten()
                ChannelAllPixel = np.delete(ChannelAllPixel, np.where(ChannelAllPixel == g_nArrayDefaultValue))
                if bShowDebugOutput:
                    print('OnePixel_{}{}: Count={} {}'.format(sColor, j+1, np.size(ChannelAllPixel), ChannelAllPixel))
                #print(ChannelAllPixel)
                
                #mask = np.logical_or(ChannelAllPixel == ChannelAllPixel.max(keepdims = 1), ChannelAllPixel == ChannelAllPixel.min(keepdims = 1))
                #ChannelAllPixel_masked = np.ma.masked_array(ChannelAllPixel, mask = mask)
                #print(ChannelAllPixel_masked)

                if ( bDeleteMaxMin and (np.size(ChannelAllPixel)//10 >= nDeleteMaxCount+nDeleteMinCount) ):
                    MaxIndex = np.argpartition(ChannelAllPixel.ravel(), (0-nDeleteMaxCount))[(0-nDeleteMaxCount):]
                    i2d = np.unravel_index(MaxIndex, ChannelAllPixel.shape)
                    ChannelAllPixel = np.delete(ChannelAllPixel, i2d)
                    MinIndex = np.argpartition(ChannelAllPixel.ravel(), nDeleteMinCount)[:nDeleteMinCount]
                    i2d = np.unravel_index(MinIndex, ChannelAllPixel.shape)
                    ChannelAllPixel = np.delete(ChannelAllPixel, i2d)
                    #print(np.size(ChannelAllPixel))
                
                #print(ChannelAllPixel)
                Channel_AVG = np.average(ChannelAllPixel)
                #print(Channel_AVG)
                lRawOrglInfo.append(Channel_AVG.tolist())
                lRawInfo.append(Channel_AVG.tolist())
                Channel_STD = np.std(ChannelAllPixel)
                #print(Channel_STD)
                lRawOrglInfo.append(Channel_STD.tolist())
                lRawInfo.append(Channel_STD.tolist())

            Save_CSV(sSaveFileName, lRawInfo)
            if not bSaveCSV_ROI:
                Save_CSV(sSaveOrgFile, lRawOrglInfo)

            if bCalMergeROIChannel:
                lRawROIInfo = []
                lRawROIInfo.clear()
                lRawROIInfo.append('{}'.format(g_sFilePathFolder[y]))

                ChannelAllPixel = ChannelArray[:,:,:].flatten()
                ChannelAllPixel = np.delete(ChannelAllPixel, np.where(ChannelAllPixel == g_nArrayDefaultValue))
                if bShowDebugOutput:
                    print('OneChannel_{}: {}'.format(sColor, ChannelAllPixel))
                Channel_AVG = np.average(ChannelAllPixel)
                print('AVG: ', Channel_AVG)
                lRawROIInfo.append(Channel_AVG.tolist())
                Channel_STD = np.std(ChannelAllPixel)
                print('STD: ', Channel_STD)
                lRawROIInfo.append(Channel_STD.tolist())

                if bSaveCSV_ROI:
                    Save_CSV(sSaveOrgFile, lRawROIInfo)


def ParsingPixel():
    nCount = nFileCount
    nRawBeginIndex = g_nRawBeginIndex

    #Get the numbers of every channel
    nR_Gb_Len = nROI_W//4 * nROI_H//4
    nGr_B_Len = nROI_W//4 * nROI_H//4
    #print(nR_Gb_Len)
    #print(nGr_B_Len)

    #Get the leftest pixel offset
    nWOffset = nROI_X % 4

    #Set the save orgnize file (Orgnize result)
    sTempSavePath = sSavePath.format('Total')
    sSaveOrgRFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'R')
    sSaveOrgGrFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'Gr')
    sSaveOrgGbFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'Gb')
    sSaveOrgBFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'B')

    if os.path.exists(sSaveOrgRFile):
        os.remove(sSaveOrgRFile)
    if os.path.exists(sSaveOrgGrFile):
        os.remove(sSaveOrgGrFile)
    if os.path.exists(sSaveOrgGbFile):
        os.remove(sSaveOrgGbFile)
    if os.path.exists(sSaveOrgBFile):
        os.remove(sSaveOrgBFile)
    lRawInfo = []
    lRawInfo.clear()
    lRawInfo = ['', 'Ch1_AVG', 'Ch1_STD', 'Ch2_AVG', 'Ch2_STD', 'Ch3_AVG', 'Ch3_STD', 'Ch4_AVG', 'Ch4_STD']
    Save_CSV(sSaveOrgRFile, lRawInfo)
    Save_CSV(sSaveOrgGrFile, lRawInfo)
    Save_CSV(sSaveOrgGbFile, lRawInfo)
    Save_CSV(sSaveOrgBFile, lRawInfo)

    h = 0
    for x in g_sFilePathFolder:
        sTempFilePath = sFilePath.format(x)
        
        #4 Quad channel (1~4) of 4Channel (R/Gr/Gb/B)
        ChannelR_array = np.zeros((nCount, 4, nR_Gb_Len))
        ChannelGr_array = np.zeros((nCount, 4, nGr_B_Len))
        ChannelGb_array = np.zeros((nCount, 4, nR_Gb_Len))
        ChannelB_array = np.zeros((nCount, 4, nGr_B_Len))
            
        #Set the every channel saving file (R/Gr/Gb/B) (Total)
        sTempSavePath = sSavePath.format(x)
        sSaveRFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'R')
        sSaveGrFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'Gr')
        sSaveGbFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'Gb')
        sSaveBFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'B')

        if os.path.exists(sSaveRFile):
            os.remove(sSaveRFile)
        if os.path.exists(sSaveGrFile):
            os.remove(sSaveGrFile)
        if os.path.exists(sSaveGbFile):
            os.remove(sSaveGbFile)
        if os.path.exists(sSaveBFile):
            os.remove(sSaveBFile)

        if bShowDebugOutput:
            print('TempFilePath: ', sTempFilePath)
        k = 0
        for root, dirs, files in os.walk(sTempFilePath):
            for sFile in files:
                if k >= nCount:
                    continue

                nR0Index, nR1Index, nR2Index, nR3Index = 0, 0, 0, 0
                nGr0Index, nGr1Index, nGr2Index, nGr3Index = 0, 0, 0, 0
                nGb0Index, nGb1Index, nGb2Index, nGb3Index = 0, 0, 0, 0
                nB0Index, nB1Index, nB2Index, nB3Index = 0, 0, 0, 0

                sFileTemp = sFile
                #rePattern = g_re_FilePattern
                #
                #if not Check_File(sFileTemp, rePattern):
                #    continue
                #else:
                #    if g_nSelect_HSValue != 100:
                #        if g_nSelect_HSValue == 0:
                #            if not Check_FileHS(sFileTemp, g_FilePattern_HS0):
                #                continue
                #        elif g_nSelect_HSValue == -1:
                #            if not Check_FileHS(sFileTemp, g_FilePattern_HSN1):
                #                continue
                #        elif g_nSelect_HSValue == 1:
                #            if not Check_FileHS(sFileTemp, g_FilePattern_HSP1):
                #                continue
                #        else:
                #            continue

                sFileTemp = root + '/' + sFileTemp
                print('sFileTemp: ', sFileTemp)
                #Every row
                for i in range(nROI_Y, nROI_Y+nROI_H):
                    bNeedCal = False

                    nPixelOffset = nWidth * i * 2 + nROI_X * 2 + nRawBeginIndex
                    #if i == nROI_Y:
                    #    print('nPixelOffset: ', nPixelOffset)
                    input_file = open(sFileTemp, 'rb')
                    #Get all pixel of one range row
                    input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W, sep="", offset=nPixelOffset)
                    input_file.close()
                    #print('input_array: {0}, Len:{1}'.format(input_array, np.size(input_array)))
                    
                    if i%4==gCol1_Index:  #R1~2+Gr1~2
                        for l in range(0, nROI_W):
                            if g_bDeleteBadPixel and input_array[l] < g_nBadPixelLevel:
                            #    print('Bad Pixel {0}, {1}'.format(l, input_array[l]))
                                continue

                            if (l+nWOffset)%4==gRow1_Index: #R1
                                #print('h:{}, i:{}, k:{}, Index:{}, l:{}'.format(h, i, k, nR0Index, l))
                                ChannelR_array[k,0,nR0Index] = input_array[l]
                                nR0Index += 1
                            elif (l+nWOffset)%4==gRow2_Index: #R2
                                ChannelR_array[k,1,nR1Index] = input_array[l]
                                nR1Index += 1
                            elif (l+nWOffset)%4==gRow3_Index: #Gr1
                                #if nGr0Index == 0:
                                #    print('{}: {}'.format(k, input_array[l]))
                                ChannelGr_array[k,0,nGr0Index] = input_array[l]
                                nGr0Index += 1
                            elif (l+nWOffset)%4==gRow4_Index: #Gr2
                                ChannelGr_array[k,1,nGr1Index] = input_array[l]
                                nGr1Index += 1
                    elif i%4==gCol2_Index:  #R3~4+Gr3~4
                        for l in range(0, nROI_W):
                            if g_bDeleteBadPixel and input_array[l] < g_nBadPixelLevel:
                            #    print('Bad Pixel {0}, {1}'.format(l, input_array[l]))
                                continue

                            if (l+nWOffset)%4==gRow1_Index: #R3
                                ChannelR_array[k,2,nR2Index] = input_array[l]
                                nR2Index += 1
                            elif (l+nWOffset)%4==gRow2_Index: #R4
                                ChannelR_array[k,3,nR3Index] = input_array[l]
                                nR3Index += 1
                            elif (l+nWOffset)%4==gRow3_Index: #Gr3
                                ChannelGr_array[k,2,nGr2Index] = input_array[l]
                                nGr2Index += 1
                            elif (l+nWOffset)%4==gRow4_Index: #Gr4
                                ChannelGr_array[k,3,nGr3Index] = input_array[l]
                                nGr3Index += 1
                    elif i%4==gCol3_Index:  #Gb1~2+B1~2
                        for l in range(0, nROI_W):
                            if g_bDeleteBadPixel and input_array[l] < g_nBadPixelLevel:
                            #    print('Bad Pixel {0}, {1}'.format(l, input_array[l]))
                                continue

                            if (l+nWOffset)%4==gRow1_Index: #Gb1
                                ChannelGb_array[k,0,nGb0Index] = input_array[l]
                                nGb0Index += 1
                            elif (l+nWOffset)%4==gRow2_Index: #Gb2
                                ChannelGb_array[k,1,nGb1Index] = input_array[l]
                                nGb1Index += 1
                            elif (l+nWOffset)%4==gRow3_Index: #B1
                                ChannelB_array[k,0,nB0Index] = input_array[l]
                                nB0Index += 1
                            elif (l+nWOffset)%4==gRow4_Index: #B2
                                ChannelB_array[k,1,nB1Index] = input_array[l]
                                nB1Index += 1
                    elif i%4==gCol4_Index:  #Gb3~4+B3~4
                        for l in range(0, nROI_W):
                            if g_bDeleteBadPixel and input_array[l] < g_nBadPixelLevel:
                            #    print('Bad Pixel {0}, {1}'.format(l, input_array[l]))
                                continue

                            if (l+nWOffset)%4==gRow1_Index: #Gb3
                                ChannelGb_array[k,2,nGb2Index] = input_array[l]
                                nGb2Index += 1
                            elif (l+nWOffset)%4==gRow2_Index: #Gb4
                                ChannelGb_array[k,3,nGb3Index] = input_array[l]
                                nGb3Index += 1
                            elif (l+nWOffset)%4==gRow3_Index: #B3
                                ChannelB_array[k,2,nB2Index] = input_array[l]
                                nB2Index += 1
                            elif (l+nWOffset)%4==gRow4_Index: #B4
                                ChannelB_array[k,3,nB3Index] = input_array[l]
                                nB3Index += 1
                k = k + 1

        Cal_Save_AllInformation(h, nCount, ChannelR_array, 'R', sSaveRFile, sSaveOrgRFile)

        Cal_Save_AllInformation(h, nCount, ChannelGr_array, 'Gr', sSaveGrFile, sSaveOrgGrFile)

        Cal_Save_AllInformation(h, nCount, ChannelGb_array, 'Gb', sSaveGbFile, sSaveOrgGbFile)

        Cal_Save_AllInformation(h, nCount, ChannelB_array, 'B', sSaveBFile, sSaveOrgBFile)

        h = h + 1
        nEachIntervalTime = time.time()
        print("Durning Each Interval:{} Time(sec): {}".format(h, nEachIntervalTime - StartTime))

        if gCallbackMessageFunc != None and gCaller != None:
            gCallbackMessageFunc(gCaller, 'Parse finish. (zett)')

        return

def CallMain(nWidth, nHeight, nX, nY, nROI_W, nROI_H, nColIndex, nRowIndex, nFileCounts, FileTimeStamp, InputFolder, OutputFolder, ArrayFolder, Caller, CallbackMsgFunc):
    listVarOfGlobals = globals()
    listVarOfGlobals['nWidth']                      = nWidth
    listVarOfGlobals['nHeight']                     = nHeight

    listVarOfGlobals['nROI_X']                      = nX
    listVarOfGlobals['nROI_Y']                      = nY
    listVarOfGlobals['nROI_W']                      = nROI_W
    listVarOfGlobals['nROI_H']                      = nROI_H

    listVarOfGlobals['gCol1_Index']                 = nColIndex
    listVarOfGlobals['gCol2_Index']                 = (nColIndex + 1) % 4
    listVarOfGlobals['gCol3_Index']                 = (nColIndex + 2) % 4
    listVarOfGlobals['gCol4_Index']                 = (nColIndex + 3) % 4

    listVarOfGlobals['gRow1_Index']                 = nRowIndex
    listVarOfGlobals['gRow2_Index']                 = (nRowIndex + 1) % 4
    listVarOfGlobals['gRow3_Index']                 = (nRowIndex + 2) % 4
    listVarOfGlobals['gRow4_Index']                 = (nRowIndex + 3) % 4

    listVarOfGlobals['nFileCount']                  = nFileCounts
    listVarOfGlobals['sFilePath']                   = InputFolder
    listVarOfGlobals['sFileTempTime']               = FileTimeStamp
    listVarOfGlobals['TimeInfo']                    = FileTimeStamp

    listVarOfGlobals['sSavePath']                   = OutputFolder

    print(listVarOfGlobals['g_sFilePathFolder'])
    listVarOfGlobals['g_sFilePathFolder']           = ArrayFolder
    print(listVarOfGlobals['g_sFilePathFolder'])

    listVarOfGlobals['gCaller']                     = Caller
    listVarOfGlobals['gCallbackMessageFunc']        = CallbackMsgFunc
    #gCallbackMessageFunc(gCaller, 'Test Message')

    #ParsingPixel()
    pass

#def CallMes(CallbackMsg):
#    listVarOfGlobals = globals()
#    listVarOfGlobals['gCallbackMessageFunc']        = CallbackMsg
#    gCallbackMessageFunc('Callback test')
#    return

if __name__ == "__main__":
    ParsingPixel()
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)


###########################################
#def get_channels(bayer_image):
#    red = bayer_image[0::2,0::2]
#    blue = bayer_image[1::2,1::2]
#   green1 = bayer_image[0::2,1::2]
#   green2 = bayer_image[1::2,0::2]
#   green = (green1 + green2)/2
#   return red, green, blue
##########################################
