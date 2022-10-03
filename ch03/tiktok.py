import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import pandas as pd

SLEEP_TIME = 5
SCROLL_NUM = 5
CSV_NAME = "tiktok.csv"
if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        base_url = "https://www.tiktok.com/@tv_asahi_news"
        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(base_url)
        
        time.sleep(SLEEP_TIME)

        for i in range(SCROLL_NUM): 
            time.sleep(SLEEP_TIME)
            driver.execute_script("window.scrollBy(0, 6000);")

        prosuct_elements = driver.find_elements(By.CSS_SELECTOR, ".tiktok-x6y88p-DivItemContainerV2.e19c29qe7")

        results = list()
        for i_section in prosuct_elements:
            result_row = dict()
            a_element = i_section.find_element(By.CSS_SELECTOR, "div > div > div > a")
            result_row["url"] = a_element.get_attribute("href")
            img_element = i_section.find_element(By.CSS_SELECTOR, "div > div > div > a > div > div > img")
            result_row["name"] = img_element.get_attribute("alt")
            results.append(result_row)

        pd.DataFrame(results).to_csv(CSV_NAME)
    finally:
        driver.quit()
