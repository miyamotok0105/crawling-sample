# -*- coding: utf-8 -*-

"""
仮想通貨取引所バイナンスのデータを取得する
"""
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

DATA_DIR = "output"
SLEEP_TIME = 1

if __name__=="__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://www.binance.com/ja/markets"
        driver.get(base_url)
        time.sleep(SLEEP_TIME)
        
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        btc_file_name = os.path.join(DATA_DIR, "btc.csv")
        f_btc = open(btc_file_name, "a")
        eth_file_name = os.path.join(DATA_DIR, "eth.csv")
        f_eth = open(eth_file_name, "a")
        usdt_file_name = os.path.join(DATA_DIR, "usdt.csv")
        f_usdt = open(usdt_file_name, "a")

        price_elements = driver.find_elements(By.CLASS_NAME, "css-ydcgk2")
        while True:
            btc_price = price_elements[0].text
            eth_price = price_elements[1].text
            usdt_price = price_elements[2].text

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f_btc.write(f"{btc_price.replace(',','')},{now}\n")
            f_eth.write(f"{eth_price.replace(',','')},{now}\n")
            f_usdt.write(f"{usdt_price.replace(',','')},{now}\n")
            print(now)

            time.sleep(SLEEP_TIME)
    
    finally:
        driver.quit()