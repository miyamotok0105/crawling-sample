import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 3
CSV_NAME = "mbok.csv"

def update_page_num(driver, page_num):
    driver.get(f"https://www.mbok.jp/category/categ_80.html?o=&at=all&q=%C8%B8%C0%B2&vt=0&ls%5Fexec=1&p={page_num}")

def get_item_urls(driver):
    elements = driver.find_elements(By.CLASS_NAME, "item-thumb")
    item_urls = [i.get_attribute('href') for i in elements]
    return item_urls

def get_item_info(driver):
    result = dict()
    result["url"] = driver.current_url.split("/")[-1]
    result["title"]  = driver.find_element(By.CLASS_NAME, "title").text
    price_elements = log_elements[0].find_elements(By.TAG_NAME, "span")
    result["price"] = driver.find_elements(By.CSS_SELECTOR, "p.log-left2 > span")[0].text
    result["time_left"] =driver.find_elements(By.CSS_SELECTOR, "p.log-left2 > span")[2].text
    result["bid_number"] = driver.find_elements(By.CSS_SELECTOR, "p.log-left2")[2].text
    result["description"] = driver.find_element(By.CSS_SELECTOR, "li.article-detail > div.descript").text

    detail_element = driver.find_element(By.CSS_SELECTOR, "li.article-detail > dl.dlist")
    keys = detail_element.find_elements(By.TAG_NAME, "dt")
    values = detail_element.find_elements(By.TAG_NAME, "dd")
    for k,v in zip(keys, values): result[k] = v
    return result

if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        target_url = "https://www.mbok.jp/category/categ_80.html?o=&at=all&q=%C8%B8%C0%B2&vt=0&ls%5Fexec=1&p=1"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
        
        total_num = int(driver.find_element(By.CLASS_NAME, "pagerSum")
                              .text
                              .replace("合計", "")
                              .replace("件", ""))

        page_num = total_num // 50 +1
        urls = list()
        for i in range(1, page_num+1):
            update_page_num(driver, i)
            time.sleep(SLEEP_TIME)
            urls.extend(get_item_urls(driver))

        results = list()
        for i_url in item_urls:
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            results.append(get_item_info(driver))

        pd.DataFrame(results).to_csv(CSV_NAME)

    finally:
        driver.quit()