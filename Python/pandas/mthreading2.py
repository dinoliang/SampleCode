from bs4 import BeautifulSoup
import concurrent.futures
import requests
import time
 
 
def scrape(urls):
    response = requests.get(urls)
 
    soup = BeautifulSoup(response.content, "lxml")
 
    # 爬取文章標題
    titles = soup.find_all("h3", {"class": "post_title"})
 
    for title in titles:
        print(title.getText().strip())
 
    time.sleep(2)
 
 
base_url = "https://www.inside.com.tw/tag/AI"
urls = [f"{base_url}?page={page}" for page in range(1, 6)]  # 1~5頁的網址清單
 
start_time = time.time()  # 開始時間
 
# 同時建立及啟用10個執行緒
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scrape, urls)
 
end_time = time.time()
print(f"{end_time - start_time} 秒爬取 {len(urls)} 頁的文章")