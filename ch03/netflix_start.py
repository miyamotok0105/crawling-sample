# -*- coding: utf-8 -*-

"""
Netflix配信予定作品の情報を取得する
"""
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 10
CSV_NAME = "output/netflix_start.csv"

def get_info(driver):
    results = list()
    day_elements = driver.find_elements(By.CLASS_NAME, "date-cc")
    for i_day in day_elements:
        date = i_day.find_element(By.CLASS_NAME, "newtoto2").text
        contens_elements = i_day.find_elements(By.CSS_SELECTOR, "div.mark89 > div")
        for i_content in contens_elements:
            content_result = dict()
            content_result["date"] = date
            title_element = i_content.find_element(By.CLASS_NAME, "sche-npp-txt")
            content_result["title"] = title_element.text
            content_result["url"] = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            content_result["season"] = i_content.find_element(By.CLASS_NAME, "sche-npp-seas").text
            content_result["genre"] = i_content.find_element(By.CLASS_NAME, "sche-npp-gen").text
            results.append(content_result)
    return results

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        #target_url = "https://www.net-frx.com/p/netflix-coming-soon.html"
        target_url = "https://www.net-frx.com/p/netflix-expiring.html"

        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        result = get_info(driver)

        pd.DataFrame(result).to_csv(CSV_NAME,index=False)
    
    finally:
        driver.quit()
