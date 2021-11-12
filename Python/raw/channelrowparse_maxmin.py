#######################################################
### Get one row data to calculate.
### Calculate block(R1~4/Gr1~4/Gb1~4/B1~4) std and avg.

import numpy as np
import time
import csv
import datetime
import enum
import os

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
nWidth = 8000
nHeight = 6000

nFileCount = 100
sFilePath = '/home/dino/RawShared/20211111_fulldark/'
sFileTempTime = '20211111160205'
sFileTempFormat = 'P10'

bExposureRaw = False # True/False
nFileExposureIM = 1
nFileExposureID = 30
nFileExposureCount = 10
nFileExposureInterval = 1
nFileExposureIntervalNum = 1

nROI_X = 1444#3998
nROI_Y = 337#2998
nROI_W = 4    #multiple of 4
nROI_H = 4    #multiple of 4

sSavePath = '/home/dino/RawShared/Output/'

### Change the parameters to match the settings
#######################################################

if not bExposureRaw:
    # Normal
    sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}.raw'
    sSaveStdFile = 'STD_{}.csv'
    sSaveAvgFile = 'AVG_{}.csv'
    nFileExposureIntervalNum = 1
else:
    # Exposure
    sFileTempName = 'FrameID0_W{0:d}_H{1:d}_{2:s}_{3:s}_{4:04d}_{5:d}_{6:d}.raw'
    sSaveStdFile = 'STD_{}_{}_{}_{}.csv'
    sSaveAvgFile = 'AVG_{}_{}_{}_{}.csv'

sSaveTempFile = '{}_{}_{}_{}.csv' 
sSaveOrganizeTempFile = '{}_{}_{}.csv'

#PixelRow_array = np.zeros((nFileCount, nROI_W))
lCsvStdRow = []
lCsvAvgRow = []

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
TimeInfo = sFileTempTime
#print(TimeInfo)

def Save_CSV(FileName, RowInfo):
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
                Channel_AVG = np.average(ChannelArray[i,j])
                lRawInfo.append(Channel_AVG.tolist())
                Channel_STD = np.std(ChannelArray[i,j])
                lRawInfo.append(Channel_STD.tolist())
            Save_CSV(sSaveFileName, lRawInfo)
        elif i == nCount: # Total
            lRawMin = []
            lRawMin.clear()
            lRawMin.append('Min:')
            lRawMax = []
            lRawMax.clear()
            lRawMax.append('Max:')
            lRawOrglInfo = []
            lRawOrglInfo.clear()
            lRawOrglInfo.append('Exp{}'.format(nExpIndex))
            lRawInfo.clear()
            lRawInfo.append('FrameTotal')
            for j in range(0, 4):
                ChannelAllPixel = ChannelArray[:,j,:].flatten()
                #print(ChannelAllPixel)
                #print('Min: ', np.min(ChannelAllPixel))
                #print('Max: ', np.max(ChannelAllPixel))
                lRawMin.append(np.min(ChannelAllPixel))
                lRawMin.append('')
                lRawMax.append(np.max(ChannelAllPixel))
                lRawMax.append('')
                Channel_AVG = np.average(ChannelAllPixel)
                lRawOrglInfo.append(Channel_AVG.tolist())
                lRawInfo.append(Channel_AVG.tolist())
                Channel_STD = np.std(ChannelAllPixel)
                lRawOrglInfo.append(Channel_STD.tolist())
                lRawInfo.append(Channel_STD.tolist())
            Save_CSV(sSaveFileName, lRawInfo)
            Save_CSV(sSaveFileName, lRawMin)
            Save_CSV(sSaveFileName, lRawMax)
            Save_CSV(sSaveOrgFile, lRawOrglInfo)


def ParsingPixel():
    nCount = nFileCount
    if bExposureRaw:
        nCount = nFileExposureCount

    nR_Gb_Len = nROI_W//4 * nROI_H//4
    nGr_B_Len = nROI_W//4 * nROI_H//4
    #print(nR_Gb_Len)
    #print(nGr_B_Len)

    nWOffset = nROI_X % 4

    sSaveOrgRFile = sSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'R')
    sSaveOrgGrFile = sSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'Gr')
    sSaveOrgGbFile = sSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'Gb')
    sSaveOrgBFile = sSavePath+sSaveOrganizeTempFile.format(TimeInfo, nFileExposureID, 'B')
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
        
    for h in range(0, nFileExposureIntervalNum):
        bR_Gr = False
        bGb_B = False

        ChannelR_array = np.zeros((nCount, 4, nR_Gb_Len))
        ChannelGr_array = np.zeros((nCount, 4, nGr_B_Len))
        ChannelGb_array = np.zeros((nCount, 4, nR_Gb_Len))
        ChannelB_array = np.zeros((nCount, 4, nGr_B_Len))
        
        nExposureIntervalIndex = h*nFileExposureInterval+nFileExposureIM
        sSaveRStdFile = sSavePath+sSaveStdFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'R')
        sSaveRAvgFile = sSavePath+sSaveAvgFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'R')
        sSaveGrStdFile = sSavePath+sSaveStdFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gr')
        sSaveGrAvgFile = sSavePath+sSaveAvgFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gr')
        sSaveGbStdFile = sSavePath+sSaveStdFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gb')
        sSaveGbAvgFile = sSavePath+sSaveAvgFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gb')
        sSaveBStdFile = sSavePath+sSaveStdFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'B')
        sSaveBAvgFile = sSavePath+sSaveAvgFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'B')
        if os.path.exists(sSaveRStdFile):
            os.remove(sSaveRStdFile)
        if os.path.exists(sSaveRAvgFile):
            os.remove(sSaveRAvgFile)
        if os.path.exists(sSaveGrStdFile):
            os.remove(sSaveGrStdFile)
        if os.path.exists(sSaveGrAvgFile):
            os.remove(sSaveGrAvgFile)
        if os.path.exists(sSaveGbStdFile):
            os.remove(sSaveGbStdFile)
        if os.path.exists(sSaveGbAvgFile):
            os.remove(sSaveGbAvgFile)
        if os.path.exists(sSaveBStdFile):
            os.remove(sSaveBStdFile)
        if os.path.exists(sSaveBAvgFile):
            os.remove(sSaveBAvgFile)
            
        sSaveRFile = sSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'R')
        sSaveGrFile = sSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gr')
        sSaveGbFile = sSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'Gb')
        sSaveBFile = sSavePath+sSaveTempFile.format(TimeInfo, nExposureIntervalIndex, nFileExposureID, 'B')
        if os.path.exists(sSaveRFile):
            os.remove(sSaveRFile)
        if os.path.exists(sSaveGrFile):
            os.remove(sSaveGrFile)
        if os.path.exists(sSaveGbFile):
            os.remove(sSaveGbFile)
        if os.path.exists(sSaveBFile):
            os.remove(sSaveBFile)

        for k in range(0, nCount):
            nR0Index, nR1Index, nR2Index, nR3Index = 0, 0, 0, 0
            nGr0Index, nGr1Index, nGr2Index, nGr3Index = 0, 0, 0, 0
            nGb0Index, nGb1Index, nGb2Index, nGb3Index = 0, 0, 0, 0
            nB0Index, nB1Index, nB2Index, nB3Index = 0, 0, 0, 0
            if not bExposureRaw:
                sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, k)
            else:
                nContinueFileIndex = k+((h+nFileExposureIM-1)*nFileExposureCount)
                sFileTemp = sFilePath+sFileTempName.format(nWidth, nHeight, sFileTempTime, sFileTempFormat, nContinueFileIndex, nExposureIntervalIndex, nFileExposureID)
            #if k == 0:
            #    print('File: ' + sFileTemp)

            #input_file = open(sFileTemp, 'rb')
            #input_array = np.fromfile(input_file, dtype=np.uint16, count=-1, sep="", offset=0)
            #input_array = input_array.reshape((nHeight, nWidth))
            #print('Frame{} Index:{} Max: {}'.format(k, np.argmax(input_array), np.max(input_array)))
            #print('Frame{} Index:{} Min: {}'.format(k, np.argmin(input_array), np.min(input_array)))
            #arr_condition = np.where(input_array > 70)
            #print('Frame{} Size:{} >70: {}'.format(k, np.size(arr_condition), arr_condition))
            #input_file.close()

            for i in range(nROI_Y, nROI_Y+nROI_H):
                bNeedCal = False

                nPixelOffset = nWidth * i * 2 + nROI_X * 2
                #print('nPixelOffset: ', nPixelOffset)
                input_file = open(sFileTemp, 'rb')
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
                            ChannelGr_array[k,0,nGr0Index] = input_array[l]
                            nGr0Index += 1
                        elif (l+nWOffset)%4==3: #Gr2
                            ChannelGr_array[k,1,nGr1Index] = input_array[l]
                            nGr1Index += 1
                    bR_Gr = True
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
                    bR_Gr = True
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
                    bGb_B = True
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
                    bGb_B = True

        if bR_Gr:
            #print(h)
            #lCsvStdRow.clear()
            #lCsvAvgRow.clear()
            Cal_Save_AllInformation(i, nCount, ChannelR_array, 'R', sSaveRFile, nExposureIntervalIndex, sSaveOrgRFile)
            #Save_CSV(sSaveRStdFile, lCsvStdRow)
            #Save_CSV(sSaveRAvgFile, lCsvAvgRow)

            #lCsvStdRow.clear()
            #lCsvAvgRow.clear()
            Cal_Save_AllInformation(i, nCount, ChannelGr_array, 'Gr', sSaveGrFile, nExposureIntervalIndex, sSaveOrgGrFile)
            #Save_CSV(sSaveGrStdFile, lCsvStdRow)
            #Save_CSV(sSaveGrAvgFile, lCsvAvgRow)
        if bGb_B:
            #lCsvStdRow.clear()
            #lCsvAvgRow.clear()
            Cal_Save_AllInformation(i, nCount, ChannelGb_array, 'Gb', sSaveGbFile, nExposureIntervalIndex, sSaveOrgGbFile)
            #Save_CSV(sSaveGbStdFile, lCsvStdRow)
            #Save_CSV(sSaveGbAvgFile, lCsvAvgRow)

            #lCsvStdRow.clear()
            #lCsvAvgRow.clear()
            Cal_Save_AllInformation(i, nCount, ChannelB_array, 'B', sSaveBFile, nExposureIntervalIndex, sSaveOrgBFile)
            #Save_CSV(sSaveBStdFile, lCsvStdRow)
            #Save_CSV(sSaveBAvgFile, lCsvAvgRow)

        nEachIntervalTime = time.time()
        print("Durning Each Interval Time(sec): {}".format(nEachIntervalTime - StartTime))
  

if __name__ == "__main__":
    ParsingPixel()


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)