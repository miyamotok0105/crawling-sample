# -*- coding: utf-8 -*-

"""
Netflix配信終了予定の情報を取得する
"""
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 2
CSV_NAME = "output/netflix_end.csv"

def get_info(day_elements):
    result = list()
    for i_day in day_elements:
        i_day_class = i_day.get_attribute("class").replace(" ", ".")
        day = i_day.find_element(By.TAG_NAME, "p").get_attribute("textContent")
        genre_elements = i_day.find_elements(By.CSS_SELECTOR, f".{i_day_class} > div")
        genre_elements = [i for i in genre_elements if not i.get_attribute("class") == "g-calen-all5"]
        for i_genre in genre_elements:
            genre_name = i_genre.find_element(By.CLASS_NAME, "szam1").get_attribute("textContent")
            li_elements = i_genre.find_elements(By.TAG_NAME, "li")
            for i_li in li_elements:
                # print(i_li.get_attribute("outerHTML"))
                movie_result = dict()
                movie_result["day"] = day
                movie_result["genre"] = genre_name
                a_element = i_li.find_element(By.CSS_SELECTOR, "div.firt-top1 > a")
                movie_result["title"] = a_element.get_attribute("textContent")
                movie_result["url"] = a_element.get_attribute("href")
                result.append(movie_result)
    return result

if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://www.net-frx.com/p/netflix-expiring.html"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        result = list()
        month1_elements = driver.find_elements(By.CSS_SELECTOR, ".data-fd1.goke3 > div")
        result.extend(get_info(month1_elements))
        
        month2_elements = driver.find_elements(By.CSS_SELECTOR, ".data-fd2 > div")
        result.extend(get_info(month2_elements))

        pd.DataFrame(result).to_csv(CSV_NAME)
        print(pd.DataFrame(result))
    
    finally:
        driver.quit()
