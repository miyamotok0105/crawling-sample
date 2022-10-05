import os
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 10
FILE_DIR = "livedoor"

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
        pager_elements = driver.find_elements(By.CLASS_NAME, "pager")
        if pager_elements:
            next_li_element = pager_elements[0].find_element(By.CLASS_NAME, "next")
            next_url = next_li_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            driver.get(next_url)
            time.sleep(SLEEP_TIME)
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
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        
        if not os.path.exists(FILE_DIR):
            os.makedirs(FILE_DIR)

        target_url = "https://news.livedoor.com/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        article_urls = list()

        urls = get_news_url(driver)
        article_urls.extend(urls)
        article_urls = set([i.replace("topics", "article") for i in article_urls])

        results = list()
        for i_url in article_urls:
            print(i_url)
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            results.append(get_data(driver))
        
    finally:
        driver.quit()