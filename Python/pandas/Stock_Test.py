#######################################################
### Calculate the information by pixel csv file (not origin bin file (raw image))

import numpy as np
import pandas as pd
import time
import datetime
import requests
import sqlite3

StartTime = time.time()

#######################################################

#######################################################

NowDate = datetime.datetime.now()

def EmptyFunc():
    return

def GetStock():
    today = NowDate.strftime('%Y%m%d')  #西元年(yyyymmdd)
    chinese_today = f"{(NowDate.year - 1911)}/{NowDate.strftime('%m/%d')}"  #民國年(yyy/mm/dd)

    response = requests.get(f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={today}&stockNo=2891')
    response_data = response.json()['data']
    #print(response_data)

    result = [data for index, data in enumerate(response_data) if chinese_today in response_data[index]]
    if result:  #如果有資料
        result[0].insert(0, '2891')
        print(result)

    return

if __name__ == "__main__":
    GetStock()
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
