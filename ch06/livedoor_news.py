# -*- coding: utf-8 -*-

"""
ライブドアニュースを取得
"""
import os
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
SLEEP_TIME = 10
FILE_DIR = "output"
CSV_NAME = "./output/livedoor.csv"

def get_data(driver):
    result = dict()
    result["url"] = driver.current_url
    result["id"] = driver.current_url.split("/")[-2]
    result["title"] = driver.find_element(By.CLASS_NAME, "articleTtl").text
    result["date"] = driver.find_element(By.CLASS_NAME, "articleDate").text
    result["vender"] = driver.find_element(By.CLASS_NAME, "articleVender").text
    result["file_name"] = f"livedoor_{result['id']}.txt"
    
    article_text = str()
    while True:
        i_article_text = driver.find_element(By.CLASS_NAME, "articleBody").text        
        article_text = article_text + "\n" + i_article_text
        pager_elements = driver.find_elements(By.CLASS_NAME, "next")
        if pager_elements:
            next_li_element = pager_elements[0].find_elements(By.CLASS_NAME, "next")
            if next_li_element:
                next_url = next_li_element.find_element(By.TAG_NAME, "a").click()
                time.sleep(SLEEP_TIME)
            else:
                break
        else:
            break

    file_path = os.path.join(FILE_DIR, result["file_name"])
    with open(file_path, "w") as f:
        f.write(article_text)
    return result

def get_news_url(driver):
    a_elements = driver.find_elements(By.CLASS_NAME, "rewrite_ab")
    return [i.get_attribute("href") for i in a_elements]

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if not os.path.exists(FILE_DIR):
            os.makedirs(FILE_DIR)

        target_url = "https://news.livedoor.com/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        article_urls = list()

        urls = get_news_url(driver)
        # データの量を減らす
        urls = urls[:4]
        article_urls.extend(urls)
        article_urls = set([i.replace("topics", "article") for i in article_urls])

        results = list()
        for i_url in article_urls:
            print(i_url)
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            results.append(get_data(driver))
        pd.DataFrame(results).to_csv(CSV_NAME, index=False)

    finally:
        driver.quit()