# -*- coding: utf-8 -*-

"""
BUYMAのデータを取得する
"""
import time
import datetime
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

CSV_NAME = "./output/buyma.csv"
SLEEP_TIME = 2

def update_page_num(driver, search_word, page_num):
    base_url = "https://www.buyma.com/r/"
    next_url = base_url + search_word + f"_{page_num}"
    driver.get(next_url)

def get_item_urls(driver):
    product_elements = driver.find_elements(By.CLASS_NAME, "product_name")
    a_elements = [i.find_element(By.TAG_NAME, "a") for i in product_elements]
    return [i.get_attribute("href") for i in a_elements]

def get_item_info(driver):
    result = dict()

    result["id"] = driver.current_url.split("/")[-2]
    result["url"] = driver.current_url
    result["datetime"] = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S')    
    result["title"]= driver.find_element(By.ID, 'item_h1').text
    result["price"]  = driver.find_element(By.ID, "abtest_display_pc").text
    result["description"] = driver.find_element(By.CLASS_NAME, "free_txt").text
    print(result)
    return result
    
if __name__=="__main__":
    try:    
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        driver = webdriver.Chrome(ChromeDriverManager().install())
    
        base_url = "https://www.buyma.com/r/"
        search_word = "ネクタイ%20ベージュ%20シルク%20チェック"
        target_url = base_url + search_word 
        driver.get(target_url)   
        first_page_url = driver.current_url
        time.sleep(SLEEP_TIME)
    
        page_num=0
        item_urls = list()
        while True: 
            time.sleep(3) 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            page_num+=1
            update_page_num(driver, search_word, page_num)
            print(driver.current_url, first_page_url)
            if driver.current_url.lower() == first_page_url: 
                break
    
        item_infos = list()
        for i_url in item_urls:
            try:
                driver.get(i_url)   
                time.sleep(SLEEP_TIME)
                item_infos.append(get_item_info(driver))
            except:
                print(i_url)
    finally:
        driver.quit()
        pd.DataFrame(item_infos).to_csv(CSV_NAME, index=False)