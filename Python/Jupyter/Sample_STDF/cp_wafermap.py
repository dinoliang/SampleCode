import time
import os
import datetime
import sys

import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import csvhandle
StartTime = time.time()

#######################################################
### Change the parameters to match the settings
gResultFolder = 'I:\\Work\\Zettmage\\Data\\Work\\ZP6024\\CP\\Chroma\\STDFSample\\CPResult_P8P125.00(#6_#9)_20221020\\P8P125.00(#6_#9)\\WaferMap\\'
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
        # 1. Get the width & height of WaferMap 2. Combine all stdf
        Result_Array = None
        nWaferWidth = -1
        nWaferHeight = -1
        nUsedFileCount = 0
        for root, dirs, files in os.walk(resultFolder):
            for sFile in files:
                if '.csv' not in sFile:
                    continue
                if 'Result' in sFile or 'Out' in sFile or 'Output' in sFile:
                    continue
                filepathe = os.path.join(resultFolder, sFile)
                print('Wafer map csv:{}'.format(filepathe))

                OneWafer_Array = None
                with open(filepathe, newline='', encoding="utf-8") as csvfile:
                    # Read CSV Content
                    rows = csv.reader(csvfile)

                    nArrayWidth = 0
                    nArrayHeight = 0
                    for row in rows:
                        nArrayHeight = nArrayHeight + 1
                        if len(row) > nArrayWidth:
                            nArrayWidth = len(row)

                    OneWafer_Array = np.empty([nArrayHeight, nArrayWidth], dtype=object)

                    # Get every row
                    csvfile.seek(0)
                    RowIdx = 0
                    for row in rows:
                        #OneRaw = np.empty([1, len(row)], dtype=object)
                        line_array = np.array(row)
                        #print('line_array:{}, shape:{}'.format(line_array, line_array.shape))
                        OneWafer_Array[RowIdx, 0:line_array.shape[0]] = line_array[:]
                        RowIdx = RowIdx + 1
                #print('OneWafer_Array:{}'.format(OneWafer_Array))
                print('OneWafer_Array shape:{}'.format(OneWafer_Array.shape))

                if nWaferWidth == -1 or nWaferHeight == -1:
                    nWaferWidth = OneWafer_Array.shape[1] - 2
                    nWaferHeight = -1
                    nWaferHeightBegin = -1
                    nWaferHeightEnd = -1
                    for i in range(OneWafer_Array.shape[0]):
                        #print('OneWafer_Array[{}, 0]:{}'.format(i, OneWafer_Array[i, 0]))
                        if str(OneWafer_Array[i, 1]) == '0' and str(OneWafer_Array[i, 2]) == '1' and str(OneWafer_Array[i, 3]) == '2' and nWaferHeightBegin == -1:
                            nWaferHeightBegin = i
                        elif str(OneWafer_Array[i, 1]) == '0' and str(OneWafer_Array[i, 2]) == '1' and str(OneWafer_Array[i, 3]) == '2':
                            nWaferHeightEnd = i
                    nWaferHeight = nWaferHeightEnd - nWaferHeightBegin - 1
                print('Wafer width:{}, height:{}'.format(nWaferWidth, nWaferHeight))

                if nWaferWidth <= 0 or nWaferHeight <= 0:
                    continue
                nUsedFileCount = nUsedFileCount + 1

                X = (OneWafer_Array.shape[1] - nWaferWidth - 1)
                Y = (OneWafer_Array.shape[0] - nWaferHeight - 2)
                #print('Wafer X:{}, Y:{}'.format(X, Y))
                #print('WaferMap:{}'.format(OneWafer_Array[Y:Y+nWaferHeight, X:X+nWaferWidth]))
                #print('WaferMap[1,11]:{}'.format(OneWafer_Array[Y+1, X+11]))
                #print('WaferMap[16,:]:{}'.format(OneWafer_Array[Y+16, X:X+nWaferWidth]))
                #print('WaferMap[17,:]:{}'.format(OneWafer_Array[Y+17, X:X+nWaferWidth]))
                #print('WaferMap[18,:]:{}'.format(OneWafer_Array[Y+18, X:X+nWaferWidth]))

                if nWaferWidth > 0 and nWaferHeight > 0 and Result_Array is None:
                    #Result_Array = np.zeros([nWaferHeight, nWaferWidth])
                    Result_Array = np.ndarray((nWaferHeight, nWaferWidth))
                    Result_Array.fill(-1)

                for j in range(nWaferHeight):
                    for i in range(nWaferWidth):
                        #print('OneWafer_Array[{}, {}]:{}'.format(Y+j, X+i, OneWafer_Array[Y+j, X+i]))
                        #if str(OneWafer_Array[Y+j, X+i]) == 'X':
                        #    Result_Array[j, i] = Result_Array[j, i] + 1
                        #    #print('Result_Array[{}, {}]:{}'.format(j, i, Result_Array[j, i]))
                        try:
                            #print('Result_Array[{}, {}]:{}, csvMatrix[{}, {}]:{}'.format(i, j, Result_Array[i, j], i+1, j+1, csvMatrix[i+1, j+1]))
                            nResultNum = np.int64(Result_Array[j, i])
                            strWafer = str(OneWafer_Array[Y+j, X+i])
                            #print('nResultNum:{}, nNum:{}'.format(nResultNum, nNum))
                            if nResultNum == -1 and strWafer == 'O': #Pass
                                Result_Array[j, i] = 0
                            #elif nResultNum != -1 and strWafer != 'X': #Pass again
                            #    pass
                            elif nResultNum == -1 and strWafer == 'X': #Fail
                                Result_Array[j, i] = 1
                            elif nResultNum != -1 and strWafer == 'X': #Fail again
                                Result_Array[j, i] = nResultNum + 1
                        except:
                            pass
                        finally:
                            pass

        #print('Result_Array:{}'.format(Result_Array))
        #print('Result_Array[16,:]:{}'.format(Result_Array[16, :]))

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

        print('Combine finish!!')
        if self.callback_Func is not None and self.callback_Caller is not None:
            self.callback_Func(self.callback_Caller, 'Combine finish!!')

        # heat map 1
        #plt.imshow(Result_Array, cmap='h', interpolation='nearest')
        #plt.show()
        # heat map 2
        #  cmap='YlOrBr', cmap='YlGnBu', cmap = 'coolwarm'
        ax = sns.heatmap(Result_Array, cmap='YlOrBr', linewidth=float(nUsedFileCount/4))
        plt.show()

        return

    def StartTest(self):
        self.StartCombine(gResultFolder, gResultOutFile)
        return

if __name__ == "__main__":
    result = ResultHandler()
    result.StartCombine(gResultFolder, gResultOutFile)
    pass

EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
