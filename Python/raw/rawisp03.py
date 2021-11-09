import numpy as np
import time
import csv
import datetime
import enum
import os

from PIL import Image
#from skimage import io
from matplotlib import pyplot as plt

import cv2

StartTime = time.time()

class RawFormat(enum.IntEnum):
    Raw8 = 0
    Raw10 = 1
    Raw16 = 2

class RawBayer(enum.IntEnum):
    RGGB = 0
    GRBG = 1
    GBRG = 2
    BGGR = 3
    Q_RGGB = 4
    Q_GRBG = 5
    Q_GBRG = 6
    Q_BGGR = 7

#######################################################
# Var
g_nWidth = 8000
g_nHeight = 6000

g_InputPath = '//home/dino/RawShared/Temp/'
g_InputFile = 'FrameID0_W8000_H6000_20211108160758_P10_0000.raw'

g_rawBayer = RawBayer.Q_RGGB

#######################################################

NowDate = datetime.datetime.now()
TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)

def Get_RGBImage(RawArray, bayerFormat):
    Img = RawArray//4
    return Img


def ReMosaic(RawArray):
    #print(np.size(RawArray, 0))
    #print(np.size(RawArray, 1))
    for i in range(0, g_nHeight, 4):
        RawArray[[i+1,i+2],:] = RawArray[[i+2,i+1],:]
    for i in range(0, g_nWidth, 4):
        RawArray[:,[i+1,i+2]] = RawArray[:,[i+2,i+1]]


def DeMosaic(RawArray, bayerFormat):
    RGBRaw = Get_RGBImage(RawArray, bayerFormat)
    RGBRaw = RGBRaw.astype(np.uint8)

    DeMosaicImg = cv2.cvtColor(RGBRaw, cv2.COLOR_BAYER_RG2RGB)

    return DeMosaicImg


def ISP(RawArray):
    bayerFormat = g_rawBayer
    if g_rawBayer >= RawBayer.Q_RGGB or g_rawBayer <= RawBayer.Q_BGGR :
        ReMosaic(RawArray)
        if g_rawBayer == RawBayer.Q_RGGB:
            bayerFormat = RawBayer.RGGB
        elif g_rawBayer == RawBayer.Q_GRBG:
            bayerFormat = RawBayer.GRBG
        elif g_rawBayer == RawBayer.Q_GBRG:
            bayerFormat = RawBayer.GBRG
        elif g_rawBayer == RawBayer.Q_BGGR:
            bayerFormat = RawBayer.BGGR

    RGBImage = DeMosaic(RawArray, bayerFormat)

    return RGBImage


def ReadRaw(rawFormat):
    if rawFormat == RawFormat.Raw8:
        pass
    elif rawFormat == RawFormat.Raw10:
        input_file = open(g_InputPath+g_InputFile, 'rb')
        input_array = np.fromfile(input_file, dtype=np.uint16, count=-1, sep="", offset=0)
        input_file.close()
        input_array = input_array.reshape((g_nHeight, g_nWidth))
    elif rawFormat == RawFormat.Raw16:
        pass
    return input_array

if __name__ == "__main__":    
    input_array = ReadRaw(RawFormat.Raw10)
    OutputImage = ISP(input_array)
    ISPTime = time.time()
    print("Durning ISP Time(sec): ", ISPTime - StartTime)
    
    #Displayed the image
    cv2.namedWindow("ISP Img",0);
    cv2.resizeWindow("ISP Img", 64, 48);
    cv2.imshow("ISP Img", OutputImage)
    cv2.waitKey(0)
        

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)