#######################################################
### Calculate the information by pixel csv file (not origin bin file (raw image))

import numpy as np
import pandas as pd
import time
import datetime
import requests
import sqlite3
from bs4 import BeautifulSoup

StartTime = time.time()

#######################################################

#######################################################

NowDate = datetime.datetime.now()

class Stock:
    def __init__(self, *stock_numbers) -> None:
        '''
        *stock_numbers not only one parameter, maybe more
        '''
        self.stock_numbers = stock_numbers
        print(self.stock_numbers)
        pass

    def EmptyFunc(self):
        return

    def GetStock(self):
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

    def Scrape(self):
        result = list()  # 最終結果

        for stock_number in self.stock_numbers:
            response = requests.get('https://tw.stock.yahoo.com/quote/{}'.format(stock_number))
            soup = BeautifulSoup(response.text, "lxml")
            stock_name = soup.find('h1', {'class': 'C($c-link-text) Fw(b) Fz(24px) Mend(8px)'}).getText()
            stock_date = soup.find('span', {'class': 'C(#6e7780) Fz(14px) As(c)'}).getText()
            market_date = stock_date[0:15]  #日期
            market_time = stock_date[16:21]  #時間
            ul = soup.find('ul', {'class': 'D(f) Fld(c) Flw(w) H(192px) Mx(-16px)'})
            items = ul.find_all('li', {'class': 'price-detail-item H(32px) Mx(16px) D(f) Jc(sb) Ai(c) Bxz(bb) Px(0px) Py(4px) Bdbs(s) Bdbc($bd-primary-divider) Bdbw(1px)'})
            data = tuple(item.find_all('span')[1].getText() for item in items)
            (market_date, stock_name, market_time) + data
            result.append((market_date, stock_name, market_time) + data)
        return result

    def Scrape2(self):
        url = "https://partner-query.finance.yahoo.com/v8/finance/chart/%5EDJI?range=1d&comparisons=undefined&includePrePost=false&interval=2m&corsDomain=tw.stock.yahoo.com&.tsrc=yahoo-tw"
        response = requests.get(url)
        
        close = response.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"] #美股指數
        volume = response.json()["chart"]["result"][0]["indicators"]["quote"][0]["volume"]  #成交量
        
        tw_time = []  #存放日期格式的台灣時間
        timestamps = response.json()["chart"]["result"][0]["timestamp"]
        for index in range(len(timestamps)):
        tw_time.append(datetime.datetime.utcfromtimestamp(timestamps[index]-18000)) #將時間戳記轉為台灣時間
        pass

if __name__ == "__main__":
    st = Stock('2451', '2454')

    '''
    st.GetStock()
    '''
    
    '''
    result = st.Scrape()
    print(result)
    '''
    
    
    pass


EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
