# -*- coding: utf-8 -*-

"""
Peatixイベントの情報を取得する
"""
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 4
CSV_NAME = "output/peatix.csv"

def page_update(driver):
    driver.find_element(By.CLASS_NAME, "next").click()

def check_last(driver):
    button_css = driver.find_element(By.CLASS_NAME, "next").get_attribute("style")
    return "display: none" in button_css

def get_url(driver):
    ul_element = driver.find_element(By.CSS_SELECTOR, ".event-list.event-list__medium")
    a_elements =ul_element.find_elements(By.CLASS_NAME, "event-thumb_link")
    return [i.get_attribute("href") for i in a_elements]

def get_info(driver):
    result = dict()
    result["id"] = driver.current_url.split("/")[-1].split("?")[0]
    result["url"] = driver.current_url
    print(result["url"])
    result["title"] = driver.find_element(By.CLASS_NAME, "event-summary__title").text

    event_info_elemet = driver.find_element(By.CLASS_NAME, "event-essential")
    time_element = event_info_elemet.find_element(By.TAG_NAME, "time")
    result["date"] = time_element.find_elements(By.TAG_NAME, "p")[0].text
    result["time"] = time_element.find_elements(By.TAG_NAME, "p")[1].text

    address_elements = event_info_elemet.find_elements(By.CSS_SELECTOR, "address")
    result["place"] = address_elements[0].text if len(address_elements) > 0 else "オンライン"
    
    ul_elements = event_info_elemet.find_elements(By.CLASS_NAME, "event-tickets__list")
    if len(ul_elements) > 0:
        result["ticket"] = "/".join([i.text for i in ul_elements[0].find_elements(By.TAG_NAME, "li")])
    
    result["description"] = driver.find_element(By.CLASS_NAME, "event-main").text
    result["organize"] = driver.find_element(By.CLASS_NAME, "pod-thumb__name-link").text
    
    return result    
    
    
if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://peatix.com/search?q=python&country=JP&l.text=%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E5%A0%B4%E6%89%80&p=1&size=20&v=3.4&tag_ids=&dr=&p=2")
        urls = list()
        while True:
            time.sleep(SLEEP_TIME)
            urls.extend(get_url(driver))
            if check_last(driver):
                break
            page_update(driver)

        result=list()
        for i_url in urls:
            driver.get(i_url)
            time.sleep(SLEEP_TIME)
            result.append(get_info(driver))
        
        pd.DataFrame(result).to_csv(CSV_NAME)
        print(pd.DataFrame(result))

    finally:
        driver.quit()
