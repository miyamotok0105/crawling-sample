# -*- coding: utf-8 -*-

"""
AU Payマーケットのデータを取得する
"""
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

CSV_NAME  = "output/aupay_market.csv"
SLEEP_TIME = 2

def get_item_urls(driver,page_num):
    product_elements = driver.find_elements(By.CLASS_NAME, 'productItem')
    return [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in product_elements]

def get_item_info(driver):
    result = dict()
    table_element = driver.find_element(By.CLASS_NAME, 'pb20')
    result["name"] = table_element.find_element(By.CLASS_NAME, 'name').text
    result["url"] = driver.current_url    
    result["id"] = driver.current_url.split("/")[-1]
    result["price"] = driver.find_element(By.ID, 'js-baseItemPrice').text
    result["datetime"] =  datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
    
    try:
        result["discribe"] = driver.find_element(By.ID, 'itemSuperDetailAra').text
    except:
        desc_table = driver.find_element(By.CLASS_NAME, 'fixedWidth')
        result["discribe"] = desc_table.find_element(By.CLASS_NAME, 'inner').text

    print(result)
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://wowma.jp/itemlist?e_scope=O&at=FP&non_gr=ex&spe_id=c_act_sc03&e=tsrc_topa_m&ipp=40&keyword=%83%7D%83%8A%83I%83X%83g%83%89%83C%83J%81%5B%83Y&clk=1"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
        product_num = int(driver.find_element(By.CLASS_NAME,'-headingSeachCount--headingSeachCount--1lTdy-')
                                .find_element(By.TAG_NAME, 'span')
                                .text)
    
        display_num = len(driver.find_elements(By.CLASS_NAME, "productItem"))
        page_num = product_num // display_num
        
        urls = list()
        for i_page_num in range(1, page_num+1):
            next_url = target_url + f"&page={i_page_num}"
            driver.get(next_url)
            time.sleep(SLEEP_TIME)
            urls.extend(get_item_urls(driver,page_num))
        
        print(urls)
    
        result = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_item_info(driver))
        
        df = pd.DataFrame(result)
        df.to_csv(CSV_NAME, encoding='utf_8_sig')
    finally:
        driver.quit()