import numpy as np
import time
import csv
import datetime
import enum
import os

from PIL import Image
#from skimage import io
from matplotlib import pyplot as plt

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

def Get_R_B_Image(RawArray, bayerFormat, bRImg):
    Img = RawArray//4

    nInitX = 0
    nInitY = 0
    if bayerFormat == RawBayer.RGGB:
        if bRImg == True:
            nInitX = 0
            nInitY = 0
        else:
            nInitX = 1
            nInitY = 1
    elif bayerFormat == RawBayer.GRBG:
        if bRImg == True:
            nInitX = 0
            nInitY = 1
        else:
            nInitX = 1
            nInitY = 2
    elif bayerFormat == RawBayer.GBRG:
        if bRImg == True:
            nInitX = 1
            nInitY = 0
        else:
            nInitX = 0
            nInitY = 1
    elif bayerFormat == RawBayer.BGGR:
        if bRImg == True:
            nInitX = 1
            nInitY = 1
        else:
            nInitX = 0
            nInitY = 0

    for i in range(0, g_nHeight):
        for j in range(0, g_nWidth):
            nCount = 0
            nTotoal = 0

            if (i)%2 == nInitX and (j)%2 == nInitY:
                continue
            else:
                if i-1 >= 0 and (i-1)%2 == nInitX and (j)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i-1,j]
                elif j-1 >= 0 and (i)%2 == nInitX and (j-1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i,j-1]
                elif i+1 < g_nHeight and (i+1)%2 == nInitX and (j)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i+1,j]
                elif j+1 < g_nWidth and (i)%2 == nInitX and (j+1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i,j+1]
                elif i-1 >= 0 and j-1 >= 0 and (i-1)%2 == nInitX and (j-1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i-1,j-1]
                elif i-1 >= 0 and j+1 < g_nWidth and (i-1)%2 == nInitX and (j+1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i-1,j+1]
                elif i+1 < g_nHeight and j-1 >= 0 and (i+1)%2 == nInitX and (j-1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i+1,j-1]
                elif i+1 < g_nHeight and j+1 < g_nWidth and (i+1)%2 == nInitX and (j+1)%2 == nInitY:
                    nCount += 1
                    nTotoal += Img[i+1,j+1]

            if nCount > 0 and nTotoal > 0:
                Img[i,j] = nTotoal // nCount;

    return Img


def Get_GImage(RawArray, bayerFormat):
    Img = RawArray//4

    nInitX0 = 0
    nInitY0 = 0
    nInitX1 = 0
    nInitY1 = 0
    if bayerFormat == RawBayer.RGGB or bayerFormat == RawBayer.BGGR:
        nInitX0 = 0
        nInitY0 = 1
        nInitX1 = 1
        nInitY1 = 0
    else:
        nInitX0 = 0
        nInitY0 = 0
        nInitX1 = 1
        nInitY1 = 1

    for i in range(0, g_nHeight):
        for j in range(0, g_nWidth):
            nCount = 0
            nTotoal = 0

            if (i)%2 == nInitX0 and (j)%2 == nInitY0:
                continue
            elif (i)%2 == nInitX1 and (j)%2 == nInitY1:
                continue
            else:
                if i-1 >= 0 and \
                (((i-1)%2 == nInitX0 and (j)%2 == nInitY0) or ((i-1)%2 == nInitX1 and (j)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i-1,j]
                elif j-1 >= 0 and \
                (((i)%2 == nInitX0 and (j-1)%2 == nInitY0) or ((i)%2 == nInitX1 and (j-1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i,j-1]
                elif i+1 < g_nHeight and \
                (((i+1)%2 == nInitX0 and (j)%2 == nInitY0) or ((i+1)%2 == nInitX1 and (j)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i+1,j]
                elif j+1 < g_nWidth and \
                (((i)%2 == nInitX0 and (j+1)%2 == nInitY0) or ((i)%2 == nInitX1 and (j+1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i,j+1]
                elif i-1 >= 0 and j-1 >= 0 and \
                (((i-1)%2 == nInitX0 and (j-1)%2 == nInitY0) or ((i-1)%2 == nInitX1 and (j-1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i-1,j-1]
                elif i-1 >= 0 and j+1 < g_nWidth and \
                (((i-1)%2 == nInitX0 and (j+1)%2 == nInitY0) or ((i-1)%2 == nInitX1 and (j+1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i-1,j+1]
                elif i+1 < g_nHeight and j-1 >= 0 and \
                (((i+1)%2 == nInitX0 and (j-1)%2 == nInitY0) or ((i+1)%2 == nInitX1 and (j-1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i+1,j-1]
                elif i+1 < g_nHeight and j+1 < g_nWidth and \
                (((i+1)%2 == nInitX0 and (j+1)%2 == nInitY0) or ((i+1)%2 == nInitX1 and (j+1)%2 == nInitY1)):
                    nCount += 1
                    nTotoal += Img[i+1,j+1]

            if nCount > 0 and nTotoal > 0:
                Img[i,j] = nTotoal // nCount;

    return Img


def ReMosaic(RawArray):
    #print(np.size(RawArray, 0))
    #print(np.size(RawArray, 1))
    for i in range(0, g_nHeight, 4):
        RawArray[[i+1,i+2],:] = RawArray[[i+2,i+1],:]
    for i in range(0, g_nWidth, 4):
        RawArray[:,[i+1,i+2]] = RawArray[:,[i+2,i+1]]


def DeMosaic(RawArray, bayerFormat):
    RGBImage = np.zeros((g_nHeight, g_nWidth, 3))
    RGBImage[:, :, 0] = Get_R_B_Image(RawArray, bayerFormat, True)
    RGBImage[:, :, 1] = Get_GImage(RawArray, bayerFormat)
    RGBImage[:, :, 2] = Get_R_B_Image(RawArray, bayerFormat, False)
    #print(RGBImage[0:1,:,0])
    #print(RGBImage[0:1,:,1])
    #print(RGBImage[0:1,:,2])

    RGBImage = RGBImage.astype(np.uint8)
    return RGBImage


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
    ImageData = Image.fromarray(OutputImage)
    #print(np.size(OutputImage, 0))
    #print(np.size(OutputImage, 1))
    #print(np.size(OutputImage, 2))
    ImageData.save('/home/dino/RawShared/Temp/out_{}.bmp'.format(TimeInfo))
    image = Image.open('/home/dino/RawShared/Temp/out_{}.bmp'.format(TimeInfo))
    plt.imshow(image)
    plt.show()
    #plt.imshow(OutputImage)
    #plt.show()
    

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)