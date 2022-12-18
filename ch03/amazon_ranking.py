# -*- coding: utf-8 -*-

"""
Amazon商品ランキング情報(IT)を取得する
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

if __name__=="__main__":
    try:
        CSV_NAME = "output/amazon_ranking.csv"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        base_url = "https://www.amazon.co.jp/gp/new-releases/books/466298/ref=zg_bsnr_unv_books_2_492350_1"
        driver.get(base_url)        
        time.sleep(5)

        # scroll
        while len(driver.find_elements(By.ID, "gridItemRoot")) < 50:
            time.sleep(5)
            driver.execute_script("window.scrollBy(0, 3000);")

        # レビューごとの要素
        prosuct_elements = driver.find_elements(By.ID, "gridItemRoot")

        results = list()
        for i_section in prosuct_elements:
            result_row = dict()
            # url
            a_element = i_section.find_element(By.CSS_SELECTOR, "div > div:nth-child(2) > div > a:nth-child(2)")
            result_row["url"] = a_element.get_attribute("href")
            # 製品名
            result_row["name"] = a_element.text

            print(result_row)

            results.append(result_row)
    finally:
        driver.quit()

    df = pd.DataFrame(results)
    df.to_csv(CSV_NAME)
