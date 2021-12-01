#######################################################
### One pixel std and avg.
### Save one pixel to one total csv

#import numpy as np
import time
import csv
import enum
import os
import re

StartTime = time.time()

class PixelSelect(enum.IntEnum):
    AllPixel = 0
    OnlyRPixel = 1
    OnlyGrPixel = 2
    OnlyGbPixel = 3
    OnlyBPixel = 4

#######################################################
### Change the parameters to match the settings
g_sFilePath = '/home/dino/RawShared/Output/2021113014/AngularSample/'
g_sFilePathFolder = [
                    '-35', '-34', '-33', '-32', '-31', '-30', \
                    '-29', '-28', '-27', '-26','-25', '-24', '-23', '-22', '-21', '-20', \
                    '-19', '-18', '-17', '-16','-15', '-14', '-13', '-12', '-11', '-10', \
                    '-9', '-8', '-7', '-6','-5', '-4', '-3', '-2', '-1', \
                    '0', \
                    '+1', '+2', '+3', '+4', '+5', '+6', '+7', '+8', '+9', '+10', \
                    '+11', '+12', '+13', '+14', '+15', '+16', '+17', '+18', '+19', '+20', \
                    '+21', '+22', '+23', '+24', '+25', '+26', '+27', '+28', '+29', '+30', \
                    '+31', '+32', '+33', '+34', '+35' \
                    ]

g_nPixelSelect = PixelSelect.OnlyGrPixel
g_re_FilePattern = r"[0-9]+(_)+(Gr)+(.csv)"

g_nGetCSVColumn_NO = 1     # -1:get all, 0:No.0 Column, ...

#g_sSavePath = '/home/dino/RawShared/Output/2021113014/AngularSample/'
g_sSavePath = '/home/dino/RawShared/Output/2021113014/AngularSample/TempMerge.csv'
### Change the parameters to match the settings
#######################################################

g_lCsvRow = []

def Check_File(sFileName):
    if re.fullmatch(g_re_FilePattern, sFileName):
        #print("Is right file..")
        return True
    #else:
    #    print("Not right file..")
    return False

def Get_Info(sFileName):
    i = 0
    with open(sFileName, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            #print(i, ':', row)
            if g_nGetCSVColumn_NO == -1:
                g_lCsvRow.append(row)
            elif g_nGetCSVColumn_NO == i:
                g_lCsvRow.append(row)
            i = i + 1
        #print(g_lCsvRow)
        #print(g_lCsvRow[0])
        #print(g_lCsvRow[0][1])
    return

def Save_CSV(sFileName, RowInfo):
    with open(sFileName, 'a+') as f:
        # create the csv writer
        csv_writer = csv.writer(f)
        # write a row to the csv file
        #print(RowInfo)
        csv_writer.writerow(RowInfo)

def CombineCSV():
    sTempSavePath = g_sSavePath
    if os.path.exists(sTempSavePath):
        os.remove(sTempSavePath)

    for i in g_sFilePathFolder:
        sTempFilePath = g_sFilePath + i
        
        for root, dirs, files in os.walk(sTempFilePath):
            #print("Path:", root)
            #print("Folder:", dirs)
            #print("File Count:", len(files))
            #print("File:", files)
            for sFile in files:
                if Check_File(sFile):
                    #print("i:", i)
                    #print("File:", sFile)
                    sTempFile = root + '/' + sFile
                    #print("File:", sTempFile)
                    g_lCsvRow.clear()
                    Get_Info(sTempFile)
                    if len(g_lCsvRow) > 0:
                        for row in g_lCsvRow:
                            Save_CSV(sTempSavePath, row)
                        pass
                    pass

if __name__ == "__main__":
    CombineCSV()

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)