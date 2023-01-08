# -*- coding: utf-8 -*-

"""
読売新聞のデータを取得する
"""

import time
import datetime
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 2
today = datetime.datetime.now().strftime('%y:%m:%d:%H:%M:%S')
CSV_NAME = f"output/yomiuri_{today}.csv"

if __name__=="__main__":
    try:
        target_url = "https://www.yomiuri.co.jp/"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        headline_element = driver.find_element(By.CLASS_NAME, "headline")
        article_elements = headline_element.find_elements(By.TAG_NAME, "article")
        title_elements = [i.find_element(By.TAG_NAME, "h3") for i in article_elements]
        titles = [i.text for i in title_elements]
        urls = [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in title_elements]

        with open(CSV_NAME, "a") as f:
            for i_title, i_url in zip(titles, urls):
                f.write(f"{i_title},{i_url}\n")
    finally:
        driver.quit()
