import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import pandas as pd

if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        CSV_NAME = "tmp.csv"

        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        

        page_urls = list()
        for i_pagenum in range(1,6):
            time.sleep(10)

            base_url = f"https://prtimes.jp/main/html/index/pagenum/{i_pagenum}"
            driver.get(base_url)
            
            # レビューごとの要素
            article_urls = [i.get_attribute("href") for i in driver.find_elements(By.CLASS_NAME, "list-article__link")]
            print(len(article_urls))
            page_urls.extend(article_urls)

        results = list()
        for i_url in page_urls:
            row_result = dict()
            driver.get(i_url)
            time.sleep(5)
            
            row_result["id"] = os.path.splitext(i_url.split("/")[-1])[0]
            row_result["url"] = i_url
            row_result["title"] = driver.find_element(By.CLASS_NAME, "release--title").text
            row_result["company"] = driver.find_element(By.CLASS_NAME, "company-name").text
            row_result["datetime"] = driver.find_element(By.TAG_NAME, "time").text
            row_result["abstruct"] = driver.find_element(By.CLASS_NAME, "r-head").text

            result.append(row_result)
            with open(f"{row_result['id']}.txt", "w") as f:
                main_text = driver.find_element(By.CLASS_NAME, "rich-text").text
                f.write(main_text)
            
            print(row_result)
    finally:
        driver.quit()

    df = pd.DataFrame(results)
    df.to_csv("tmp.csv")