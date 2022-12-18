# -*- coding: utf-8 -*-

"""
秀和システムのデータを取得する（最小版）
"""


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
# クロムドライバーの自動インストールをすると手間が減ります
from webdriver_manager.chrome import ChromeDriverManager

if __name__=="__main__":
    try:
        # 手動ダウンロードした場合
        # クロムドライバーの指定
        # CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        # chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        # driver = webdriver.Chrome(service=chrome_service)
        
        # ChromeDriverManagerを使用した場合
        driver = webdriver.Chrome(ChromeDriverManager().install())

        target_url = "https://www.shuwasystem.co.jp/book/9784798068596.html"
        driver.get(target_url)

        result = dict()
        result["title"] = driver.find_element(By.CLASS_NAME, "titleWrap").text
        result["price"] = driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div[2]/table/tbody/tr[6]/td').text
        result["author"] = driver.find_element(By.CSS_SELECTOR, "#main > div.detail > div.right > table > tbody > tr:nth-child(1) > td > a").text
        result["describe"] = driver.find_element(By.ID, "bookSample").text
        print(result)
    
    finally:
        driver.quit()
