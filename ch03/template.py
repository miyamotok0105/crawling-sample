import time
import requests
import datetime
from tqdm import tqdm
import logging
from logging import config, getLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
import configparser

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

def get_item_urls(driver):
    """
    検索結果のページから商品のURLのみを取得する
    
    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver

    Returns
    --------------------------------------
    
    """

def get_item_info(driver):
    """
    商品ページから必要なデータを取得し、
    結果を専用のデータ型に書き込み返す。

    PArameters
    ---------------------------------
    driver:
      商品紹介ページを表示した状態のchrome driver
      
    Returns
    ---------------------------------
    result: 
      データを纏めたオブジェクト
    """

    
if __name__=="__main__":
    try:
        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        
        # 運用後に変更が考えられる変数は外部ファイルで操作したい
        logger.info("start crawling")
        config_ini = configparser.ConfigParser()
        config_ini.read('config.ini', encoding='utf-8')
        

        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") # ここは要調整
        target_url = "" # 検索後の画面が出てくるURL
        driver.get(target_url)   

        time.sleep(10)


        # 収集対象のURLを取得する
        logger.info("start scrape item urls.")
        page_num=0
        item_urls = list()
        while True:   # ページ数がわかるならforがいい。tqdm使えるし。
            time.sleep(5) 
            urls = get_item_urls(driver)
            if len(urls) < 1: # 最終ページ
                break
            else:
                item_urls.extend(urls)
                page_num+=1
                update_page_num(driver, page_num)

        # 商品ごとに収集する
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