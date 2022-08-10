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
from seleium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
import pandas as pd 

class Suumo_item:
      name = None
      price = None
      floor_plan = None
      address = None
      url = None


def update_page_num(driver, page_num):
    """
    検索結果のページを次のページへ更新する。

    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver
      
    pagenum:int
      更新後のページ数
    """
    base_url = "https://houjin.jp/search?utf8=%E2%9C%93&keyword=&pref_id=13&city_id=13104&industry_id=11"
    next_url = base_url + f"&page={page_num}"
    driver.get(next_url)

def get_item_urls(driver):
    """
    検索結果のペ1ージから商品のURLのみを取得する
    
    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver

    Returns
    --------------------------------------
    
    """
    cop_item_elements = driver.find_elements(By.CLASS_NAME, "c-corp-item")
    return [i.find_element(By.TAG_NAME,"a").get_attribute("href") for i in cop_item_elements]

def get_item_info(driver):
    """
    商品ページから必要なデータを取得し、
    結果を専用のデータ型に書き込み返す。
    Parameters
    ---------------------------------
    driver:
      商品紹介ページを表示した状態のchrome driver
      
    Returns
    ---------------------------------
    result: 
      データを纏めたオブジェクト
    """
    corp_info_table_element = driver.find_element(By.CLASS_NAME, "corp-info-table")
    corp_info_html = corp_info_table_element.get_attribute("outerHTML")
    corp_info_df = pd.read_html(corp_info_html)[0]
    print(corp_info_df)
    keys = corp_info_df.iloc[:,0].tolist()
    vals = corp_info_df.iloc[:,1].tolist()
    corp_info_dict = {i_key:i_val for i_key, i_val in zip(keys, vals)}

    print(corp_info_dict)
    # print(second_df)
    # 法人名
    # 法人番号
    # 間取り
    # 住所
    # URL


def scraping():
    """
    上記コードを組み合わせて、クローリング&スクレーピングを行う

    Returns 
    ----------------------------------------
    item_infos:
        商品データを纏めたデータ型のリスト
    """

    try:
        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        fh = logging.FileHandler('spam.log') # logファイルの
        logger.addHandler(fh)

        # 運用後に変更が考えられる変数は外部ファイルで操作したい
        logger.info("start crawling")
        # config_ini = configparser.ConfigParser()
        # config_ini.read('config.ini', encoding='utf-8')

        # v4では以下の書き方になるらしい
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver",options=chrome_options)
        # driver.get('https://www.google.nl/')

        target_url = "https://houjin.jp/search?utf8=%E2%9C%93&keyword=&pref_id=13&city_id=13104&industry_id=11" # 検索後の画面が出てくるURL
        driver.get(target_url)

        time.sleep(5)

        # 収集対象のURLを取得する
        logger.info("start scrape item urls.")
        page_num=0
        item_urls = list()
        while True:   # ページ数がわかるならforがいい。tqdm使えるし。
            time.sleep(5) 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            print(urls)
            # if len(urls) < 1: # 最終ページ
            if True: # 最終ページ
                break
            else:
                page_num+=1
                update_page_num(driver, page_num)

        # 商品ごとに収集する
        item_infos = list()
        logger.info("start scrape item info.")
        for i_url in item_urls:
            print(i_url)
            time.sleep(1)
            driver.get(i_url)   
            item_infos.append(get_item_info(driver))
        
        return item_infos
    
    finally:
        driver.quit()
        logger.info('end crawring')       


if __name__=="__main__":
  scraping()