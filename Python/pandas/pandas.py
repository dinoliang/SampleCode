from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
 
 
browser = webdriver.Chrome(ChromeDriverManager().install())  #安裝Chrome驅動程式及建立Chrome物件
browser.get("https://old.accupass.com/search/r/0/0/0/0/4/0/00010101/99991231?q=python")
 
soup = BeautifulSoup(browser.page_source, "lxml")
activities = soup.find_all("div", {"class": "apcss-activity-card ng-isolate-scope"})
 
result = []
for activity in activities:
 
    #活動名稱
    title = activity.find("h3", {"class": "apcss-activity-card-title ng-binding"}).getText().strip()
    
    #觀看人數
    view = activity.find("span", {"class": "apcss-activity-pageview ng-binding"}).getText().strip()
    
    #喜歡人數(去除其中的中文字)
    like = activity.find("span", {"class": "apcss-activity-card-like ng-binding"}).getText().strip().replace(" 人喜歡", "")
    
    #售票狀態
    status = activity.find("a", {"class": "apcss-btn apcss-btn-block ng-binding activity-card-status-ready"})
    
    #如果售票狀態為已完售，則爬取另一個樣式類別(class)
    if status == None:
        status = activity.find("a", {"class": "apcss-btn apcss-btn-block ng-binding activity-card-status-end"})
		
    result.append((title, int(view), int(like), status.getText()))
 
 
df = pd.DataFrame(result, columns=["活動名稱", "觀看人數", "喜歡人數", "售票狀態"])
 
new_df = df[df["售票狀態"] == "熱銷中"]  #篩選資料
 
sort_df = new_df.sort_values(["觀看人數"], ascending=False)  #依據觀看人數來遞減排序
 
sort_df.to_excel("accupass.xlsx", sheet_name="activities", index=False)  # 匯出Excel檔案(不寫入資料索引值)
 
browser.quit()  #關閉Chrome瀏覽器