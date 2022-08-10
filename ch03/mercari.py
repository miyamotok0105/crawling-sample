import time
import requests
import datetime
from tqdm import tqdm
import logging
from logging import config, getLogger
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class Mercari_serch_option:
    base_url = None
    keyword = None
    order_by = None
    category = None
    sub_category_1 = None
    sub_category_2 = list()
    max_price = None
    min_price = None
    condition = None
    sales_status= None

class Mercari_item_info:
    id = None
    datetime = None
    title = None
    price = None
    postage = None
    description = None
    image_urls = list()

    
def update_page_num(driver, page_num):
    page_option = f"&page_token=v1%3A{page_num}"
    driver.get(target_url + page_option)

def get_item_urls(driver):
    a_tag_elements = driver.find_elements_by_tag_name("a")
    hrefs = [i.get_attribute("href") for i in a_tag_elements]
    item_urls = [i for i in hrefs if "item" in i]
    return item_urls

def get_item_info(driver):
    result = Mercari_item_info()

    # id
    result.id = driver.current_url.split("/")[-1]
    # datetime
    now = datetime.datetime.now()
    result.datetime = now.strftime('%y/%m/%d %H:%M:%S')    
    # title
    title_element = driver.find_element(By.CSS_SELECTOR, '#item_h1 > span')
    result.title = title_element.text
    # price
    price_element = driver.find_element(By.CSS_SELECTOR, "#abtest_display_pc")
    result.price = price_element.text
    # description
    description_element = driver.find_element(By.CSS_SELECTOR, "#item_maincol > div.item_main_tabcontent.js-itemdetail-tabcontent > div.item_main_tabcontent_item.is-itemdetail-tabcontent-active > div:nth-child(1) > div > p")
    result.description = description_element.text
    
    return result

    
if __name__=="__main__":
    try:
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        target_url = "https://jp.mercari.com/search?keyword=novation&t1_category_id=1328&status=on_sale&category_id=79"
        driver.get(target_url)   


        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)

        logger.info("start scrape item urls.")
        time.sleep(10)
        page_num=0
        item_urls = list()
        while True:
            time.sleep(5)
            urls = get_item_urls(driver)
            if len(urls) < 1: # 最終ページ
                break
            else:
                item_urls.extend(urls)
                page_num+=1
                update_page_num(driver, page_num)

        item_infos = list()
        logger.info("start scrape item info.")
        for i_url in tqdm(item_urls):
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))

    except Exception as e :
        logger.error(e)       
    finally:
        driver.quit()
        logger.info('end crawring') 