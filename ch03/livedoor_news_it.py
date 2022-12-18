# -*- coding: utf-8 -*-

"""
ライブドアニュース(IT)のデータを取得する
"""
import os
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

PAGE_NUM = 3
SLEEP_TIME = 3
CSV_NAME = "livedoor_it.csv"
FILE_DIR = "livedoor_it"

def get_article_url(driver):
    article_list_element = driver.find_element(By.CLASS_NAME, "articleList")
    a_elements = article_list_element.find_elements(By.TAG_NAME, "a")
    print([i.get_attribute("href") for i in a_elements])
    return [i.get_attribute("href") for i in a_elements]

def get_data(driver):
    result = dict()
    result["url"] = driver.current_url
    result["id"] = driver.current_url.split("/")[-2]
    result["title"] = driver.find_element(By.CLASS_NAME, "articleTtl").text
    result["date"] = driver.find_element(By.CLASS_NAME, "articleDate").text
    result["vender"] = driver.find_element(By.CLASS_NAME, "articleVender").text
    result["file_name"] = f"{result['id']}.txt"
    
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

if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        if not os.path.exists(FILE_DIR):
            os.makedirs(FILE_DIR)

        urls = list()
        for i_pagenum in range(1, PAGE_NUM+1):
            url = f"https://news.livedoor.com/article/category/210/?p={i_pagenum}"
            driver.get(url)
            time.sleep(SLEEP_TIME)
            urls.extend(get_article_url(driver))       
        
        urls = [i.replace("topics", "article") for i in urls]
        article_infos = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            article_infos.append(get_data(driver))

        pd.DataFrame(article_infos).to_csv(CSV_NAME)

    finally:
        driver.quit()