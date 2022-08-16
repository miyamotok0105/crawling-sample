import time
import requests
import datetime
from tqdm import tqdm
import logging
from logging import config, getLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import configparser
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
import pandas as pd 
import numpy as np

def sleep_rand(min=5):
    rand_num = np.random.normal(10, 1)
    time.sleep(rand_num if rand_num > min else min)

def get_data(driver):
    url = driver.current_url
    id = url.split("/")[-2]
    title = driver.find_element(By.CLASS_NAME, "articleTtl").text
    date = driver.find_element(By.CLASS_NAME, "articleDate").text
    vender = driver.find_element(By.CLASS_NAME, "articleVender").text
    file_name = f"{id}.txt"
    
    # ページ更新
    article_text = str()
    while True:
        i_article_text = driver.find_element(By.CLASS_NAME, "articleBody").text        
        article_text = article_text + i_article_text
        pager_elements = driver.find_elements(By.CLASS_NAME, "pager")
        if pager_elements:
            next_li_element = pager_elements.find_element(By.CLASS_NAME, "next")
            next_a_element = next_li_element.find_element(By.TAG_NAME, "a")
            a.click()
        else:
            break

    with open(file_name, "w") as f:
        f.write(article_text)
    
    
    return {"id": id, "title":title, "url":url, "date":date, "vender":vender, "file_name":file_name}

def get_news_url(driver, class_name):
    """
    """
    top_news_element = driver.find_element(By.CLASS_NAME, class_name)
    a_elements = top_news_element.find_elements(By.TAG_NAME, "a")
    return [i.get_attribute("href") for i in a_elements]

def scraping(user_id):
    """
    入力したユーザーIDのツイートを全て集める

    Returns 
    --------------------------------------
    item_infos:
        商品データを纏めたデータ型のリスト
    """

    try:
        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        fh = logging.FileHandler('spam.log') # logファイルの
        logger.addHandler(fh)

        logger.info("start crawling")
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver",options=chrome_options)
        
        target_url = "https://news.livedoor.com/"
        driver.get(target_url)
        
        sleep_rand()
        
        article_urls = list()

        urls = get_news_url(driver, "topTopicsList")
        article_urls.extend(urls)

        article_urls = [i.replace("topics", "article") for i in article_urls]

        for i_url in article_urls:
            sleep_rand()
            driver.get(i_url)
            print(get_data(driver))
        
    finally:
        driver.save_screenshot("last_screen.png")
        driver.quit()
        logger.info('end crawring')       


if __name__=="__main__":
  scraping("NanashinoSeito")