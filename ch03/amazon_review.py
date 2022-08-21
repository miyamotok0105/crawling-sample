import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import pandas as pd

if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        CSV_NAME = "tmp.csv"

        base_url = "https://www.amazon.co.jp/Novation-NOVSYNTH02UKEU-%E3%82%B7%E3%83%B3%E3%82%BB%E3%82%B5%E3%82%A4%E3%82%B6%E3%83%BC-MiniNova/product-reviews/B0096MEKZ4/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(base_url)
        
        time.sleep(5)
        
        # レビューごとの要素
        revie_elements = driver.find_elements(By.CSS_SELECTOR, ".a-section.review.aok-relative")
        
        results = list()
        for i_section in revie_elements:
            result_row = dict()
            # タイトル
            result_row["title"] = i_section.find_element(By.CSS_SELECTOR, ".a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold").text
            # テキスト
            result_row["text"] = i_section.find_element(By.CSS_SELECTOR, ".a-row.a-spacing-small.review-data").text
            # 星の取得
            # a_raw_element = i_section.find_element(By.CLASS_NAME,"a-row")
            result_row["star"] = i_section.find_element(By.TAG_NAME, "i").find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
            results.append(result_row)
    
    finally:
        driver.quit()

    df = pd.DataFrame(results)
    df.to_csv("tmp.csv")