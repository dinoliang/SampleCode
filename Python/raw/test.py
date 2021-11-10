import array as arr
import numpy as np
import time
import csv

StartTime = time.time()

if __name__ == "__main__":
    np_array = np.random.randint(low=667,high=726,size=100)
    print(np_array)
    array_STD = np.std(np_array)
    array_AVG = np.average(np_array)
    print('STD: ', array_STD)
    print('AVG: ', array_AVG)

    np_array2 = np.array([676, 673, 726, 704, 680, 688, 677, 691, 694, 667])
    array_STD = np.std(np_array2)
    array_AVG = np.average(np_array2)
    print('STD: ', array_STD)
    print('AVG: ', array_AVG)


EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)