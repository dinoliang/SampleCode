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
    testmain.TransMain(8000, 6000, 3998, 2998, 4, 4)
    pass


EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)