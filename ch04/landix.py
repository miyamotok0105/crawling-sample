# -*- coding: utf-8 -*-

"""
landixから東京都の城南エリア物件情報取得
"""
import re
import time
import datetime
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3

def get_item_urls(driver):
    result = list()
    article_elements = driver.find_elements(By.TAG_NAME, "article")
    result.extend([i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in article_elements])
    while len(driver.find_elements(By.CSS_SELECTOR, ".next.page-numbers")) > 0:
        driver.find_element(By.CSS_SELECTOR, ".next.page-numbers").click()
        time.sleep(SLEEP_TIME)
        article_elements = driver.find_elements(By.TAG_NAME, "article")
        result.extend([i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in article_elements])
    return result

# ----------------------------------------------------------------------------------
def preprosess_station(val:str):
    return [ i.replace("駅", "") for i in val.split("\n")[0].split(" ") if "駅" in i ][0]

def preprosess_walk_min(val:str):
    return [ re.sub(r"\D", "", i) for i in val.split("\n")[0].split(" ") if "分" in i ][0]

def preprosess_land_area(val:str):
    return re.sub(r"\D", "", [i for i in val.split(" ") if "㎡" in i][0])

def preprosess_price(val:str):
  price_elms = re.findall('[0-9,]+[^0-9]+', val)
  price_ele = 0
  for price_elm in price_elms:
      price_string = re.findall('[0-9,]+', price_elm)[0]
      number = float(re.sub(',', '', price_string))
      scale = 1
      if "億" in price_elm:
          scale = 100000000
      elif "万" in price_elm:
          scale = 10000
      elif "千" in price_elm:
          scale = 1000
      else:
          print('億、万、千が含まれていません')
      price_ele = price_ele + int(number * scale)
  return price_ele

def get_item_info(driver):
    td_elements = [i.text for i in driver.find_elements(By.TAG_NAME, "td")]
    columns = td_elements[::2]
    values =  td_elements[1::2]
    data_dict = {k:v for k,v in zip(columns, values)}

    result = {
      "crawl_date": str(datetime.date.today()),
      "url": driver.current_url,
      "land_image_url": "",
      "address": data_dict["所在地"],
      "price": preprosess_price(data_dict["価格"]),
      "train": "", #使ってない
      "full_station_min": "", #使ってない
      "station": preprosess_station(data_dict["交通"]),
      "walk_min": preprosess_walk_min(data_dict["交通"]),
      "distance": "", #改訂版デザインはなし
      "land_area": preprosess_land_area(data_dict["土地面積"]),
      "present_situation": "",  #使ってない
      "ownership": data_dict["権利"], 
      "land_type": "", #使ってない
      "city_plan": "", #使ってない
      "area_of_use": data_dict["地目"],
      "construct_condition": "", #使ってない
      "roadway": data_dict["接道"],
      "coverage_ratio": data_dict["容積率"].replace("%", ""),
      "floor_area_ratio": data_dict["建ぺい率"].replace("%", ""),
      "trade_type": "", #使ってない
      "renew_date": "", #使ってない
      "extra": "", #改訂版デザインはなし
      "setback": "" #改訂版デザインはなし
      }

    return result 

    
if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        target_url = "https://portal-landix.jp/recommend/"
        driver.get(target_url)
        urls = get_item_urls(driver)

        result = list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_item_info(driver))
            print("-----------------------------------------------------")

        pd.DataFrame(result).to_csv("tmp.csv")

    finally:
        driver.quit()