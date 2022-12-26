# -*- coding: utf-8 -*-

"""
yamadaモールのデータを取得する
"""
import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

ITEM_SHOW_NUM = 20
SLEEP_TIME = 2
CSV_NAME = "output/ymall.csv"

def get_total_page_num(driver):
    result_elemet = driver.find_element(By.CLASS_NAME, "result") 
    result_nums = [int(i.text) for i in result_elemet.find_elements(By.CLASS_NAME, "highlight")]
    return (result_nums[0] //  ITEM_SHOW_NUM) +1
    
def get_item_urls(driver):
    itemlist_element = driver.find_element(By.CLASS_NAME, 'item_list') 
    item_elements = itemlist_element.find_elements(By.CLASS_NAME, 'item_name')
    a_elements = [i.find_element(By.TAG_NAME,'a') for i in item_elements]
    return [i.get_attribute("href") for i in a_elements]

def update_page(driver, page_num):
    option = f"&o={(page_num-1) * ITEM_SHOW_NUM}"
    driver.get(f"https://ymall.jp/search?s9%5B%5D=yamadamobile&s9%5B%5D=ymall&s9o=1&q=%E3%82%A6%E3%83%83%E3%83%89%E3%83%99%E3%83%BC%E3%82%B9&path=MALL2{option}")

def get_item_info(driver):
    result = dict()
    if 'store' in driver.current_url:
        result["item_id"] = driver.current_url.split("/")[-2]
        result["name"] = driver.find_element(By.ID,'shop_cart_name').text
        result["url"] = driver.current_url
        result["price"] = driver.find_element(By.CLASS_NAME,'shop_cart_price_p').text
        try:
            result["description"] = driver.find_element(By.CLASS_NAME,'cart_detail1_left_free').text
        except:
            result["description"] = driver.find_element(By.CLASS_NAME,'cart_detail5_right_free').text.split('【商品説明】')[-1]
    elif 'kaden' in driver.current_url:
        result["item_id"] = driver.current_url.split("/")[-2]
        result["name"] = driver.find_element(By.CSS_SELECTOR,'.item-name.set').text
        result["url"] = driver.current_url
        result["price"] = driver.find_element(By.CSS_SELECTOR, '.highlight.x-large').text
        result["description"] = driver.find_element(By.CSS_SELECTOR, '.item-list-vertical.line').text.split('【商品詳細】')[-1]
    return result

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        update_page(driver, 1)
        time.sleep(SLEEP_TIME)
        page_num = get_total_page_num(driver)
        
        item_urls = list()
        for i_page_num in range(2, page_num+1):
            item_urls.extend(get_item_urls(driver))
            update_page(driver, i_page_num)
            time.sleep(SLEEP_TIME)

        results = list()
        for i_url in item_urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            results.append(get_item_info(driver))
        
        # CSVへ出力
        pd.DataFrame(results).to_csv(CSV_NAME, index=False)

    finally:
        driver.quit()