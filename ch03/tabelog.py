# -*- coding: utf-8 -*-

"""
食べログの飲食店データを取得する
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 4
CSV_NAME = "output/tabelog.csv"

def get_next(driver):
    pagenation_element = driver.find_elements(By.CLASS_NAME, "c-pagination__item")[-1]
    pagenation_element.find_element(By.TAG_NAME, "a").click()

def check_last(driver):
    pagenation_element = driver.find_element(By.CLASS_NAME, "list-pagenation")
    return True if "次" in pagenation_element.text else False

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://tabelog.com/tokyo/rstLst/?vs=1&sa=%E6%9D%B1%E4%BA%AC%E9%83%BD&sk=%25E5%2588%2580%25E5%2589%258A%25E9%25BA%25BA&lid=top_navi1&vac_net=&svd=20220822&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC03&LstCatD=RC0304&LstCatSD=RC030402&cat_sk=%E5%88%80%E5%89%8A%E9%BA%BA"        
        driver.get(base_url)
        time.sleep(SLEEP_TIME)
        # get store page url
        count_elements = driver.find_elements(By.CLASS_NAME, "c-page-count__num")
        paging_num = int(count_elements[1].text)
        total_num = int(count_elements[2].text)
        page_num  = total_num // paging_num

        store_urls = list()
        for i in range(page_num):
            store_elements = driver.find_elements(By.CSS_SELECTOR, ".list-rst__wrap.js-open-new-window")
            store_elements = [i.find_element(By.TAG_NAME, "h3") for i in store_elements]
            store_elements = [i.find_element(By.TAG_NAME, "a") for i in store_elements]
            urls = [i.get_attribute("href") for i in store_elements]
            store_urls.extend(urls)
            print(urls)
            get_next(driver)
            time.sleep(SLEEP_TIME)

        results = list()
        for i_url in store_urls:
            map_url = i_url + "dtlmap/"
            driver.get(map_url)
            table_elements = driver.find_elements(By.CSS_SELECTOR, ".c-table.c-table--form.rstinfo-table__table")
            outer_table = [i.get_attribute("outerHTML") for i in table_elements]    
            df = pd.read_html(outer_table[0])[0]
            columns = df[0].tolist()
            values = df[1].tolist()
            results.append({k:v for k,v in zip(columns, values)})
            time.sleep(SLEEP_TIME)
    finally:
        driver.quit()

    df = pd.DataFrame(results)
    df.to_csv(CSV_NAME)
