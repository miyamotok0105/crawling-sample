# -*- coding: utf-8 -*-

"""
yahooニュース(IT)のデータを取得する
"""
import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
CSV_NAME = "yahoo_it.csv"
FILE_DIR = "output"

def get_item_urls(driver):
    a_elements = driver.find_elements(By.CLASS_NAME, "newsFeed_item_link")
    pickup_urls = [i.get_attribute("href") for i in a_elements]
    results = list()

    results = list()
    for i_url in pickup_urls:
        driver.get(i_url)
        time.sleep(SLEEP_TIME)
        article_element = driver.find_element(By.ID, "uamods-pickup")
        urls = [i.get_attribute("href") for i in article_element.find_elements(By.TAG_NAME, "a")]
        results.append(urls[0])
    print(results)
    return [i.replace("/images/000", "") for i in results]

def get_article_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")[-1]
    article_element = driver.find_element(By.TAG_NAME, "article")
    result["title"] = driver.find_element(By.TAG_NAME, "h1").text
    result["post_time"] = driver.find_element(By.TAG_NAME, "time").text
    result["file_name"] = f"{result['id']}.txt"

    content = str()
    while True:
        content = content + driver.find_element(By.CLASS_NAME, "article_body").text   
        if len(driver.find_elements(By.CLASS_NAME, "pagination_items")) > 0:
                if "次" in driver.find_element(By.CLASS_NAME, "pagination_items").text:
                    button_element = driver.find_element(By.CSS_SELECTOR, ".pagination_item.pagination_item-next")
                    if "pagination_item-disabled" in button_element.get_attribute("class"):
                        button_element.click()
                    else:
                        break
                    time.sleep(SLEEP_TIME)
                else:
                    break
        else:
            break

    file_path = os.path.join(FILE_DIR, result["file_name"])
    with open(file_path, "w") as f:
        f.write(content)
    return result


def get_byline_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")[-1]
    article_element = driver.find_element(By.TAG_NAME, "article")
    result["title"] = driver.find_element(By.TAG_NAME, "h1").text
    result["post_time"] = driver.find_element(By.TAG_NAME, "time").text
    result["file_name"] = f"{result['id']}.txt"

    file_path = os.path.join(FILE_DIR, result["file_name"])
    with open(file_path, "w") as f:
        f.write(driver.find_element(By.CLASS_NAME, "articleBody").text)
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())

        target_url = "https://news.yahoo.co.jp/topics/it"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
        urls = get_item_urls(driver)

        result = list()
        for i_url in urls:
            print(i_url)
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            if "article" in i_url:
                result.append(get_article_info(driver))
            elif "byline" in i_url:
                result.append(get_byline_info(driver))
    
        pd.DataFrame(result).to_csv(CSV_NAME)

    finally:
        driver.quit()