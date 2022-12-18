# -*- coding: utf-8 -*-

"""
Youtuberのランキングのデータを取得する
"""
import time
import datetime
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
CSV_NAME = "output/youtube_ranking.csv"

def update_page(driver, page_num):
    url = f"https://youtube-ranking.userlocal.jp/?page={page_num}"
    driver.get(url)

def get_urls(driver):
    table_element = driver.find_element(By.TAG_NAME, "tbody")
    tr_elements = table_element.find_elements(By.TAG_NAME, "tr")
    return [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in tr_elements]

def get_info(driver):
    result = dict()
    result["name"] = driver.find_element(By.TAG_NAME, "h6").text
    result["rank_url"] = driver.current_url
    result["youtube_url"] = driver.find_element(By.CSS_SELECTOR, "h6 > a").get_attribute("href")
    result["start_date"] = driver.find_element(By.CSS_SELECTOR, "div.card-body.pt-0 > div").text
    result["discribe"] = driver.find_element(By.CSS_SELECTOR, "div.card-body.pt-0 > p").text
    result["subscriber_count"] = driver.find_element(By.CSS_SELECTOR, "div.card-body.px-3.py-5 > div.d-inline-block").text
    result["views"] = driver.find_element(By.CSS_SELECTOR, "div.card.mt-2 > div > div.d-inline-block").text
    return result

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        urls = list()
        for i_page in range(1, 3):    
            update_page(driver, i_page)
            time.sleep(SLEEP_TIME)
            urls.extend(get_urls(driver))
        
        results = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            results.append(get_info(driver))

        pd.DataFrame(results).to_csv(CSV_NAME)
    finally:
        driver.quit()
