import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 3
CSV_NAME = "yahoo_it.csv"
DATA_DIR = "yahoo_it"

def get_item_urls(driver):
    a_elements = driver.find_elements(By.CLASS_NAME, "newsFeed_item_link")
    puckup_page_urls = [i.get_attribute("href") for i in a_elements]
    results = list()
    for i_url in puckup_page_urls:
        driver.get(i_url)
        time.sleep(SLEEP_TIME)
        next_element = driver.find_element(By.CSS_SELECTOR, ".sc-cECzWn.eGAOEA")
        if next_element.text == "記事全文を読む":
            results.append(next_element.get_attribute("href"))
    return results

def get_item_info(driver):
    result = dict()

    result["id"]= driver.current_url.split("/")[-1]
    if len(driver.find_elements(By.CLASS_NAME, "sc-kasBVs")) > 0:
        result["company_name"] = driver.find_elements(By.CLASS_NAME, "sc-kasBVs")[0].text
    if len(driver.find_elements(By.CLASS_NAME, "sc-hIVACf")) > 0:
        result["post_time"] = driver.find_elements(By.CLASS_NAME, "sc-hIVACf")[0].text
    if len(driver.find_elements(By.CLASS_NAME, "sc-likbZx")) > 0:
        result["title"] = driver.find_elements(By.CLASS_NAME, "sc-likbZx")[0].text
    result["url"] = driver.current_url
    return result

if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        target_url = "https://news.yahoo.co.jp/topics/it"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        urls = get_item_urls(driver)

        result = list()
        for i_url in urls:
            print(i_url)
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            result.append(get_item_info(driver))

        pd.DataFrame(result).to_csv(CSV_NAME)

    finally:
        driver.quit()