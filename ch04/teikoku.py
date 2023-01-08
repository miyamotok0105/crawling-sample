# -*- coding: utf-8 -*-

"""
帝国データバンクから倒産情報取得する
"""
import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
CSV_NAME = "teikoku.csv"
DATA_DIR = "output"

def get_item_urls(driver):    
    content_element = driver.find_element(By.CLASS_NAME, 'contentsList')
    a_elements = content_element.find_elements(By.TAG_NAME, 'a')
    return [i.get_attribute("href") for i in a_elements]

def get_company_info(driver):
    result = dict()
    result["url"] = driver.current_url
    result["id"] = driver.current_url.split("/")[-1].replace(".html", "")
    article = driver.find_element(By.ID, 'article')
    result["title"] = article.find_element(By.TAG_NAME, 'h1').text
    result["date"] = driver.find_element(By.CLASS_NAME, 'articleDate').text
    company_summary = driver.find_element(By.CLASS_NAME, 'companySummary')
    result["abstract"] = company_summary.find_element(By.TAG_NAME, 'p').text.split("TDB企業コード:")[0]
    result["tdb_code"] = company_summary.find_element(By.TAG_NAME, 'p').text.split("TDB企業コード:")[-1]
    liabilities_elements = driver.find_elements(By.CLASS_NAME, 'liabilities')
    result["liabilities"] = liabilities_elements[0].text if len(liabilities_elements) > 0 else ""

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    result["file_name"] = f'{result["id"]}.txt'
    file_dir = os.path.join(DATA_DIR, result["file_name"])
    with open(file_dir, "w")as f:
        f.write(driver.find_element(By.CLASS_NAME, 'articleTxt').text)
    return result

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://www.tdb.co.jp/tosan/syosai/index.html"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
        urls = get_item_urls(driver)

        result = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_company_info(driver))

        pd.DataFrame(result).to_csv(CSV_NAME, index=False)
    finally:
        driver.quit()