import array as arr
import numpy as np
import time
import csv

StartTime = time.time()

def testSTD_AVG():
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


def test3D():
    data_array = np.zeros((3, 5, 6), dtype=np.int)
    data_array[1, 2, 3] = 1 #[depth, V, H]
    print(data_array)
    print(data_array[:,:,0])
    print(data_array[:,:,1])
    print(data_array[:,:,2])

def test3D_2():
    np.random.seed(123)
    X = np.random.randint(0, 5, [4, 2, 3])
    print(X)
    #print(X.sum(axis=0))
    #print(X.sum(axis=1))
    #print(X.sum(axis=2))
    Y = X.sum(axis=0)
    print(Y)
    print(Y.sum(axis=0))
    print(Y.sum(axis=1))


def test2D_2():
    np.random.seed(123)
    X = np.random.randint(0, 5, [4, 2])
    print(X)
    print(X.sum(axis=0))
    print(X.sum(axis=1))
    print(np.std(X, 0))
    print(np.std(X, 1))
    print(np.std(X))


if __name__ == "__main__":
    '''
    testSTD_AVG()
    '''
    '''
    #test3D()
    test3D_2()
    '''
    test2D_2()


EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)