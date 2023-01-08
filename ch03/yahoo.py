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

SLEEP_TIME = 3
CSV_NAME = "./output/yahoo.csv"

def display_all_item(driver):
    start_html = driver.page_source
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_TIME)
        if driver.page_source == start_html:
            break
        else:
            start_html = driver.page_source

def get_item_urls(driver):
    li_elements = driver.find_elements(By.CLASS_NAME, "LoopList__item")
    a_elements = [i.find_element(By.TAG_NAME, "a") for i in li_elements]
    return [i.get_attribute("href") for i in a_elements]

def get_item_info(driver):
    result = dict()
    result["site"] = "yahoo"
    result["url"] = driver.current_url
    # id
    result["id"] = driver.current_url.split("/")[-1]
    # title
    md_element = driver.find_element(By.CLASS_NAME, "mdItemName")
    result["title"]  = md_element.find_element(By.CLASS_NAME, "elName").text
    # price
    price_number_element = driver.find_element(By.CLASS_NAME, "elPriceNumber")
    result["price"] = price_number_element.text
    # description
    description_element = driver.find_element(By.CLASS_NAME, "mdItemDescription")
    result["description"] = description_element.text
    
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://shopping.yahoo.co.jp/search?p=novation+mininova"
        driver.get(target_url)

        display_all_item(driver)
        item_urls = get_item_urls(driver)

        item_infos = list()
        for i_url in item_urls:
            print(i_url)
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))

        pd.DataFrame(item_infos).to_csv(CSV_NAME, index=False)

    except Exception as e :
        print(e)
    finally:
        driver.quit()