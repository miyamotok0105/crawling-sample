import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 10
CSV_NAME = "netflix_end.csv"

def get_info(driver):
    results = list()
    day_elements = driver.find_elements(By.CLASS_NAME, "date-cc")
    print(f"day_elements:{day_elements}")
    for i_day in day_elements:
        date = i_day.find_element(By.CLASS_NAME, "newtoto2").text
        contens_elements = i_day.find_elements(By.CSS_SELECTOR, "div.mark89 > div")
        print(f"contens_elements:{contens_elements}")
        for i_content in contens_elements:
            content_result = dict()
            content_result["date"] = date
            title_element = i_content.find_element(By.CLASS_NAME, "sche-npp-txt")
            content_result["title"] = title_element.text
            content_result["url"] = title_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            content_result["season"] = i_content.find_element(By.CLASS_NAME, "sche-npp-seas").text
            content_result["genre"] = i_content.find_element(By.CLASS_NAME, "sche-npp-gen").text
            results.append(content_result)
    return results

if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        target_url = "https://www.net-frx.com/p/netflix-coming-soon.html"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)

        result = get_info(driver)

        pd.DataFrame(result).to_csv(CSV_NAME)
        print(pd.DataFrame(result))
    
    finally:
        driver.quit()
