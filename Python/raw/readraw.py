import array as arr
import numpy as np
import time

StartTime = time.time()

nWidth = 4000
nHeight = 3000

"""
# read unsigned shout by array
input_file = open('/mnt/hgfs/LinuxFolder/SampleRaw/DtSample40003000Raw/FrameID0_W4000_H3000_15724245_P10_0000.raw', 'rb')

input_array = arr.array('H')   # H : unsigned shout
input_array.fromfile(input_file, nWidth*nHeight)   # 讀出3個
for item in input_array:
    print(item)

input_file.close()
"""

# read unsigned shout numpy
input_file = open('/mnt/hgfs/LinuxFolder/SampleRaw/DtSample40003000Raw/FrameID0_W4000_H3000_15724245_P10_0000.raw', 'rb')
input_array = np.fromfile(input_file, dtype=np.uint16)
#for item in input_array:
#    print(item)
#print (input_array[0])
#print (input_array[1])
#print (input_array[2])
    
input_array = input_array.reshape((nHeight, nWidth))
#for item in input_array:
#    print(item)
#print (input_array[0,0])
#print (input_array[0,1])
#print (input_array[0,2])

R_array = np.zeros((nHeight//2, nWidth//2))
Gr_array = np.zeros((nHeight//2, nWidth//2))
Gb_array = np.zeros((nHeight//2, nWidth//2))
B_array = np.zeros((nHeight//2, nWidth//2))

for i in range(0,nHeight):
    for j in range(0,nWidth):
        if (i%4==0 or i%4==1) and (j%4==0 or j%4==1):
            #print(i,j, ":", input_array[i,j])
            R_array[(i+1)//2,(j+1)//2] = input_array[i,j]
        elif (i%4==0 or i%4==1) and (j%4==2 or j%4==3):
            Gr_array[(i+1)//2,(j-1)//2] = input_array[i,j]
        elif (i%4==2 or i%4==3) and (j%4==0 or j%4==1):
            Gb_array[(i-1)//2,(j+1)//2] = input_array[i,j]
        elif (i%4==2 or i%4==3) and (j%4==2 or j%4==3):
            B_array[(i-1)//2,(j-1)//2] = input_array[i,j]

'''
for i in range(0,2):
    for j in range(0,2):
        print("R", i, j, ":", R_array[i,j])
        print("Gr", i, j, ":", Gr_array[i,j])
        print("Gb", i, j, ":", Gb_array[i,j])
        print("B", i, j, ":", B_array[i,j])
'''

R_STD = np.std(R_array)
Gr_STD = np.std(Gr_array)
Gb_STD = np.std(Gb_array)
B_STD = np.std(B_array)
print("R_STD", R_STD, ", Gr_STD", Gr_STD, ", Gb_STD", Gb_STD, ", B_STD", B_STD)

R_AVG = np.average(R_array)
Gr_AVG = np.average(Gr_array)
Gb_AVG = np.average(Gb_array)
B_AVG = np.average(B_array)
print("R_AVG", R_AVG, ", Gr_AVG", Gr_AVG, ", Gb_AVG", Gb_AVG, ", B_AVG", B_AVG)

EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)