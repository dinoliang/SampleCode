import array as arr
import numpy as np
import time
import csv
import scipy.misc
import matplotlib.pyplot as plt
import channelrowparse_maxmin as testmain

StartTime = time.time()

if __name__ == "__main__":
    '''
    testmain.nROI_X = 3998
    testmain.nROI_Y = 2998
    '''
    testmain.TransMain(nWidth=8000, nHeight=6000, nX=3998, nY=2998, nROI_W=4, nROI_H=4)
    pass


EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)