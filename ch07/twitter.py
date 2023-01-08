# -*- coding: utf-8 -*-

"""
Twitterの特定のユーザーの投稿一覧を取得する
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

CSV_NAME = "output/twitter.csv"

if __name__=="__main__":
    try:
        base_url = "https://twitter.com/NanashinoSeito"        
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(base_url)
        
        time.sleep(10)

        # scroll
        pri_html = None
        tweet_elements = list()
        # while not pri_html == driver.page_source:
        a = True
        while a:
            tweet_elements.extend(driver.find_elements(By.TAG_NAME, "article"))
            print("="*100)

            driver.execute_script("window.scrollBy(0, 2000);")
            time.sleep(5)
            a =False

        # レビューごとの要素
        tweet_elements = set(tweet_elements)
        results = list()
        for i_section in tweet_elements:
            result_row = dict()
            # account
            a_element = i_section.find_element(By.CSS_SELECTOR, "div > div > div > div:div:nth-child(2) > div:div:nth-child(2) > div:nth-child(1) > div > div > div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > div > #id__ycxu7h1fa18 > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2.r-dnmrzs > div > a")
            result_row["acount_name"] = a_element.text
            result_row["acount_id"] = a_element.get_attribute("href")
            # time
            result_row["time"] = find_element(By.TAG_NAME, "time").text
            # text
            result_row["text"] = i_section.find_element(By.CSS_SELECTOR,"div > div > div > div:div:nth-child(2) > div:div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > #id__1vzh5boiiu4 > span").text

            print(result_row)

            results.append(result_row)
    finally:
        driver.quit()
# text
#article > div > div > div > div:div:nth-child(2) > div:div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > #id__1vzh5boiiu4 > span

# time 
#article > div > div > div > div:div:nth-child(2) > div:div:nth-child(2) > div:nth-child(1) > div > div > div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > div > #id__e4lvwhqw2j > div.css-1dbjc4n.r-18u37iz.r-1wbh5a2.r-13hce6t > div > div.css-1dbjc4n.r-18u37iz.r-1q142lx > a > time

# account
#article > div > div > div > div:div:nth-child(2) > div:div:nth-child(2) > div:nth-child(1) > div > div > div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > div > #id__ycxu7h1fa18 > div.css-1dbjc4n.r-1awozwy.r-18u37iz.r-1wbh5a2.r-dnmrzs > div > a