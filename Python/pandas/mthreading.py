import threading
import time
 
 
def scraper():
    print("start")
    time.sleep(10)
    print("sleep done")
 
 
t = threading.Thread(target=scraper)  #建立執行緒
t.start()  #執行
print("end")