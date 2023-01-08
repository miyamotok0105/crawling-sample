# -*- coding: utf-8 -*-

"""
リクナビNEXTのから「Django」で検索したデータを取得する
"""
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 3
SEARCH_WORD = "Django"
CSV_NAME = "output/rikunabi.csv"

def update_page_num(driver):
    ul_element = driver.find_element(By.CSS_SELECTOR, ".rnn-pagination.rnn-textRight")
    a_element = ul_element.find_elements(By.TAG_NAME, "a")[-1]
    driver.get(a_element.get_attribute("href"))
    time.sleep(SLEEP_TIME)

def get_item_urls(driver):
    elements = driver.find_elements(By.CLASS_NAME, "rnn-linkText--black")
    item_urls = [i.get_attribute('href') for i in elements]
    return item_urls

def get_normal_info(driver):
    info_element = driver.find_element(By.CLASS_NAME, "rn3-topSummaryWrapper")
    keys = [i.text for i in info_element.find_elements(By.CLASS_NAME, "rn3-topSummaryTitle")]
    values = [i.text for i in info_element.find_elements(By.CLASS_NAME, "rn3-topSummaryText")]
    return {k:v for k,v in zip(keys, values)}

def get_rcn_info(driver):
    table_html = driver.find_element(By.CLASS_NAME, "rnn-detailTable").get_attribute("outerHTML")
    df = pd.read_html(table_html)[0]
    return {i_row[0]:i_row[1] for _, i_row in df.iterrows()}



if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=srch_submitbtn")
        time.sleep(SLEEP_TIME)
        
        input_element = driver.find_element(By.CLASS_NAME, "rnn-header__search__inner").find_element(By.TAG_NAME, "input")
        input_element.send_keys(SEARCH_WORD) 
        button_element = driver.find_element(By.CSS_SELECTOR, ".rnn-header__search__keywordButton.js-submitKeyword")
        button_element.click()
        time.sleep(SLEEP_TIME)

        total_num = int(driver.find_element(By.CSS_SELECTOR, ".rnn-pageNumber.rnn-textXl").text)
        total_page_num = total_num // 50 +1

        project_urls = list()
        for _ in range(total_page_num):
            project_urls.extend(get_item_urls(driver))
            update_page_num(driver)

        result = list()
        rnc_result = list()
        for i_url in project_urls:
            template_type = i_url.split("/")[3]
            if template_type == "rnc":
                driver.get(i_url)
                time.sleep(SLEEP_TIME)
                test = get_rcn_info(driver)
                print(test)
                rnc_result.append(test)
            else: 
                url_list = i_url.split("/")
                url_list[-2] = url_list[-2].replace("nx1", "nx2")
                driver.get("/".join(url_list[:-1]))
                time.sleep(SLEEP_TIME)
                test = get_normal_info(driver)
                print(test)
                result.append(test)
        pd.DataFrame(result).to_csv(CSV_NAME)
        pd.DataFrame(rnc_result).to_csv(CSV_NAME.replace(".csv", ""))
    finally:
        driver.quit()