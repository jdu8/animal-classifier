import requests
from bs4 import BeautifulSoup
import os
import lxml
from selenium import webdriver
# os.makedirs("pic")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd



animals=['dog','cat','bird','snake','cow','butterfly','horse','spider']
url="https://unsplash.com/s/photos/"
PATH="driver\chromedriver.exe"
driver=webdriver.Chrome(PATH)
driver.maximize_window()

for animal in animals:
    print(animal)
    temp_url=url+animal
    driver.get(temp_url)
    time.sleep(2)
    # l=['//*[@id="app"]/div/div[3]/div[4]/div[3]/div[1]/button','//*[@id="app"]/div/div[2]/div[3]/div[6]/div[1]/button','//*[@id="app"]/div/div[3]/div[3]/div[3]/div[1]/button']
    ele = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Load more photos")]'))
                    )
    ele.click()
    l=[]
    time.sleep(2)
    all_image=[]
    prev_len=0
    while len(all_image)<5000:
        # time.sleep(1)
        # driver.execute_script("window.scrollTo(0, 0.85*document.body.scrollHeight);")
        docHeight=int(driver.execute_script("return document.body.scrollHeight"))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scrollVal=int((0.15*docHeight)//30)
        for _ in range(int(0.85*docHeight),docHeight,scrollVal):
            driver.execute_script(f"window.scrollTo(0, {_});")
        data = BeautifulSoup(driver.page_source,'lxml')
        all_image=data.find_all('figure',itemprop="image")
        if len(all_image)<=prev_len:
            docHeight=int(driver.execute_script("return document.body.scrollHeight"))
            for _ in range(docHeight,int(0.95*docHeight),-2):
                driver.execute_script(f"window.scrollTo(0, {_});")
        print(len(all_image))
    print("-------------------")
    for i in all_image:
        if i.find('a',rel="nofollow") != None:
            temp=[i.find('a')['title'],i.find('a',rel="nofollow")['href']]
            if temp not in l:
                l.append(temp)
    print(len(l))
    df = pd.DataFrame(l)
    df.to_csv(f'csvs\\{animal}.csv')
    time.sleep(2)











# driver.quit()
# filename=f'{animal}.csv'
# with open(filename, 'w') as csvfile: 
#     # creating a csv writer object 
#     csvwriter = csv.writer(csvfile) 
        
#     # # writing the fields 
#     # csvwriter.writerow(fields) 
        
#     # writing the data rows 
#     csvwriter.writerows(l)