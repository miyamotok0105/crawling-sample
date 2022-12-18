# -*- coding: utf-8 -*-

"""
Home’sから物件情報取得
"""
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import configparser
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

def update_page_num(driver, page_num):
    base_url = "https://www.homes.co.jp/chintai/tokyo/list/?page=2"
    next_url = base_url + f"?page={page_num}"
    driver.get(next_url)

def get_item_urls(driver):
    detail_elements = driver.find_elements(By.CLASS_NAME, "detail")
    hrefs = list()
    for i in detail_elements:
          try:
            a_element = i.find_element(By.TAG_NAME,"a")
            hrefs.append(a_element.get_attribute("href"))
          except:
            pass
    return hrefs

def is_last_page(driver):
    paging_element = driver.find_element(By.XPATH, '//*[@id="searchResult"]/div[3]')
    print(paging_element.text)
    return not "次" in paging_element.text

def set_option(driver):
    select_object.select_by_value('value1')
    
def get_item_info(driver):
    table_element = driver.find_element(By.CSS_SELECTOR, ".vertical.col4")
    df = pd.read_html(table_element.get_attribute("outerHTML"))[0]
    
    first_df = df.iloc[:, :2]
    keys = [i.replace("  ヒント", "") for i in first_df.iloc[:,0].tolist()]
    vals = first_df.iloc[:,1].tolist()
    print({i_key:i_val for i_key, i_val in zip(keys, vals)})
    return {i_key:i_val for i_key, i_val in zip(keys, vals)}

    second_df = df.iloc[:, 2:]

def scraping():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        # driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver", options=chrome_options)
        # driver.get('https://www.google.nl/')

        target_url = "https://www.homes.co.jp/chintai/tokyo/list/?cond%5Broseneki%5D%5B43704833%5D=43704833&cond%5Bmonthmoneyroomh%5D=0&cond%5Bhousearea%5D=0&cond%5Bhouseageh%5D=0&cond%5Bwalkminutesh%5D=0&bukken_attr%5Bcategory%5D=chintai&bukken_attr%5Bpref%5D=13" # 検索後の画面が出てくるURL
        driver.get(target_url)   

        time.sleep(15)

        # ページ設定
        # 賃料
        price_element = driver.find_element(By.ID,'cond_monthmoneyroomh')
        price_select_object = Select(price_element)
        price_select_object.select_by_value('6.0')

        time.sleep(13)
        # 間取り
        floor_element = driver.find_element(By.ID,'cond_madori_13')
        if not floor_element.is_selected():
              floor_element.click()
        # 収集対象のURLを取得する
        # logger.info("start scrape item urls.")
        page_num=0
        item_urls = list()
        while True:   # ページ数がわかるならforがいい。tqdm使えるし。
            time.sleep(5) 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            print(urls)
            if is_last_page(driver): # 最終ページ
                break
            else:
                page_num+=1
                update_page_num(driver, page_num)

        # 商品ごとに収集する
        item_infos = list()
        # logger.info("start scrape item info.")
        for i_url in item_urls:
            print(i_url)
            time.sleep(1)
            driver.get(i_url)   
            item_infos.append(get_item_info(driver))
        
        return item_infos
    
    finally:
        driver.save_screenshot('screenie.png')
        driver.quit()


if __name__=="__main__":
  scraping()
