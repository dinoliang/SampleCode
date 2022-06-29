#######################################################
### Calculate the information by pixel csv file (not origin bin file (raw image))

import numpy as np
from matplotlib import pyplot as plt
import time
import csv
import datetime
#import enum
import os
import re
from enum import Enum

StartTime = time.time()

#######################################################
### Change the parameters to match the settings

g_sFilePath = '/home/dino/RawShared/Other/'
g_sCsvFile = 'Config_csv_Def-220125_reg_Default_csv.csv'
g_sOutFile = 'Config_csv_Def-220125_reg_Default_csv.out'

gbDoneIdentify = True

#Debug or not
bShowDebugOutput = True

### Change the parameters to match the settings
#######################################################

g_TotalLines = 0

NowDate = datetime.datetime.now()
#TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
#print(TimeInfo)

def SaveArrayToCSV(SaveArray, strFileName, fmtType, delimiterType):
    sFile = '{}{}'.format(g_sFilePath, strFileName)
    np.savetxt(sFile, SaveArray, fmt = fmtType, delimiter = delimiterType)

def LoadFileFromCSV(strFileName):
    sFile = '{}{}'.format(g_sFilePath, strFileName)
    sLoadArray = np.loadtxt(sFile, delimiter=',')
    print('Load File:{}, Array:{} Shape:{}'.format(sFile, sLoadArray, sLoadArray.shape))
    return sLoadArray

def LoadFileFromCSV2(strFileName):
    sFile = '{}{}'.format(g_sFilePath, strFileName)
    fr = open(sFile, 'r')
    lines = fr.readlines()
    global g_TotalLines
    if not gbDoneIdentify:
        g_TotalLines = len(lines)
        sLoadArray = np.zeros((g_TotalLines, 3, 8))
        TempArray = np.zeros((g_TotalLines, 3))
    else:
        g_TotalLines = len(lines) - 1
        sLoadArray = np.zeros((g_TotalLines, 3, 8))
        TempArray = np.zeros((g_TotalLines, 3))

    Idx = 0
    for L in lines:
        string = L.strip("\n").split(",")
        #print(string)

        if np.size(string) == 6:
            #a = string[0]
            #b = np.int64(int(string[1], 16))
            #c = string[2]
            #d = np.int64(int(string[3], 16))
            #e = string[4]
            #f = np.int64(int(string[5], 16))
            #str = '%s,%u,%s,%u,%s,%u' % (a,b,c,d,e,f)
            #print(str)

            TempArray[Idx,0] = np.int64(int(string[1], 16)) * 2
            TempArray[Idx,1] = np.int64(int(string[3], 16))
            if string[5] == "0xXX" or string[5] == "0xxx":
                TempArray[Idx,2] = 255
                TempArray[Idx,0] = TempArray[Idx,0] + 1 #Read
            else:
                TempArray[Idx,2] = np.int64(int(string[5], 16))
            #print(TempArray[Idx,:])

            for i in range(0,3):
                for j in range(7,-1,-1):
                    #print("Idx=%d,i=%d,j=%d", Idx, i, j)
                    nBit = TempArray[Idx,i] % 2
                    #print(nBit)
                    TempArray[Idx,i] = TempArray[Idx,i] // 2
                    sLoadArray[Idx,i,j] = nBit
                #print(sLoadArray[Idx,i,:])

            Idx = Idx + 1

    fr.close()
    #print(sLoadArray)
    return sLoadArray

def ConvertToVectorOut(LoadArray, strWriteFileName):
    #print("g_TotalLines={}".format(g_TotalLines))
    sWriteFile = '{}{}'.format(g_sFilePath, strWriteFileName)
    strOut = ""
    with open(sWriteFile, 'w') as f:
        f.write(strOut)
    for Idx in range(0, g_TotalLines):
        #I2C start: "10"
        bRead = False
        strOut = "\"10\"\n"
        for i in range(0,3): #i==0:Slave, i==1:Address, i==2:Data
            if i == 0 and LoadArray[Idx,i,7] == 1:
                bRead = True

            for j in range(0,8): #bit[0]:highest bit
                #print("Idx={},i={},j={}".format(Idx, i, j))
                if j < 7:
                    if bRead and i == 2: # If read, the data always 0X1X0X (1~7th bit)
                        strOut = strOut + "\"0X\"\n\"1X\"\n\"0X\"\n"
                    else:
                        strBit = '\"0{:d}\"\n\"1{:d}\"\n\"0{:d}\"\n'
                        strOut = strOut + strBit.format(np.int64(LoadArray[Idx,i,j]),np.int64(LoadArray[Idx,i,j]),np.int64(LoadArray[Idx,i,j]))
                elif j == 7:
                    if bRead and i == 2: # If read, the data always 0X1X (highest bit)
                        strOut = strOut + "\"0X\"\n\"1X\"\n"
                    else:
                        strBit = '\"0{:d}\"\n\"1{:d}\"\n'
                        strOut = strOut + strBit.format(np.int64(LoadArray[Idx,i,j]),np.int64(LoadArray[Idx,i,j]))
                    
                #print(strOut)

            if Idx < g_TotalLines - 2:
                strOut = strOut + "\"0X\"\n\"0X\"\n\"1X\"\n\"1X\"\n\"0X\"\n\"01\"\n" #ACK + End of ACK
            else: # The end of last line is 00
                strOut = strOut + "\"0X\"\n\"0X\"\n\"1X\"\n\"1X\"\n\"0X\"\n\"00\"\n" #ACK + Stop
        #print(strOut)
        with open(sWriteFile, 'a') as f:
            f.write(strOut)
    strOut = "\"10\"\n\"11\"" # Finish
    #print(strOut)
    with open(sWriteFile, 'a') as f:
        f.write(strOut)
    pass

if __name__ == "__main__":
    LoadArray = LoadFileFromCSV2(g_sCsvFile)
    ConvertToVectorOut(LoadArray, g_sOutFile)
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
