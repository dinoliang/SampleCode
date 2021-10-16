import array as arr
import numpy as np


"""
# read unsigned shout by array
input_file = open('/mnt/hgfs/LinuxFolder/SampleRaw/DtSample40003000Raw/FrameID0_W4000_H3000_15724245_P10_0000.raw', 'rb')

input_array = arr.array('H')   # H : unsigned shout
input_array.fromfile(input_file, 4000*3000)   # 讀出3個
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
    
input_array = input_array.reshape((3000, 4000))
#for item in input_array:
#    print(item)
#print (input_array[0,0])
#print (input_array[0,1])
#print (input_array[0,2])
