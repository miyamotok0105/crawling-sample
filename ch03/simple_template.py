import sys
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

class XX_scraper:
    def __init__(self, config_path):
        # read config file 
        config_ini = configparser.ConfigParser()
        config_ini.read('config.ini', encoding='utf-8')
        
        # configから
        self.base_url = base_url
        logfile_path = ""
        
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver" # ここをconfigfileで
        # Driver
        # v4では以下の書き方になるらしい
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        self.driver = webdriver.Chrome(service=chrome_service)
        # logもしっかり書こう
        self.logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        fh = logging.FileHandler(logfile_path) # logファイルの
        self.logger.addHandler(fh)
    
    def update_page_num(self, page_num):
        """
        検索結果のページを次のページへ更新する。
    
        Parameters
        --------------------------------------
        pagenum:int
          更新後のページ数
        """

    def get_item_urls(self):
        """
        検索結果のページから商品のURLのみを取得する
        
        Returns
        --------------------------------------
        result: list[str]
            商品ページを纏めたもの
        """

    def get_item_info(self):
        """
        商品ページから必要なデータを取得し、
        結果を専用のデータ型に書き込み返す。
          
        Returns
        ---------------------------------
        result: list[items]
          データを纏めたオブジェクト
        """

    def is_last_page(self):
        """
        driverの画面が最終ページか判断する関数

        Returns
        ------------------------------------
        result: bool
          最終ページの場合
        """
  
    def scraping(self):
        """
        上記コードを組み合わせて、クローリング&スクレーピングを行う
    
        Returns 
        ----------------------------------------
        item_infos:
            商品データを纏めたデータ型のリスト
        """
        try:
            # 運用後に変更が考えられる変数は外部ファイルで操作したい
            self.logger.info("start crawling")
            self.driver.get(self.base_url)   
            time.sleep(10)
    
            # 収集対象のURLを取得する
            self.logger.info("start scrape item urls.")
            page_num=0
            item_urls = list()
            while True:   # ページ数がわかるならforがいい。tqdm使えるし。
                time.sleep(5) 
                urls = self.get_item_urls()
                if self.check_last(): # 最終ページ
                    break
                else:
                    item_urls.extend(urls)
                    page_num+=1
                    self.update_page_num(page_num)
    
            # 商品ごとに収集する
            item_infos = list()
            self.logger.info("start scrape item info.")
            for i_url in tqdm(item_urls):
                self.driver.get(i_url)   
                time.sleep(5)
                item_infos.append(self.get_item_info())
          
            return item_infos
          
        finally:
            self.driver.quit()
            self.logger.info('end crawring')       

if __name__=="__main__":
    scraper = XX_scraper("config.ini")
    scraper