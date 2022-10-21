import time
import os
import datetime
import sys

import numpy as np
import pandas as pd

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
gResultFolder = 'I:\\Work\\Zettmage\\Data\\Work\\ZP6024\\CP\\Chroma\\STDFSample\\CPResult_P8P125.00(#6_#9)_20221020\\P8P125.00(#6_#9)\\P8P125.00#06\\P8P125.00_P8P125.00-6_20221019_184807_stdf\\'
gResultOutFile = 'Out.csv'

#######################################################

class ResultHandler:
    callback_Caller = None
    callback_Func = None
    
    def __init__(self) -> None:
        pass

    def SetCallback(self, cCaller, cFunc):
        self.callback_Caller = cCaller
        self.callback_Func = cFunc
        return

    def StartCombine(self, resultFolder, resultOutFile):
        # Get the width & height of WaferMap
        nWaferWidth = -1
        nWaferHeight = -1
        for root, dirs, files in os.walk(resultFolder):
            for sFile in files:
                if '.csv' not in sFile:
                    continue
                if 'Result' in sFile or 'Out' in sFile or 'Output' in sFile:
                    continue
                filepathe = os.path.join(resultFolder, sFile)

                df = pd.read_csv('data.csv')
                for i in range(df.shape[0]):
                    if df[i, 0] == 'Wafer maxinum X':
                        nWaferWidth = np.int64(df[i, 1])
                    if df[i, 0] == 'Wafer maxinum Y':
                        nWaferHeight = np.int64(df[i, 1])
                print('Wafer width:{}, height:{}'.format(nWaferWidth, nWaferHeight))
                #csvRows = csvfile.ReadCSVToNumpy2(filepathe, 3)
                break
            break

        if nWaferWidth <= 0 or nWaferHeight <= 0:
            return

        # ChannelR_array = np.zeros((len(files), 4, nR_Gb_Len)) or ndarray = numpy.ndarray((20, 21))
        # .fill
        Result_Array = np.ndarray((nWaferHeight, nWaferWidth))
        Result_Array.fill(-1)
        #print('Result_Array:{}, Shape:{}'.format(Result_Array, Result_Array.shape))

        # Combine all stdf
        for root, dirs, files in os.walk(resultFolder):
            for sFile in files:
                if '.csv' not in sFile:
                    continue
                if 'Result' in sFile or 'Out' in sFile:
                    continue
                #print(sFile)
                filepathe = os.path.join(resultFolder, sFile)
                csvfile = csvhandle.csvhandle()
                csvRows = csvfile.ReadCSV(filepathe, 3)
                csvMatrix = np.array(csvRows)
                #print('csvMatrix:{}, Shape:{}'.format(csvMatrix, csvMatrix.shape))

                for i in range(0, nWaferHeight):
                    for j in range(0, nWaferWidth): 
                        try:
                            #print('Result_Array[{}, {}]:{}, csvMatrix[{}, {}]:{}'.format(i, j, Result_Array[i, j], i+1, j+1, csvMatrix[i+1, j+1]))
                            nResultNum = np.int64(Result_Array[i, j])
                            nNum = np.int64(csvMatrix[i+1, j+1])
                            #print('nResultNum:{}, nNum:{}'.format(nResultNum, nNum))
                            if nResultNum == -1 and nNum == 1: #Pass
                                Result_Array[i, j] = 0
                            #elif nResultNum != -1 and nNum == 1: #Pass again
                            #    pass
                            elif nResultNum == -1 and nNum != 1: #Fail
                                Result_Array[i, j] = 1
                            elif nResultNum != -1 and nNum != 1: #Fail again
                                Result_Array[i, j] = nResultNum + 1
                        except:
                            pass
                        finally:
                            pass

        #print(Result_Array[45, 29])      
        #print('Result_Array:{}, Shape:{}'.format(Result_Array, Result_Array.shape))

        '''
        # Output to CSV
        NowDate = datetime.datetime.now()
        TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)
        if resultOutFile == '':
            OutFilename = 'Result_{}.csv'.format(TimeInfo)
        else:
            OutFilename = resultOutFile
        outFile = os.path.join(resultFolder, OutFilename)
        csvfile = csvhandle.csvhandle()
        csvfile.WriteCSVToNumpy(outFile, Result_Array)
        '''

        print('Combine finish!!')
        if self.callback_Func is not None and self.callback_Caller is not None:
            self.callback_Func(self.callback_Caller, 'Combine finish!!')
        return

if __name__ == "__main__":
    result = ResultHandler()
    result.StartCombine(gResultFolder, gResultOutFile)
    pass

EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
