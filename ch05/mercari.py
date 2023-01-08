# -*- coding: utf-8 -*-

"""
メルカリのデータを取得する
"""
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs 
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
    
def update_page_num(driver, page_num):
    page_option = f"&page_token=v1%3A{page_num}"
    driver.get(target_url + page_option)

def get_item_urls(driver):
    a_tag_elements = driver.find_elements(By.TAG_NAME, "a")
    if len(a_tag_elements)==0:
        return list()
    hrefs = [i.get_attribute("href") for i in a_tag_elements]
    item_urls = [i for i in hrefs if "item" in i]
    return item_urls

def get_item_info(driver):
    result = dict()
    driver.save_screenshot('screenie.png')
    result["id"] = driver.current_url.split("/")[-1]
    result["datetime"] = datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S')
    result["description"] = driver.find_element(By.CSS_SELECTOR, "pre").text
    result["title"] = driver.find_element(By.TAG_NAME, 'h1').text
    result["price"] = driver.find_element(By.CSS_SELECTOR, ".span.number").text
    return result
    
if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://jp.mercari.com/search?keyword=novation&t1_category_id=1328&status=on_sale&category_id=79"
        driver.get(target_url)   
        time.sleep(5)

        page_num=0
        item_urls = list()
        while True:
            urls = get_item_urls(driver)
            time.sleep(SLEEP_TIME)
            if len(urls) < 1: # 最終ページ
                break
            else:
                item_urls.extend(urls)
                page_num+=1
                update_page_num(driver, page_num)

        item_infos = list()
        for i_url in item_urls:
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))

    finally:
        pass
        driver.quit()