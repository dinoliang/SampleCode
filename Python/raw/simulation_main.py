import array as arr
import numpy as np
import time
import csv
import scipy.misc
import matplotlib.pyplot as plt
import channelrowparse_maxmin as testmain
import channelrowparse_zett as zettmain

StartTime = time.time()

def UseCallPy():
    '''
    testmain.nROI_X = 3998
    testmain.nROI_Y = 2998
    '''

    sFilePathFolder = [
                        '0x1010', '0x1020', '0x1030', '0x1040', '0x1050', '0x1060', '0x1070', '0x1080', '0x1090', '0x10A0', '0x10B0', '0x10C0', \
                      ]

    '''
    testmain.CallMain(  nWidth=8000, \
                        nHeight=6000, \
                        nX=3998, \
                        nY=2998, \
                        nROI_W=4, \
                        nROI_H=4, \
                        nFileCounts=10, \
                        FileTimeStamp='20211111160205', \
                        InputFolder='/home/dino/RawShared/20211111_fulldark/', \
                        ArrayFolder=sFilePathFolder, \
                        OutputFolder='/home/dino/RawShared/Output/')
    print(testmain.g_sFilePathFolder)
    '''

    zettmain.CallMain(  nWidth=9728, \
                        nHeight=8192, \
                        nX=4766, \
                        nY=3996, \
                        nROI_W=16, \
                        nROI_H=16, \
                        nColIndex=0, \
                        nRowIndex=2, \
                        nFileCounts=2, \
                        FileTimeStamp='2022051810', \
                        InputFolder='/home/dino/IMX586_Bin/2022051810_P8N533#2#1843_Lag/{}/', \
                        OutputFolder='/home/dino/RawShared/Output/2022051810_P8N533#2#1843_Lag/{}/', \
                        ArrayFolder=sFilePathFolder)
    print(zettmain.g_sFilePathFolder)

    return

if __name__ == "__main__":
    UseCallPy()

    pass


EndTime = time.time()
print("Simulation Durning Time(sec): ", EndTime - StartTime)