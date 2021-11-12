import array as arr
import numpy as np
import time
import csv
import scipy.misc
import matplotlib.pyplot as plt

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
    print('X: \n', X)
    print('X.shape: ', X.shape)
    print('X.dtype: ', X.dtype)
    print('np.size(X): ', np.size(X))
    print('np.size(X, 0): ', np.size(X, 0))
    print('np.size(X, 1): ', np.size(X, 1))
    print('np.prod(X.shape): ', np.prod(X.shape))
    X_dim = X.shape
    print('X.shape[0]: ', X_dim[0])
    print('X.shape[1]: ', X_dim[1])
    print('len(X): ', len(X))
    print('X.sum(axis=0): ', X.sum(axis=0))
    print('X.sum(axis=1): ', X.sum(axis=1))
    print('np.std(X, 0): ', np.std(X, 0))
    print('np.std(X, 1): ', np.std(X, 1))
    print('np.std(X): ', np.std(X))
    print('X.T: \n', X.T)


def np_append_test():
    '''
    arr = np.array([[[]]])
    arr = np.append(arr, '1')
    '''
    '''
    arr = np.empty((0,0,0))
    data_array = np.zeros((3, 5, 6), dtype=np.int)
    arr = np.append(arr, data_array)
    print(arr)
    '''
    empty_array = np.empty((0,4))
    # Append a row to the 2D numpy array
    empty_array = np.append(empty_array, np.array([[11, 21, 31, 41]]), axis=0)
    # Append 2nd rows to the 2D Numpy array
    empty_array = np.append(empty_array, np.array([[15, 25, 35, 45]]), axis=0)
    print('2D Numpy array:')
    print(empty_array)

    empty_array = np.append(empty_array, np.array([[16, 26, 36, 46], [17, 27, 37, 47]]), axis=0)
    print('2D Numpy array:')
    print(empty_array)


def testText():
    print('Hello', end='')
    print('World')


def numpy_condition_001():
    x = np.array([[10, 20, 30],
               [3, 50, 5]])
    y = np.array([[70, 80, 90],
                [100, 110, 120]])
    condition = np.where(x>20,x,y)
    print("Input array :")
    print(x)
    print(y)
    print("Output array with condition applied:")
    print(condition)


def numpy_condition_002():
    m = np.where([[True, False, True],
                  [False, True, False]],
                 [[1,2,3],
                  [4, 5, 6]],
                 [[7,8,9],
                  [10, 11, 12]])
    print(m)


def numpy_condition_003():
    m = np.array([1,2,3,4,5])
    n = np.where((m > 1) & (m < 5), m, 0)
    print(n)


def Matplotlib_Show():
    #lena=scipy.misc.lena()
    ascent=scipy.misc.ascent()
    plt.gray()
    plt.imshow(ascent)
    plt.show()


if __name__ == "__main__":
    #testSTD_AVG()

    #test3D()
    #test3D_2()

    #test2D_2()

    #np_append_test()

    #testText()

    #numpy_condition_003()

    Matplotlib_Show()
    pass


EndTime = time.time()
print("Durning Time(sec): ", EndTime - StartTime)