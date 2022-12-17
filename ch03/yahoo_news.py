import os
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 4
CSV_NAME = "yahoo_news.csv"
FILE_DIR = "yahoo_news"

def get_item_urls(driver):
    a_elements = driver.find_elements(By.CLASS_NAME, "sc-btzYZH")
    pickup_urls = [i.get_attribute("href") for i in a_elements]

    results = list()
    for i_url in pickup_urls:
        driver.get(i_url)
        time.sleep(SLEEP_TIME)
        title_element = driver.find_element(By.CLASS_NAME, "sc-hMapFE")
        results.append(title_element.get_attribute("href"))
    return results

def get_article_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")[-1]
    result["title"] = driver.find_element(By.CSS_SELECTOR, "article > header >h1").text
    result["post_time"] = driver.find_element(By.CSS_SELECTOR, "article > header >div > div > div >p > time").text
    result["file_name"] = f"{result['id']}.txt"

    content = str()
    while True:
        content = content + driver.find_element(By.CLASS_NAME, "article_body").text   
        if len(driver.find_elements(By.CLASS_NAME, "pagination_items")) > 0:
                if "次" in driver.find_element(By.CLASS_NAME, "pagination_items").text:
                    button_element = driver.find_element(By.CSS_SELECTOR, ".pagination_item.pagination_item-next")
                    if "pagination_item-disabled" in button_element.get_attribute("class"):
                        button_element.click()
                        time.sleep(SLEEP_TIME)
                    else: break
                else: break
        else: break

    file_path = os.path.join(FILE_DIR, result["file_name"])
    with open(file_path, "w") as f:
        f.write(content)
    return result

def get_byline_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")[-1]
    result["title"] = driver.find_element(By.CSS_SELECTOR, "article > div > header > h1").text
    result["post_time"] = driver.find_element(By.CSS_SELECTOR, "article > div > header > div > div  > div > time").text
    result["file_name"] = f"{result['id']}.txt"

    file_path = os.path.join(FILE_DIR, result["file_name"])
    with open(file_path, "w") as f:
        f.write(driver.find_element(By.CLASS_NAME, "articleBody").text)
    return result

if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        if not os.path.exists(FILE_DIR):
            os.makedirs(FILE_DIR)

        target_url = "https://news.yahoo.co.jp/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        article_urls = get_item_urls(driver)
    
        result = list()
        for i_url in article_urls:
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