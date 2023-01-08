# -*- coding: utf-8 -*-

"""
PRTIMESのから資金調達データを取得する
"""
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

ARTICLE_DATA_DIR = "output"
CSV_NAME = "prtimes_funding.csv"
SLEEP_TIME = 3
PAGE_NUM = 10

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = f"https://prtimes.jp/topics/keywords/%E8%B3%87%E9%87%91%E8%AA%BF%E9%81%94"
        driver.get(base_url)
        time.sleep(SLEEP_TIME)
        if not os.path.exists(ARTICLE_DATA_DIR):
            os.makedirs(ARTICLE_DATA_DIR)
        
        for i_pagenum in range(PAGE_NUM-1):
            button_element = driver.find_element(By.CSS_SELECTOR, ".button.button-read-more.icon.icon-read-more")
            button_element.click()
            time.sleep(SLEEP_TIME)

        page_urls = [i.get_attribute("href") for i in driver.find_elements(By.CSS_SELECTOR, ".link-title-item.link-title-item-ordinary.thumbnail-title")]
        print(page_urls)

        results = list()
        for i_url in page_urls:
            row_result = dict()
            driver.get(i_url)
            time.sleep(5)
            
            row_result["id"] = os.path.splitext(i_url.split("/")[-1])[0]
            row_result["url"] = i_url
            row_result["title"] = driver.find_element(By.CLASS_NAME, "release--title").text
            row_result["company"] = driver.find_element(By.CLASS_NAME, "company-name").text
            row_result["datetime"] = driver.find_element(By.TAG_NAME, "time").text
            row_result["abstruct"] = driver.find_element(By.CLASS_NAME, "r-head").text

            results.append(row_result)
            article_path = os.path.join(ARTICLE_DATA_DIR, f"{row_result['id']}.txt")
            with open(article_path, "w") as f:
                main_text = driver.find_element(By.CLASS_NAME, "rich-text").text
                f.write(main_text)
            
            print(row_result)
    finally:
        driver.quit()

    df = pd.DataFrame(results)
    df.to_csv(CSV_NAME)