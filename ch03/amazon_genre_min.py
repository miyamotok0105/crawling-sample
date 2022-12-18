# -*- coding: utf-8 -*-

"""
ジャンル別でAmazon商品情報を取得する（最小版）
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

if __name__=="__main__":
    try:
        base_url = "https://www.amazon.co.jp/gp/bestsellers/musical-instruments/3232345051/ref=zg_bs_nav_musical-instruments_2_2130095051"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(base_url)        
        time.sleep(5)
        # レビューごとの要素
        prosuct_elements = driver.find_elements(By.ID, "gridItemRoot")
        i_section = prosuct_elements[0]
        result_row = dict()
        # url
        a_element = i_section.find_element(By.CSS_SELECTOR, "div > div:nth-child(2) > div > a:nth-child(2)")
        result_row["url"] = a_element.get_attribute("href")
        # 製品名
        result_row["name"] = a_element.text
        print(result_row)

    finally:
        driver.quit()
