# -*- coding: utf-8 -*-

"""
M&A案件一覧を取得する（事業を売る）
"""
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs 

SLEEP_TIME = 3
GET_PAGE_NUM = 3 # Noneなら全件
CSV_NAME = "./output/tranbi_sell.csv"

def update_page_num(driver, page_num):
    base_url = "https://www.tranbi.com/sell/list/"
    url = base_url + f"?page={page_num}"
    driver.get(url)

def get_project_url(driver):
    project_list_element = driver.find_element(By.CSS_SELECTOR, ".buylistArea.js-toggle-bookmark-area")
    a_elements = project_list_element.find_elements(By.TAG_NAME, "a") 
    hrefs = [i.get_attribute("href") for i in a_elements]
    return [ i for i in hrefs if "detail" in i ]

def get_info(driver):
    result = list()
    project_elements = driver.find_elements(By.CLASS_NAME, "needsOfferCard")
    for i_element in project_elements:
        enterprise_list = i_element.find_elements(By.CLASS_NAME, "needsOfferCard__list")
        if len(enterprise_list) == 1:
            keys = enterprise_list[0].find_elements(By.CLASS_NAME, "needsOfferCard__listHead")
            values = enterprise_list[0].find_elements(By.CLASS_NAME, "needsOfferCard__listBody")
        else:
            personal_list = driver.find_elements(By.CSS_SELECTOR, ".needsOfferCard__list.has-list")[0]
            keys = personal_list.find_elements(By.CLASS_NAME, "needsOfferCard__listHead")
            values = personal_list.find_elements(By.CLASS_NAME, "needsOfferCard__listBody")
        row_data = {k.text:v.text for k,v in zip(keys, values)}
        
        needs_elements = i_element.find_elements(By.CLASS_NAME, "needsOfferCard__needsInfo")
        needs_result = list()
        if len(needs_elements) > 0:
            needs_element = needs_elements[0]
            needs_dl_element = needs_element.find_elements(By.TAG_NAME, "dl")
            for i_table in needs_dl_element:
                keys_elements = needs_elements[0].find_elements(By.CLASS_NAME, "needsOfferCard__listHead")
                values_elements = needs_elements[0].find_elements(By.CLASS_NAME, "needsOfferCard__listBody")
                keys = [i.text for i in keys_elements]
                keys[-1]  = "詳細URL"
                values = [i.find_element(By.TAG_NAME, "a").get_attribute("href") if i.text=="詳細" else i.text for i in values_elements]
                needs_result.append({k:v for k,v in zip(keys, values)})

            
        neko_elements = i_element.find_elements(By.CLASS_NAME, "needsOfferCard__userInterest")
        if len(neko_elements) > 0:
            row_data["coment_text"] = neko_elements[0].text
        result.append(row_data)

    return result , needs_result


if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
    
        target_url = "https://www.tranbi.com/sell/list/"
        driver.get(target_url)
        time.sleep(SLEEP_TIME)
    
        if GET_PAGE_NUM == None:
            total_num_element = driver.find_element(By.CLASS_NAME, "searchResultText").text
            page_num = int(total_num_element.replace("件", "").replace(",", "")) // 20 + 1
        else:
            page_num = GET_PAGE_NUM
    
        result = list()
        for i_page_num in range(1, page_num+1):
            update_page_num(driver, i_page_num)
            time.sleep(SLEEP_TIME)
            item_info, _ = get_info(driver)
            result.extend(item_info)
    
        pd.DataFrame(result).to_csv(CSV_NAME, index=False)
        
    finally:
        driver.quit()