# -*- coding: utf-8 -*-

"""
日経新聞のデータを取得する
"""
import os
import time
import json 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

CSV_NAME = "./output/nikkei.csv"
FILE_DIR = "./output"
SLEEP_TIME = 3

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = f"https://www.nikkei.com/"
        driver.get(base_url)
        time.sleep(SLEEP_TIME)

        head_line = driver.find_elements(By.TAG_NAME, "article")
        json_infos = [i.get_attribute("data-k2-headline-article-data") for i in head_line]
        json_infos = [i for i in json_infos if bool(i)]
        print(json_infos)

        results = list()
        for i_json in json_infos:
            item_info = dict()
            json_data = json.loads(i_json)
            item_info["id"] = json_data['id']
            item_info["url"] = f"https://www.nikkei.com/article/{json_data['id']}"
            item_info["title"] = json_data["title"]
            
            driver.get(item_info["url"])
            time.sleep(SLEEP_TIME)
            article_element = driver.find_element(By.TAG_NAME, "article")
            header_element = article_element.find_element(By.TAG_NAME, "header")
            item_info["title"] = header_element.find_element(By.TAG_NAME, "h1").text
            item_info["time"] = header_element.find_element(By.TAG_NAME, "time").text
            
            with open(os.path.join(FILE_DIR, f"{item_info['id']}.txt"), "w") as f:
                article_text = driver.find_element(By.TAG_NAME, "section").text
                f.write(article_text)

            results.append(item_info)
        
        pd.DataFrame(results).to_csv(CSV_NAME, index=False)

    finally:
        driver.quit()
