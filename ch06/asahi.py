# -*- coding: utf-8 -*-

"""
朝日新聞のデータを取得する
"""
import os
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
CSV_NAME = "output/asahi.csv"

def get_news_url(driver, css_selector):
    first_headline = driver.find_element(By.CSS_SELECTOR, css_selector)
    a_elements = first_headline.find_elements(By.TAG_NAME, "a")
    urls = [i.get_attribute("href") for i in a_elements]
    return [i for i in urls if "articles" in i]

def get_article_info(driver):
    result = dict()
    html_name = driver.current_url.split("/")[-1]
    result["id"] = html_name.split("?")[0].replace(".html", "")
    result["url"] = driver.current_url
    result["title"] = driver.find_element(By.CSS_SELECTOR, "main > div > h1").text
    result["article_text"] = driver.find_element(By.CLASS_NAME, "nfyQp").text
    
    result["writer"] = driver.find_element(By.CSS_SELECTOR, "main > div > div > span").text

    return result

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://www.asahi.com/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        news_urls = list()
        news_urls.extend(get_news_url(driver, ".l-section.p-topNews"))
        news_urls.extend(get_news_url(driver, ".p-topNews2.p-topNews2__list.p-topNews__list"))
        # データの量を減らす
        news_urls = news_urls[:6]

        result = list()
        for i_url in news_urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_article_info(driver))
        pd.DataFrame(result).to_csv(CSV_NAME, index=False)

    finally:
        driver.quit()