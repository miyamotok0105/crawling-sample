# -*- coding: utf-8 -*-

"""
インスタグラマーのランキングのデータを取得する
"""
import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
CSV_NAME = "output/insta_ranking.csv"

def update_page_num(driver, page_num):
    url = f"https://insta.refetter.com/ranking/?p={page_num}"
    driver.get(url)

def get_urls(driver):
    result = list()
    table_elements = driver.find_elements(By.TAG_NAME, "table")
    for i_table in table_elements:
        photo_elements = i_table.find_elements(By.CLASS_NAME, "photo")
        urls = [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in photo_elements]
        print(urls)
        result.extend(urls)   
    return result

def get_user_info(driver):
    table_data = driver.find_element(By.CSS_SELECTOR, "#person > section.basic > div.basic")
    dt_elements = table_data.find_elements(By.TAG_NAME, "dt")
    keys = [i.text for i in dt_elements]
    dd_elements = table_data.find_elements(By.TAG_NAME, "dd")
    values = [i.text for i in dd_elements]
    result = {k:v for k,v in zip(keys, values)}

    bc_element = driver.find_element(By.CLASS_NAME, "breadcrumb")
    result["ユーザー名"] =  bc_element.find_elements(By.TAG_NAME, "li")[-1].text
    result["ランキングURL"] = driver.current_url
    if len(result) <= 4: # 消去済み垢はここでストップ
        return result
    a_element = driver.find_element(By.CLASS_NAME, "fullname").find_element(By.TAG_NAME, "a")
    result["インスタURL"] = a_element.get_attribute("href")
    result["取得日時"] = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M')

    print(result)
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        user_urls = list()
        for i_page_num in range(1, 2):
            update_page_num(driver, i_page_num)
            time.sleep(SLEEP_TIME)
            user_urls.extend(get_urls(driver))
        print("="*100)
        result = list()
        for i_url in user_urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_user_info(driver))
        pd.DataFrame.to_csv(CSV_NAME)
    finally:
        driver.quit()
