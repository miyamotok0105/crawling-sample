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
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
import pandas as pd 

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
    base_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=30&smk=&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&rn=0350&ek=035009200&ra=013&cb=0.0&ct=6.0&md=03&et=9999999&mb=0&mt=9999999&cn=9999999&fw2="
    next_url = base_url + f"&pn={page_num}"
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
    h2_elements = driver.find_elements(By.CSS_SELECTOR, ".cassetteitem_other-linktext")
    return [i.get_attribute("href") for i in h2_elements]

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
    table_element = driver.find_element(By.CSS_SELECTOR, ".data_table.table_gaiyou")
    df = pd.read_html(table_element.get_attribute("outerHTML"))[0]
    
    first_df = df.iloc[:, :2]
    # first_df.iloc[:,0] = [i.replace("  ヒント", "") for i in first_df.iloc[:,0].tolist()]
    keys = [i.replace("  ヒント", "") for i in first_df.iloc[:,0].tolist()]
    vals = first_df.iloc[:,1].tolist()
    info_dict = {i_key:i_val for i_key, i_val in zip(keys, vals)}
    print(pd.DataFrame.from_dict(info_dict))


def is_last_page(driver):
    paging_elements = driver.find_elements(By.CLASS_NAME, "pagination-parts")
    paging_text = [i.text for i in paging_elements]
    if "次へ" in paging_text:
        return False
    else:
        return True

def scraping():
    """
    上記コードを組み合わせて、クローリング&スクレーピングを行う

    Returns 
    --------------------------------------
    item_infos:
        商品データを纏めたデータ型のリスト
    """

    try:
        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        fh = logging.FileHandler('spam.log') # logファイルの
        logger.addHandler(fh)

        logger.info("start crawling")
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver",options=chrome_options)
        target_url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=30&smk=&po1=25&po2=99&shkr1=03&shkr2=03&shkr3=03&shkr4=03&rn=0350&ek=035009200&ra=013&cb=0.0&ct=6.0&md=03&et=9999999&mb=0&mt=9999999&cn=9999999&fw2="
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
            if is_last_page(driver): # 最終ページ
                break
            else:
                page_num+=1、
                update_page_num(driver, page_num)

        # 商品ごとに収集する
        item_info_df = pd.DataFrame(columns=['間取り詳細', '階建', '損保', '入居', '条件', 'SUUMO物件コード', '情報更新日', '仲介手数料', '保証会社', 'ほか初期費用', 'ほか諸費用', '備考'])
        logger.info("start scrape item info.")
        for i_url in item_urls:
            print(i_url)
            time.sleep(1)
            driver.get(i_url)   
            pd.concat(item_info_df, get_item_info(driver))、
        
        return item_info_df
    
    finally:
        driver.quit()
        logger.info('end crawring')       


if __name__=="__main__":
  scraping()