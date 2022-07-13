#######################################################
### Calculate the information by pixel csv file (not origin bin file (raw image))

import numpy as np
import pandas as pd
import time
import datetime

StartTime = time.time()

#######################################################

#######################################################

NowDate = datetime.datetime.now()

def EmptyFunc():
    return

def PrintStockEveryDay():
    # 將 csv 檔案轉換成 DataFrame
    df = pd.read_csv('STOCK_DAY_ALL_20220627.csv')

    # 輸入資料概況
    print(df.info())
    print(df.describe())

    # 輸出頭尾資料
    print(df.head())
    print(df.tail())

    return

if __name__ == "__main__":
    PrintStockEveryDay()
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
