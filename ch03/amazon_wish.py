# -*- coding: utf-8 -*-

"""
Amazon欲しいものリスト情報を取得する
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

if __name__=="__main__":
    try:
        CSV_NAME = "output/amazon_wish.csv"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://www.amazon.co.jp/hz/wishlist/ls/7UNVFD2BUDK5?ref_=wl_share"
        driver.get(base_url)
        
        time.sleep(5)
        
        # レビューごとの要素
        prosuct_elements = driver.find_elements(By.CLASS_NAME, "a-fixed-right-grid-inner")
        print(prosuct_elements)

        results = list()
        for i_section in prosuct_elements:
            result_row = dict()
            # 製品名
            name_element = i_section.find_element(By.TAG_NAME, "h2")
            result_row["name"] = name_element.text
            # 価格
            price_text = i_section.find_element(By.CLASS_NAME, "a-price-whole").text
            result_row["price"] = int(price_text.replace(",", ""))
            # url
            result_row["url"] = name_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            results.append(result_row)
    
    finally:
        driver.quit()

    print(results)    
    df = pd.DataFrame(results)
    df.to_csv(CSV_NAME)
