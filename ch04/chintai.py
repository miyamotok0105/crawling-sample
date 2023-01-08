# -*- coding: utf-8 -*-

"""
物件情報CHINTAIのデータを取得する
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

CSV_NAME = "output/chintai.csv"
SLEEP_TIME = 5

def update_page_num(driver, page_num):
    pager_element = driver.find_element(By.CLASS_NAME, "list_pager")
    nextbutton_element = pager_element.find_element(By.CLASS_NAME, "next")
    a_element = nextbutton_element.find_element(By.TAG_NAME, "a")
    driver.get(a_element.get_attribute("href"))

def get_item_urls(driver):
    property_elements = driver.find_elements(By.CSS_SELECTOR, ".cassette_item.build")
    a_elements = [i.find_element(By.CSS_SELECTOR, ".js_bukken_info_area.ga_bukken_cassette") for i in property_elements]
    return [i.get_attribute("href") for i in a_elements]

def get_item_info(driver):
    result = dict()
    result["url"] = driver.current_url
    result["id"] = result["url"].split("/")[-2]
    result["title"] = driver.find_element(By.TAG_NAME, "h2").text.replace("の賃貸物件詳細", "")
    result["price"] = driver.find_element(By.CLASS_NAME, "price").text
    result["access"]  = driver.find_element(By.CLASS_NAME, "mod_necessaryTime").text
    return result

def is_last_page(driver):
    paging_text = driver.find_element(By.CLASS_NAME, "list_pager").text
    return not "次" in paging_text

if __name__=="__main__":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    base_url = "https://www.chintai.net/list/?o=10&pageNoDisp=20%E4%BB%B6&o=10&rt=51&prefkey=tokyo&ue=000004864&urlType=dynamic&cf=0&ct=60&k=1&m=0&m=2&jk=0&jl=0&sf=0&st=0&j=&h=99&b=1&b=2&b=3&jks="    
    driver.get(base_url)   
    time.sleep(SLEEP_TIME)

    page_num = 1
    item_urls = list()
    while True:
        time.sleep(SLEEP_TIME) 
        urls = get_item_urls(driver)
        print(urls)
        item_urls.extend(urls)
        if is_last_page(driver):
            break
        else:
            page_num+=1
            update_page_num(driver, page_num)
    item_infos = list()
    for i_url in item_urls:
        driver.get(i_url)   
        time.sleep(SLEEP_TIME)
        item_infos.append(get_item_info(driver))
    
    pd.DataFrame(item_infos).to_csv(CSV_NAME, index=False)