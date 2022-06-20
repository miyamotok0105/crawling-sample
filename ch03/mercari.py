import time
import requests
from tqdm import tqdm
from logging import config, getLogger
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

    
class Mercari_item_info:
    id = None
    datetime = None
    title = None
    price = None
    postage = None
    description = None
    image_urls = list()

def export_csv(item_infos, out_path):
    info_vec_2d = 
    columns = ["id", "title", "price", "postage", "description", ""]
    df = pd.Dataframe(info_vec_2d)
    df.to_csv(out_path)
    

def update_page_num(driver, page_num):
    page_option = f"&page_token=v1%3A{page_num}"
    driver.get(target_url + page_option)

def get_item_urls(driver):
    a_tag_elements = driver.find_elements_by_tag_name("a")
    hrefs = [i.get_attribute("href") for i in a_tag_elements]
    item_urls = [i for i in hrefs if "item" in i]
    return item_urls

def get_item_info(driver):
    result = Mercari_item_info()

    # id
    # datetime

    # title
    title_element = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > mer-heading')
    print(f"title_sections: {title_element}")             
    title = title_element.text
    result.title = title
    print(f"title: {title}")
    print("="*100)
    
    # price
    price_element = driver.find_element(By.CSS_SELECTOR, "#item-info > section:nth-child(1) > section:nth-child(2) > div > mer-price")
    print(f"title_sections: {price_element}")
    price = price_element.text
    result.price = price
    print(f"title: {price}")
    print("="*100)
    
    # description
    description_element = driver.find_element(By.CSS_SELECTOR, "#item-info > section:nth-child(2) > mer-show-more > mer-text")
    description = description_element.text
    result.description = description
    print(f"description: {description}")
    print("="*100)

    # sip cost
    postage_sections = driver.find_element(By.CSS_SELECTOR, "#item-info > section.layout__StyledSection-sc-1lyi7xi-7.kdAFPN > div > mer-display-row:nth-child(4) > span:nth-child(2)")
    postage = postage_sections.text
    result.postage = postage
    print(f"description: {postage}")
    print("="*100)

    # title = driver.find_elements_by_tag_name()
    # images 
    images_section= driver.find_elements(By.CLASS_NAME, "sticky-inner-wrapper")[0]
    image_tags = images_section.find_elements(By.TAG_NAME, "mer-item-thumbnail")
    srcs = list(set([i.get_attribute("src") for i in image_tags]))
    result.image_urls.extend(srcs)
    return result

if __name__=="__main__":
    try:
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        target_url = "https://jp.mercari.com/search?keyword=novation&t1_category_id=1328&status=on_sale&category_id=79"
        driver.get(target_url)   

        time.sleep(10)
        page_num=0
        item_urls = list()
        while True:
            print(f"======== {page_num} ===================")
            time.sleep(5)
            urls = get_item_urls(driver)
            if len(urls) < 1: # 最終ページ
                break
            else:
                print(urls)
                print(len(urls))
                item_urls.extend(urls)
                page_num+=1
                update_page_num(driver, page_num)

        item_infos = list()
        for i_url in tqdm(item_urls):
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))


    except Exception as e :
        print(f"======{}")        
    finally:
        driver.quit()