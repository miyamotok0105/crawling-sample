# -*- coding: utf-8 -*-

"""
東京商工リサーチから倒産情報取得する
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
DATA_DIR = "output"
CSV_NAME = "tokyosyoko.csv"

def get_monthly_urls(driver):
    a_elements= list()
    ul_elements = driver.find_elements(By.CLASS_NAME, 'month')
    for i_ul in ul_elements:
        a_elements.extend(i_ul.find_elements(By.TAG_NAME, "a"))
    return [i.get_attribute("href") for i in a_elements]

def open_all_tab(driver):
    button_elements = driver.find_elements(By.CSS_SELECTOR, '.profile.equalHeight')
    for i_button in button_elements[1:]:
        i_button.click()
        time.sleep(SLEEP_TIME)

def get_company_info(driver):
    result = list()
    yyyymm = driver.current_url.split('/')[-1].replace(".html", "")

    info_elements = driver.find_elements(By.CSS_SELECTOR, ".profile.equalHeight")
    detail_elements = driver.find_elements(By.CLASS_NAME, "detail")

    for i_info, i_detail in zip(info_elements, detail_elements):
        row_result = dict()
        row_result["yyyymm"] = yyyymm
        row_result["name"] = i_info.find_element(By.CLASS_NAME, 'name').text
        row_result["type"] = i_info.find_element(By.CLASS_NAME, 'type').text
        row_result["debt"] = i_info.find_element(By.CLASS_NAME, 'debt').text.split('総額')[-1]
        row_result["url"] = driver.current_url
        row_result["file_name"] = f'{row_result["name"]}.txt'
        result.append(row_result)
        file_path = os.path.join(DATA_DIR, row_result["file_name"])
        with open(file_path, "w") as f:
            f.write(i_detail.text)

    return result

if __name__ == '__main__':
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        url = 'https://www.tsr-net.co.jp/news/process/index.html'
        driver.get(url)
        time.sleep(SLEEP_TIME)

        urls = get_monthly_urls(driver)
        result = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            open_all_tab(driver)
            result.extend(get_company_info(driver))
        pd.DataFrame(result).to_csv(CSV_NAME)
    finally:
        driver.quit()
