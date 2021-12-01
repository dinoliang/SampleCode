#######################################################
### Get one row data to calculate.
### Calculate block(R1~4/Gr1~4/Gb1~4/B1~4) std and avg.

import numpy as np
import time
import csv
import datetime
import enum
import os
import re

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
nWidth = 8000
nHeight = 6000

nFileCount = 200
sFilePath = '/home/dino/RawShared/2021111810/{}/'
#sFilePath = '/home/dino/RawShared/2021112914/600/{}/'
#sFilePath = '/home/dino/RawShared/2021113014/AngularSample/{}/'

#LightIntensity
g_sFilePathFolder = [
                    '20211118093237', '20211118094433', '20211118094925', '20211118095420', '20211118095940' \
                    ]

#ExposureTime
#g_sFilePathFolder = [
#                    '25', '26', '27', '28', '29', '30', \
#                    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'
#                    ]
                    
#AngulerResponse
#g_sFilePathFolder = [
#                    '-35', '-34', '-33', '-32', '-31', '-30', \
#                    '-29', '-28', '-27', '-26','-25', '-24', '-23', '-22', '-21', '-20', \
#                    '-19', '-18', '-17', '-16','-15', '-14', '-13', '-12', '-11', '-10', \
#                    '-9', '-8', '-7', '-6','-5', '-4', '-3', '-2', '-1', \
#                    '0', \
#                    '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', \
#                    '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20', \
#                    '+21', '+22', '+23', '+24', '+25', '+26', '+27', '+28', '+29', '+30', \
#                    '+31', '+32', '+33', '+34', '+35' \
#                    ]



bExposureRaw = False # True/False
nFileExposureIM = 25
nFileExposureID = 600
nFileExposureInterval = 1

nROI_X = 4000
nROI_Y = 3000
nROI_W = 4    #multiple of 4
nROI_H = 4    #multiple of 4

g_re_FilePattern = "[a-zA-Z0-9_]+(.raw)"

bSaveCSV = True
sFileTempTime = '2021113015'
sSavePath = '/home/dino/RawShared/Output/Temp/2021111810/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021112914/4000_3000/600/{}/'
#sSavePath = '/home/dino/RawShared/Output/Temp/2021113014/AngularSample/{}/'

bShowDebugOutput = False

bDeleteMaxMin = False
nDeleteMaxCount = 3
nDeleteMinCount = 3

bCalROIChannel = False
bSaveCSV_ROI = False
### Change the parameters to match the settings
#######################################################

if not bExposureRaw:
    # Normal
    sSaveTempFile = '{}_Single_{}.csv'
    sSaveOrganizeTempFile = '{}_{}.csv'
else:
    # Exposure
    sSaveTempFile = '{}_{}_{}_{}.csv'
    sSaveOrganizeTempFile = '{}_{}_{}.csv'

#PixelRow_array = np.zeros((nFileCount, nROI_W))
lCsvStdRow = []
lCsvAvgRow = []

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
TimeInfo = sFileTempTime
#print(TimeInfo)

def Check_File(sFileName, rePattern):
    if re.fullmatch(rePattern, sFileName):
        #print("Is right file..")
        return True
    #else:
    #    print("Not right file..")
    return False

def Save_CSV(FileName, RowInfo):
    if not bSaveCSV:
        return
    with open(FileName, 'a+') as f:
        # create the csv writer
        csv_writer = csv.writer(f)
        # write a row to the csv file
        #print(RowInfo)
        csv_writer.writerow(RowInfo)

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
                lCsvStdRow.append('Total_STD_{}{}'.format(sColor, j+1))
                Channel_STD = np.std(ChannelAllPixel)
                lCsvStdRow.append(Channel_STD.tolist())
                lCsvAvgRow.append('Total_AVG_{}{}'.format(sColor, j+1))
                Channel_AVG = np.average(ChannelAllPixel)
                lCsvAvgRow.append(Channel_AVG.tolist())
        #print(lCsvStdRow)
        #print(lCsvAvgRow)


def Cal_Save_AllInformation(y, nCount, ChannelArray, sColor, sSaveFileName, nExpIndex, sSaveOrgFile):
    #print(ChannelArray)
    #print('')
    lRawInfo = []
    lRawInfo.clear()
    lRawInfo = ['', 'Ch1_AVG', 'Ch1_STD', 'Ch2_AVG', 'Ch2_STD', 'Ch3_AVG', 'Ch3_STD', 'Ch4_AVG', 'Ch4_STD']
    Save_CSV(sSaveFileName, lRawInfo)
    for i in range(0, nCount+1):
        if i < nCount:
            lRawInfo.clear()
            lRawInfo.append('Frame{}'.format(i))
            for j in range(0, 4):
                #print(ChannelArray[i,j])
                ChannelAllPixel = ChannelArray[i,j].flatten()
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
            lRawOrglInfo.append('Exp{}'.format(nExpIndex))
            lRawInfo.clear()
            lRawInfo.append('FrameTotal')
            for j in range(0, 4):
                #print("({},{},{})".format(i, j, sColor))
                ChannelAllPixel = ChannelArray[:,j,:].flatten()
                if bShowDebugOutput:
                    print('OnePixel_{}{}: {}'.format(sColor, j+1, ChannelAllPixel))
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

                ##Dino test
                #if sColor == 'Gr' and j == 1:
                #    print(ChannelAllPixel)
                #    print(ChannelAllPixel.max())
                #    print(ChannelAllPixel.min())
                #    with open('/home/dino/RawShared/Output/Temp/20211124.csv', 'w+') as f:
                #        # create the csv writer
                #        csv_writer = csv.writer(f)
                #        # write a row to the csv file
                #        #print(RowInfo)
                #        csv_writer.writerow(ChannelAllPixel.tolist())
                
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

            if bCalROIChannel:
                lRawROIInfo = []
                lRawROIInfo.clear()
                lRawROIInfo.append('ROI_Exp{}'.format(nExpIndex))

                ChannelAllPixel = ChannelArray[:,:,:].flatten()
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

    #Get the numbers of every channel
    nR_Gb_Len = nROI_W//4 * nROI_H//4
    nGr_B_Len = nROI_W//4 * nROI_H//4
    #print(nR_Gb_Len)
    #print(nGr_B_Len)

    #Get the leftest pixel offset
    nWOffset = nROI_X % 4

    #Set the save orgnize file (Orgnize result)
    sTempSavePath = sSavePath.format('Total')
    if not bExposureRaw:
        sSaveOrgRFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'R')
        sSaveOrgGrFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'Gr')
        sSaveOrgGbFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'Gb')
        sSaveOrgBFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, 'B')
    else:
        sSaveOrgRFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'R')
        sSaveOrgGrFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'Gr')
        sSaveOrgGbFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'Gb')
        sSaveOrgBFile = sTempSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'B')
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
        
        #The exposure time index
        if not bExposureRaw:
            nExposureIntervalIndex = 0
        else:
            nExposureIntervalIndex = h*nFileExposureInterval+nFileExposureIM
            
        #Set the every channel saving file (R/Gr/Gb/B) (Total)
        sTempSavePath = sSavePath.format(x)
        if not bExposureRaw:
            sSaveRFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'R')
            sSaveGrFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'Gr')
            sSaveGbFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'Gb')
            sSaveBFile = sTempSavePath+sSaveTempFile.format(TimeInfo, 'B')
        else:
            sSaveRFile = sTempSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'R')
            sSaveGrFile = sTempSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gr')
            sSaveGbFile = sTempSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gb')
            sSaveBFile = sTempSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'B')
        if os.path.exists(sSaveRFile):
            os.remove(sSaveRFile)
        if os.path.exists(sSaveGrFile):
            os.remove(sSaveGrFile)
        if os.path.exists(sSaveGbFile):
            os.remove(sSaveGbFile)
        if os.path.exists(sSaveBFile):
            os.remove(sSaveBFile)

        k = 0
        for root, dirs, files in os.walk(sTempFilePath):
            for sFile in files:
                nR0Index, nR1Index, nR2Index, nR3Index = 0, 0, 0, 0
                nGr0Index, nGr1Index, nGr2Index, nGr3Index = 0, 0, 0, 0
                nGb0Index, nGb1Index, nGb2Index, nGb3Index = 0, 0, 0, 0
                nB0Index, nB1Index, nB2Index, nB3Index = 0, 0, 0, 0

                sFileTemp = sFile
                rePattern = g_re_FilePattern
                if not Check_File(sFileTemp, rePattern):
                    continue

                sFileTemp = root + '/' + sFileTemp
                print('sFileTemp: ', sFileTemp)
                #Every row
                for i in range(nROI_Y, nROI_Y+nROI_H):
                    bNeedCal = False

                    nPixelOffset = nWidth * i * 2 + nROI_X * 2
                    #print('nPixelOffset: ', nPixelOffset)
                    input_file = open(sFileTemp, 'rb')
                    #Get all pixel of one range row
                    input_array = np.fromfile(input_file, dtype=np.uint16, count=nROI_W, sep="", offset=nPixelOffset)
                    input_file.close()
                    #print('input_array: ', input_array)
                    
                    if i%4==0:  #R1~2+Gr1~2
                        for l in range(0, nROI_W):
                            if (l+nWOffset)%4==0: #R1
                                #print('h:{}, i:{}, k:{}, Index:{}, l:{}'.format(h, i, k, nR0Index, l))
                                ChannelR_array[k,0,nR0Index] = input_array[l]
                                nR0Index += 1
                            elif (l+nWOffset)%4==1: #R2
                                ChannelR_array[k,1,nR1Index] = input_array[l]
                                nR1Index += 1
                            elif (l+nWOffset)%4==2: #Gr1
                                #if nGr0Index == 0:
                                #    print('{}: {}'.format(k, input_array[l]))
                                ChannelGr_array[k,0,nGr0Index] = input_array[l]
                                nGr0Index += 1
                            elif (l+nWOffset)%4==3: #Gr2
                                ChannelGr_array[k,1,nGr1Index] = input_array[l]
                                nGr1Index += 1
                    elif i%4==1:  #R3~4+Gr3~4
                        for l in range(0, nROI_W):
                            if (l+nWOffset)%4==0: #R3
                                ChannelR_array[k,2,nR2Index] = input_array[l]
                                nR2Index += 1
                            elif (l+nWOffset)%4==1: #R4
                                ChannelR_array[k,3,nR3Index] = input_array[l]
                                nR3Index += 1
                            elif (l+nWOffset)%4==2: #Gr3
                                ChannelGr_array[k,2,nGr2Index] = input_array[l]
                                nGr2Index += 1
                            elif (l+nWOffset)%4==3: #Gr4
                                ChannelGr_array[k,3,nGr3Index] = input_array[l]
                                nGr3Index += 1
                    elif i%4==2:  #Gb1~2+B1~2
                        for l in range(0, nROI_W):
                            if (l+nWOffset)%4==0: #Gb1
                                ChannelGb_array[k,0,nGb0Index] = input_array[l]
                                nGb0Index += 1
                            elif (l+nWOffset)%4==1: #Gb2
                                ChannelGb_array[k,1,nGb1Index] = input_array[l]
                                nGb1Index += 1
                            elif (l+nWOffset)%4==2: #B1
                                ChannelB_array[k,0,nB0Index] = input_array[l]
                                nB0Index += 1
                            elif (l+nWOffset)%4==3: #B2
                                ChannelB_array[k,1,nB1Index] = input_array[l]
                                nB1Index += 1
                    elif i%4==3:  #Gb3~4+B3~4
                        for l in range(0, nROI_W):
                            if (l+nWOffset)%4==0: #Gb3
                                ChannelGb_array[k,2,nGb2Index] = input_array[l]
                                nGb2Index += 1
                            elif (l+nWOffset)%4==1: #Gb4
                                ChannelGb_array[k,3,nGb3Index] = input_array[l]
                                nGb3Index += 1
                            elif (l+nWOffset)%4==2: #B3
                                ChannelB_array[k,2,nB2Index] = input_array[l]
                                nB2Index += 1
                            elif (l+nWOffset)%4==3: #B4
                                ChannelB_array[k,3,nB3Index] = input_array[l]
                                nB3Index += 1
                k = k + 1

        #Save the R information
        #print(h)
        #lCsvStdRow.clear()
        #lCsvAvgRow.clear()
        #Save_CSV(sSaveRStdFile, lCsvStdRow)
        #Save_CSV(sSaveRAvgFile, lCsvAvgRow)
        Cal_Save_AllInformation(h, nCount, ChannelR_array, 'R', sSaveRFile, nExposureIntervalIndex, sSaveOrgRFile)
        #Save the G information
        #lCsvStdRow.clear()
        #lCsvAvgRow.clear()
        #Save_CSV(sSaveGrStdFile, lCsvStdRow)
        #Save_CSV(sSaveGrAvgFile, lCsvAvgRow)
        Cal_Save_AllInformation(h, nCount, ChannelGr_array, 'Gr', sSaveGrFile, nExposureIntervalIndex, sSaveOrgGrFile)
        #Save the Gb information
        #lCsvStdRow.clear()
        #lCsvAvgRow.clear()
        #Save_CSV(sSaveGbStdFile, lCsvStdRow)
        #Save_CSV(sSaveGbAvgFile, lCsvAvgRow)
        Cal_Save_AllInformation(h, nCount, ChannelGb_array, 'Gb', sSaveGbFile, nExposureIntervalIndex, sSaveOrgGbFile)
        #Save the B information
        #lCsvStdRow.clear()
        #lCsvAvgRow.clear()
        #Save_CSV(sSaveBStdFile, lCsvStdRow)
        #Save_CSV(sSaveBAvgFile, lCsvAvgRow)
        Cal_Save_AllInformation(h, nCount, ChannelB_array, 'B', sSaveBFile, nExposureIntervalIndex, sSaveOrgBFile)

        h = h + 1
        nEachIntervalTime = time.time()
        print("Durning Each Interval:{} Time(sec): {}".format(h, nEachIntervalTime - StartTime))

if __name__ == "__main__":
    ParsingPixel()


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)