# -*- coding: utf-8 -*-

"""
yahooショッピングのデータを取得する
"""
import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

def update_page_num(driver, page_num):
    page_option = f"?page={page_num}"
    driver.get(target_url + page_option)

def get_item_urls(driver):
    tr_elements = driver.find_elements(By.CLASS_NAME, "elNameLink")
    item_urls = [i.get_attribute("href") for i in tr_elements]
    return item_urls

def get_item_info(driver):
    result = Yahoo_item_info()

    # id
    result.id = driver.current_url.split("/")[-1]
    # datetime
    now = datetime.datetime.now()
    result.datetime = now.strftime('%y/%m/%d %H:%M:%S')
    # title
    element = driver.find_element(By.CLASS_NAME, "mdItemName")
    title_element = element.find_element(By.CLASS_NAME, "elName")
    result.title = title_element.text
    # price
    price_number_element = driver.find_element(By.CLASS_NAME, "elPriceNumber")
    price_unit_element = driver.find_element(By.CLASS_NAME, "elPriceUnit")
    result.price = str(price_number_element.text + price_unit_element.text)
    # description
    description_element = driver.find_element(By.CLASS_NAME, "mdItemDescription")
    result.description = description_element.text
    # stock
    element_table = driver.find_element(By.CLASS_NAME, "elTableInner")
    html = element_table.get_attribute('outerHTML')
    result.stock = pd.read_html(html)
    # images 
    image_elements= driver.find_elements(By.CLASS_NAME, "elPanelImage")
    result.image_urls = list(set([i.get_attribute("src") for i in image_elements]))
    
    # review
    if len(driver.find_elements(By.CLASS_NAME, "elReviewValue")) > 0:
        review_element = driver.find_element(By.CLASS_NAME, "elReviewValue")
        result.review = review_element.text
    
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # In The City -> トップス
        target_url = "https://store.shopping.yahoo.co.jp/ryouhin-boueki/a5c8a5c3a5.html"
        driver.get(target_url)

        page_num=0
        item_urls = list()
        while True:
            time.sleep(5)
            urls = get_item_urls(driver)
            if len(urls) < 1:
                break
            else:
                item_urls.extend(urls)
                page_num += 1
                update_page_num(driver, page_num)
        
        item_infos = list()
        logger.info("start scrape item info.")
        for i_url in tqdm(item_urls):
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))

    except Exception as e :
        logger.error(e)
    finally:
        driver.quit()
        logger.info('end crawring')