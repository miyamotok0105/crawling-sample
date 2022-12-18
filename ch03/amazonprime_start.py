# -*- coding: utf-8 -*-

"""
Amazonプライムビデオ配信予定作品の情報を取得する
"""
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
CSV_NAME = "output/amazonprime_start.csv"

def calender_update(driver):
    driver.execute_script("window.scrollBy(0, 600);")
    driver.find_element(By.CLASS_NAME, "next").click()

def get_info(driver):
    results = list()
    day_elements = driver.find_elements(By.CLASS_NAME, "day-column")
    for i_day in day_elements:
        day_data = i_day.get_attribute("data-date")
        content_elements = i_day.find_elements(By.CSS_SELECTOR, ".event.upcoming")
        for i_content in content_elements:
            content_result = dict()
            content_result["day"] = day_data
            content_result["title"] = i_content.find_element(By.CLASS_NAME, "content-title").text
            content_result["url"] = i_content.find_element(By.CLASS_NAME, "content-title").get_attribute("href")
            results.append(content_result)
            print(content_result["title"])
    return results

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://animephilia.net/amazon-prime-video-arrival-calendar/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        results = list()
        for i in range(3):
            results.extend(get_info(driver))
            calender_update(driver)
            time.sleep(SLEEP_TIME)

        pd.DataFrame(results).to_csv(CSV_NAME)
        print(pd.DataFrame(results))

    finally:
        driver.quit()
