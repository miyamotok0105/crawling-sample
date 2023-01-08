# -*- coding: utf-8 -*-

"""
官報から決算書を取得する
"""
import os
import time
import datetime
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs 
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
CSV_NAME = "kanpo.csv"
DOWNLOAD_DIR =  "output"

def get_vol_url(driver):
    result = list()
    today_element = driver.find_element(By.ID, "todayBox")
    a_elements = today_element.find_elements(By.TAG_NAME, "a")
    today_url = [i.get_attribute("href") for i in a_elements]
    result.append(today_url)

    btn_div_element = driver.find_element(By.CLASS_NAME, "toggleBtn")
    btn_div_element.find_element(By.TAG_NAME, "button").click()
    time.sleep(SLEEP_TIME)

    archive_element = driver.find_element(By.ID, "archiveBox") 
    dl_elements = archive_element.find_elements(By.TAG_NAME, "dl")
    for i_dl in dl_elements:
        a_elements = i_dl.find_elements(By.TAG_NAME, "a")
        result.append([i.get_attribute("href") for i in a_elements])
    return result

def get_pdf_info(driver):
    result = list()
    contents_element = driver.find_element(By.CLASS_NAME, "contentsBox")
    section_elements = contents_element.find_elements(By.TAG_NAME, "section")
    print([i.text for i in section_elements])
    for i_section in section_elements:
        article_element = i_section.find_elements(By.TAG_NAME, "a")
        for i_article in article_element:
            title = i_article.text
            url = i_article.get_attribute("href")
            page_num = i_article.find_element(By.CLASS_NAME, "date").text
            result.append({"title":title, "url":url, "page":page_num})

    return result

def download_pdf(dir, url):
    file_name = url.split("/")[-1]
    file_path = os.path.join(dir, file_name)
    print(file_path)
    content_data = requests.get(url).content
    time.sleep(SLEEP_TIME)
    with open(file_path ,'wb') as f:
        f.write(content_data)

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())    
        target_url = "https://kanpou.npb.go.jp/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
        day_urls = get_vol_url(driver)
     
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)
    
        for i_day in day_urls:
            date = i_day[0].split("/")[-3]
            date_dir = os.path.join(DOWNLOAD_DIR, date)
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)
    
            for i_vol in i_day:
                vol_name = i_vol.split("/")[-2]
                vol_dir = os.path.join(date_dir, vol_name)
                if not os.path.exists(vol_dir):
                    os.makedirs(vol_dir)
    
                driver.get(i_vol)
                time.sleep(SLEEP_TIME)
                
                total_page_num =int(driver.find_element(By.ID, "pageAll").text)
                base_url = "/".join(i_vol.split("/")[:-1])
                for i_num in range(1,total_page_num+1):
                    file_name_num = str(i_num).zfill(4)
                    doc_num = i_vol.split("/")[-2]
                    file_name = f'{doc_num}{file_name_num}.pdf'
                    file_url = os.path.join(base_url, "pdf", file_name)
                    download_pdf(vol_dir, file_url)
    
                if "m" in i_vol.split("/")[-2]:
                    continue # 目録には目次がないため
                article_infos = get_pdf_info(driver)
                file_path = os.path.join(vol_dir, "summary.csv")
                pd.DataFrame(article_infos).to_csv(file_path)
    finally:
        driver.quit()