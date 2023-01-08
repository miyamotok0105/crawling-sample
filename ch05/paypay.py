# -*- coding: utf-8 -*-

"""
Paypayモールのデータを取得する
"""
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
CSV_NAME = "output/paypay.csv"

def update_page_num(driver):
    while True:
        time.sleep(SLEEP_TIME)
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        if '検索結果は以上です' in driver.page_source:
            break

def get_item_urls(driver, page_num):
    item_elements = driver.find_elements(By.CLASS_NAME, "ListItem_link")
    return ([i.get_attribute("href") for i in item_elements])

def get_item_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")
    result["url"] = driver.current_url
    result["name"] = driver.find_element(By.CLASS_NAME, 'ItemName').text
    result["product_code"] = [i.text.split(":")[-1] for i in driver.find_elements(By.CLASS_NAME, 'ItemDetails_list')]
    result["price"] = driver.find_element(By.CLASS_NAME, 'ItemPrice_price').text
    if len(driver.find_elements(By.ID, 'itm')) ==0:
        result["description"] =""    
    else:
        result["description"] = driver.find_element(By.ID, 'itm').text
    return result

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = 'https://paypaymall.yahoo.co.jp/search?p=%E3%83%9E%E3%83%AA%E3%82%AA%E3%82%AB%E3%83%BC%E3%83%888&cid=&brandid=&kspec=&catopn=&b=1'
        driver.get(url)
        time.sleep(SLEEP_TIME)
        
        totla_num_element = driver.find_element(By.CLASS_NAME,'SearchTotal_search')
        total_num = int(totla_num_element.text.split('件')[0])
        update_page_num(driver)
        item_urls = get_item_urls(driver, total_num)

        result = list()
        for i_url in item_urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_item_info(driver))

        pd.DataFrame(result).to_csv(CSV_NAME)    
        # pd.DataFrame().to_csv(CSV_NAME, encoding='utf_8_sig')    

    finally:
        driver.quit()
