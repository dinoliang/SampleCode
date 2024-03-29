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

import ispawb001

import png
from scipy.ndimage import gaussian_filter

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
g_bResolution = True

g_nWidth = 9728
g_nHeight = 8192
#g_nWidth = 8000
#g_nHeight = 6000

#g_InputPath = '//home/dino/RawShared/TEG_Output/20220122/'
#g_InputFile = 'SamplingData_DESKTOP-D5MOV6A_FULL_20220122_151835.bin'
#g_InputFile = 'SamplingData_DESKTOP-D5MOV6A_FULL_20220122_151835_ReMosaic.bin'
#g_InputPath = '//home/dino/RawShared/Temp/'
#g_InputFile = 'FrameID0_W8000_H6000_20211130153042_P10_0000.bin'

g_InputPath = '//home/dino/RawShared/TEG_Output/20220124/'
g_InputFile = 'SamplingData_DESKTOP-D5MOV6A_FULL_20220124_170605_12db.bin'

g_rawBayer = RawBayer.Q_GRBG#RawBayer.Q_RGGB


g_bDeMosaic = True

#ISP 
g_bISP_DeNoise = False
g_bISP_AWB = False
g_bISP_Sharp = False
#https://www.pathpartnertech.com/camera-tuning-understanding-the-image-signal-processor-and-isp-tuning/
#Color Correction
#Lens shading correction
#Defect pixel correction (BPC)
#Gamma correction
#Local tone mapping
#Auto Exposure (AEC)
#Auto Focus
#https://www.gushiciku.cn/pl/p7wM/zh-tw
#black level compensation (BLC)
#lens shading correction
#bad pixel correction
#demosaic#
#Bayer denoise
#awb
#color correction
#gamma correction
#Convert color space
#DeNoise
#edge enhance
#enhance color、contrast
#Flip、Mirror、Rotation
#output YUV or RGB

g_bSaveReMosaicRaw = False
g_bSaveTiff = True
g_SavingFileName = 'FrameID0_W8000_H6000_20211130153042_P10_0000.bmp'

g_bDisplay = True

#######################################################

NowDate = datetime.datetime.now()
TimeInfo = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(NowDate.year, NowDate.month, NowDate.day, NowDate.hour, NowDate.minute, NowDate.second)

def SaveTiff(RawImage):
    cv2.imwrite(g_InputPath + g_SavingFileName, RawImage)

def SavePng(RawImage):
    #write_png('example1.png', RawImage, bitdepth=16)
    # Use pypng to write zgray as a grayscale PNG.
    #with open('example1.png', 'wb') as f:
    #    writer = png.Writer(width=g_nWidth, height=g_nHeight, bitdepth=16, greyscale=True)
    #    #zgray2list = RawImage.tolist()
    #    #print(zgray2list)
    #    writer.write(f, RawImage)
    nrows = 240
    ncols = 320
    np.random.seed(12345)
    x = np.random.randn(nrows, ncols, 3)

    # y is our floating point demonstration data.
    y = gaussian_filter(x, (16, 16, 0))

    # Convert y to 16 bit unsigned integers.
    z = (65535*((y - y.min())/y.ptp())).astype(np.uint16)

    # Use pypng to write z as a color PNG.
    with open('foo_color.png', 'wb') as f:
        writer = png.Writer(width=z.shape[1], height=z.shape[0], bitdepth=16)
        # Convert z to the Python list of lists expected by
        # the png writer.
        z2list = z.reshape(-1, z.shape[1]*z.shape[2]).tolist()
        writer.write(f, z2list)

def SaveRaw(RawImage):
    output_array_header = np.array([g_nWidth, g_nHeight])
    output_array_data = RawImage.reshape((g_nHeight * g_nWidth))
    output_array = np.append(output_array_header, output_array_data)
    output_array.astype('int16').tofile(g_InputPath + g_SavingFileName)
    pass

def ReMosaic(RawArray):
    #print(np.size(RawArray, 0))
    #print(np.size(RawArray, 1))
    for i in range(0, g_nHeight, 4):
        RawTemp = RawArray[[i+1,i+2],:]
        RawArray[[i+1,i+2],:] = RawArray[[i+2,i+1],:]
        RawArray[[i+2,i+1],:] = RawTemp
    for i in range(0, g_nWidth, 4):
        RawTemp = RawArray[:,[i+1,i+2]]
        RawArray[:,[i+1,i+2]] = RawArray[:,[i+2,i+1]]
        RawArray[:,[i+2,i+1]] = RawTemp
    if (g_bSaveReMosaicRaw):
        SaveRaw(RawArray);
    return RawArray


def DeMosaic(RawArray, bayerFormat):
    RGBRaw = RawArray // 4
    RGBRaw = RGBRaw.astype(np.uint8)
    #print('RGBRaw[0,0], RGBRaw[0,1] ', RGBRaw[0,0], RGBRaw[0,1])

    if bayerFormat == RawBayer.RGGB:
        cvtColorFormat = cv2.COLOR_BAYER_RG2RGB
    elif bayerFormat == RawBayer.GRBG:
        cvtColorFormat = cv2.COLOR_BAYER_GR2RGB
    elif bayerFormat == RawBayer.GBRG:
        cvtColorFormat = cv2.COLOR_BAYER_GB2RGB
    elif bayerFormat == RawBayer.BGGR:
        cvtColorFormat = cv2.COLOR_BAYER_BG2RGB

    DeMosaicImg = cv2.cvtColor(RGBRaw, cvtColorFormat)

    return DeMosaicImg


def DeNoise(RawImg):
    '''
    cv2.fastNlMeansDenoising() - works with a single grayscale images
    cv2.fastNlMeansDenoisingColored() - works with a color image.
    cv2.fastNlMeansDenoisingMulti() - works with image sequence captured in short period of time (grayscale images)
    cv2.fastNlMeansDenoisingColoredMulti() - same as above, but for color images.
    '''
    DeDeNoiseImg = cv2.fastNlMeansDenoisingColored(RawImg, None, 10, 10, 7, 21)

    return DeDeNoiseImg


def SharpImage(RawImg):
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
    image_sharp = cv2.filter2D(src=RawImg, ddepth=-1, kernel=kernel)

    return image_sharp


def ISP(RawArray):
    bayerFormat = g_rawBayer
    if g_rawBayer >= RawBayer.Q_RGGB or g_rawBayer <= RawBayer.Q_BGGR :
        ReMosaicImg = ReMosaic(RawArray)
        if g_rawBayer == RawBayer.Q_RGGB:
            bayerFormat = RawBayer.RGGB
        elif g_rawBayer == RawBayer.Q_GRBG:
            bayerFormat = RawBayer.GRBG
        elif g_rawBayer == RawBayer.Q_GBRG:
            bayerFormat = RawBayer.GBRG
        elif g_rawBayer == RawBayer.Q_BGGR:
            bayerFormat = RawBayer.BGGR
    else:
        ReMosaicImg = RawArray
    StageTime = time.time()
    print("Durning ReMosaic Stage Time(sec): ", StageTime - StartTime)

    if g_bDeMosaic:
        DeMosaicImg = DeMosaic(ReMosaicImg, bayerFormat)
        RGBImage = DeMosaicImg
        StageTime = time.time()
        print("Durning DeMosaic Stage Time(sec): ", StageTime - StartTime)
    else:
        RGBImage = ReMosaicImg

    if g_bISP_DeNoise:
        DeNoiseImg = DeNoise(RGBImage)
        RGBImage = DeNoiseImg
        StageTime = time.time()
        print("Durning DeNoise Stage Time(sec): ", StageTime - StartTime)

    if g_bISP_AWB:
        AWBImg = ispawb001.white_balance_1(RGBImage)
        #AWBImg = ispawb001.GW(DeMosaicImg)
        RGBImage = AWBImg
        StageTime = time.time()
        print("Durning AWB Stage Time(sec): ", StageTime - StartTime)

    if g_bISP_Sharp:
        SharpImg = SharpImage(RGBImage)
        RGBImage = SharpImg
        StageTime = time.time()
        print("Durning Sharp Stage Time(sec): ", StageTime - StartTime)

    return RGBImage


def ReadRaw(rawFormat):
    if rawFormat == RawFormat.Raw8:
        pass
    elif rawFormat == RawFormat.Raw10:
        input_file = open(g_InputPath+g_InputFile, 'rb')
        #if g_bResolution:
        #    input_array_r = np.fromfile(input_file, dtype=np.uint16, count=2, sep="", offset=0)
        #    g_nWidth = input_array_r[0]
        #    g_nHeight = input_array_r[1]
        #input_array = np.fromfile(input_file, dtype=np.uint16, count=-1, sep="", offset=0)
        input_array = np.fromfile(input_file, dtype=np.uint16, count=-1, sep="", offset=4)
        input_file.close()
        print("Raw resolution W:{0}, H:{1}".format(g_nWidth, g_nHeight))
        print("Max LSB:{0}, Min LSB:{1}".format(np.max(input_array), np.min(input_array)))
        input_array = input_array.reshape((g_nHeight, g_nWidth))
    elif rawFormat == RawFormat.Raw16:
        pass
    return input_array


if __name__ == "__main__":    
    input_array = ReadRaw(RawFormat.Raw10)
    #OutputImage = ISP(input_array)
    #ISPTime = time.time()
    #print("Durning ISP Time(sec): ", ISPTime - StartTime)

    #if g_bSaveTiff:
    #    SaveTiff(OutputImage)

    SavePng(input_array)

    #Displayed the image
    #if g_bDisplay:
    #    cv2.namedWindow("ISP Img",0);
    #    cv2.resizeWindow("ISP Img", 64, 48);
    #    cv2.imshow("ISP Img", OutputImage)
    #    cv2.waitKey(0)
    #
    #cv2.destroyAllWindows()

    
        

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)
