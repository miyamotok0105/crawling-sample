# -*- coding: utf-8 -*-

"""
秀和システムのデータを取得する
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
# クロムドライバーの自動インストールをすると手間が減ります
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
CSV_NAME = "output/syuwa.csv"

def update_page_num(driver, page_num):
    base_url = "https://www.shuwasystem.co.jp/search/index.php?search_genre=13273&c=1"
    page_option = f"&page={page_num}"
    next_url = base_url + page_option
    driver.get(next_url)

def get_item_urls(driver):
    ro_element = driver.find_element(By.CLASS_NAME, "bookWrap")
    ttl_elements = ro_element.find_elements(By.CLASS_NAME, "ttl")
    a_elements = [i.find_element(By.TAG_NAME, "a") for i in ttl_elements]
    return [i.get_attribute("href") for i in a_elements]

def get_item_info(driver):
    result = dict()
    result["title"] = driver.find_element(By.CLASS_NAME, "titleWrap").text
    result["price"] = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div[2]/table/tbody/tr[6]/td').text
    result["author"] = driver.find_element(By.CSS_SELECTOR, "#main > div.detail > div.right > table > tbody > tr:nth-child(1) > td > a").text
    result["describe"] = driver.find_element(By.ID, "bookSample").text
    return result

def is_last_page(driver):
    pagingWrap_element = driver.find_element(By.CLASS_NAME, "pagingWrap")
    paging_text = pagingWrap_element.find_element(By.CLASS_NAME, "right").text
    return not "次" in paging_text

if __name__=="__main__":
    try:
        # 手動ダウンロードした場合
        # クロムドライバーの指定
        # CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        # chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        # driver = webdriver.Chrome(service=chrome_service)

        # ChromeDriverManagerを使用した場合
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        page_num = 1
        item_urls = list()
        while True:
            update_page_num(driver, page_num)
            time.sleep(SLEEP_TIME) 
            urls = get_item_urls(driver)
            print(urls)
            item_urls.extend(urls)
            if is_last_page(driver): 
                break
            page_num += 1
        # データの量を減らす
        item_urls = item_urls[:2]

        item_infos = list()
        for i_url in item_urls:
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            item_infos.append(get_item_info(driver))
      
        df = pd.DataFrame(item_infos)
        df.to_csv(CSV_NAME, index=False)
      
    finally:
        driver.quit()