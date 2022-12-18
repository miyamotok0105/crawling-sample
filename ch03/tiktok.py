# -*- coding: utf-8 -*-

"""
TikTok情報を取得する
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
SCROLL_NUM = 5
CSV_NAME = "output/tiktok.csv"

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://www.tiktok.com/@tv_asahi_news"
        driver.get(base_url)        
        time.sleep(SLEEP_TIME)

        for _ in range(SCROLL_NUM): 
            time.sleep(SLEEP_TIME)
            driver.execute_script("window.scrollBy(0, 6000);")

        prosuct_elements = driver.find_elements(By.CSS_SELECTOR, ".tiktok-x6y88p-DivItemContainerV2.e19c29qe7")

        results = list()
        for i_section in prosuct_elements:
            result_row = dict()
            a_element = i_section.find_element(By.CSS_SELECTOR, "div > div > div > a")
            result_row["url"] = a_element.get_attribute("href")
            img_element = i_section.find_element(By.CSS_SELECTOR, "div > div > div > a > div > div > img")
            result_row["name"] = img_element.get_attribute("alt")
            results.append(result_row)

        pd.DataFrame(results).to_csv(CSV_NAME)
    finally:
        driver.quit()
