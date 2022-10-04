import time
import datetime
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 2

def scrap_headline():
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        target_url = "https://www.yomiuri.co.jp/"
        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        today = datetime.datetime.now().strftime('%y:%m:%d:%H:%M:%S')
        csv_name = f"yomiuri_{today}.csv"

        headline_element = driver.find_element(By.CLASS_NAME, "headline")
        article_elements = headline_element.find_elements(By.TAG_NAME, "article")
        title_elements = [i.find_element(By.TAG_NAME, "h3") for i in article_elements]
        titles = [i.text for i in title_elements]
        urls = [i.find_element(By.TAG_NAME, "a").get_attribute("href") for i in title_elements]

        with open(csv_name, "a") as f:
            for i_title, i_url in zip(titles, urls):
                f.write(f"{i_title},{i_url}\n")
    finally:
        driver.quit()

if __name__=="__main__":
  scrap_headline()