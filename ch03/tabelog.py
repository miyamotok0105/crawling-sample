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

def get_pagenum(driver):
    count_elements = driver.find_elements(By.CLASS_NAME, "c-page-count__num")
    paging_num = int(count_elements[1].text)
    total_num = int(count_elements[2].text)
    return total_num // paging_num

def get_store_url(driver):
    store_elements = driver.find_elements(By.CSS_SELECTOR, ".list-rst__wrap.js-open-new-window")
    store_elements = [i.find_element(By.TAG_NAME, "h3") for i in store_elements]
    store_elements = [i.find_element(By.TAG_NAME, "a") for i in store_elements]
    return [i.get_attribute("href") for i in store_elements]

def get_store_info(driver, url):
    map_url = url + "dtlmap/"
    driver.get(map_url)
    time.sleep(SLEEP_TIME)
    table_elements = driver.find_element(By.CSS_SELECTOR, ".c-table.c-table--form.rstinfo-table__table")
    th_texts = [i.text for i in table_elements.find_elements(By.TAG_NAME, "th")]
    td_texts = [i.text for i in table_elements.find_elements(By.TAG_NAME, "td")]
    return {k:v for k,v in zip(th_texts, td_texts)}

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://tabelog.com/tokyo/rstLst/?vs=1&sa=%E6%9D%B1%E4%BA%AC%E9%83%BD&sk=%25E5%2588%2580%25E5%2589%258A%25E9%25BA%25BA&lid=top_navi1&vac_net=&svd=20220822&svt=1900&svps=2&hfc=1&Cat=RC&LstCat=RC03&LstCatD=RC0304&LstCatSD=RC030402&cat_sk=%E5%88%80%E5%89%8A%E9%BA%BA"        
        driver.get(base_url)
        time.sleep(SLEEP_TIME)

        page_num = get_pagenum(driver)
        # データの量を減らす
        page_num = 1

        store_urls = list()
        for i in range(page_num):
            urls = get_store_url(driver)
            # データの量を減らす
            urls = urls[:2]

            store_urls.extend(urls)
            get_next(driver)
            time.sleep(SLEEP_TIME)

        # データの量を減らす
        store_urls = store_urls[:2]
        
        results = list()
        for i_url in store_urls:
            store_info = get_store_info(driver, i_url)
            results.append(store_info)
    finally:
        driver.quit()

    print(results)
    df = pd.DataFrame(results)
    df.to_csv(CSV_NAME, index=False)
