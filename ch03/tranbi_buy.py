# -*- coding: utf-8 -*-

"""
M&A案件一覧を取得する（事業を買う）
"""
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs 

SLEEP_TIME = 3
GET_PAGE_NUM = 1
CSV_NAME = "./output/tranbi_buy.csv"

def update_page_num(driver, page_num):
    base_url = "https://www.tranbi.com/buy/list/?prill=&priul=&srl=&sru=&proll=&proul=&ft=&page_size=120&per-page=120"
    url = base_url + f"&page={page_num}"
    driver.get(url)

def get_project_url(driver):
    project_list_element = driver.find_element(By.CSS_SELECTOR, ".buylistArea.js-toggle-bookmark-area")
    a_elements = project_list_element.find_elements(By.TAG_NAME, "a") 
    hrefs = [i.get_attribute("href") for i in a_elements]
    return [ i for i in hrefs if "detail" in i ]

def get_info(driver):
    result = dict()
    result["title"] = driver.find_element(By.CLASS_NAME, "nwBuyDetail__tagList").text
    result["genre"] = driver.find_element(By.CLASS_NAME, "nwBuyDetail__title").text
    result["date"] = driver.find_element(By.CLASS_NAME, "nwBuyDetail__dateInfo").text

    project_info = driver.find_element(By.CLASS_NAME, "nwBuyDetail__detailList")
    table_info = project_info.find_elements(By.CLASS_NAME, "nwBuyDetail__detailItemBody")
    result["sales_amount"] = table_info[0].text
    result["income"] = table_info[1].text
    result["place"] = table_info[2].text
    result["employee"] = table_info[3].text

    result["price"] = driver.find_element(By.CLASS_NAME, "nwBuyDetail__buyCost")
    
    table_info = driver.find_elements(By.CLASS_NAME, "definitionItemType2__body")
    result["seles_subject"] = table_info[0].text
    result["fiscal_year"] = table_info[1].text

    return result

def get_detail_info(driver):
    table_data = driver.find_elements(By.CSS_SELECTOR, ".list2column.flex")[0]
    li_elements = table_data.find_elements(By.TAG_NAME, "li")
    keys = [i.text for i in li_elements[::2]]
    values = [i.text for i in li_elements[1::2]]
    result = [(k,v) for k,v in zip(keys, values)]
    print("案件概要")
    print(result)

    # ビジネスモデル
    table_data = driver.find_elements(By.CSS_SELECTOR, ".list2column.flex")[1]
    li_elements = table_data.find_elements(By.TAG_NAME, "li")
    keys = [i.text for i in li_elements[::2]]
    values = [i.text for i in li_elements[1::2]]
    result = [(k,v) for k,v in zip(keys, values)]
    print("ビジネスモデル")
    print(result)
    
if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
    
        target_url = "https://www.tranbi.com/buy/list/?prill=&priul=&srl=&sru=&proll=&proul=&ft=&page_size=120"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
    
        if GET_PAGE_NUM == None:
            total_num_element = driver.find_element(By.CLASS_NAME, "searchResultCount").text
            page_num = int(total_num_element.replace("件", "").replace(",", "")) // 120 + 1
        else:
            page_num = GET_PAGE_NUM
    
        detail_urls = list()
        for i_page_num in range(1, page_num+1):
            update_page_num(driver, i_page_num)
            time.sleep(SLEEP_TIME)
            detail_urls.extend(get_project_url(driver))
    
        result = list()
        for i_url in detail_urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME) 
            get_info(driver)
            result.append(get_detail_info(driver))
    
        pd.DataFrame(result).to_csv(CSV_NAME, index=False)
        
    finally:
        driver.quit()