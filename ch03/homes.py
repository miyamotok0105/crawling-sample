# -*- coding: utf-8 -*-

"""
Home’sから物件情報取得
"""
import time
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 5
CSV_NAME = "./output/homes.csv"

def update_page_num(driver, page_num):
    base_url = "https://www.homes.co.jp/chintai/tokyo/list/"
    next_url = base_url + f"?page={page_num}"
    driver.get(next_url)
    time.sleep(SLEEP_TIME)

def get_item_urls(driver):
    detail_elements = driver.find_elements(By.CSS_SELECTOR, ".anchor.prg-detailAnchor")
    return [i.get_attribute("href") for i in detail_elements]

def is_last_page(driver):
    inner_element = driver.find_element(By.CLASS_NAME, 'inner')
    return len(inner_element.find_elements(By.CLASS_NAME, "nextPage")) == 0

    
def get_item_info(driver):
    table_element = driver.find_element(By.CSS_SELECTOR, ".vertical.col4")
    th_elements = table_element.find_elements(By.TAG_NAME, "th")
    td_elements = table_element.find_elements(By.TAG_NAME, "td")
    result = {k.text:v.text for k,v in zip(th_elements, td_elements)}

    result["賃料（管理費等）"] = table_element.find_element(By.CLASS_NAME, "price").text
    result["入居可能時期"] = table_element.find_element(By.CLASS_NAME, "spec").text
    return result


if __name__=="__main__":
    try:
        # chrome_options = Options()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver", options=chrome_options)
        # driver.get('https://www.google.nl/')

        target_url = "https://www.homes.co.jp/chintai/tokyo/list/?cond%5Broseneki%5D%5B43704833%5D=43704833&cond%5Bmonthmoneyroomh%5D=0&cond%5Bhousearea%5D=0&cond%5Bhouseageh%5D=0&cond%5Bwalkminutesh%5D=0&bukken_attr%5Bcategory%5D=chintai&bukken_attr%5Bpref%5D=13" # 検索後の画面が出てくるURL
        driver.get(target_url)   
        time.sleep(SLEEP_TIME)

<<<<<<< HEAD
        time.sleep(5)

        # ページ設定
        # 賃料
        price_element = driver.find_element(By.ID,'cond_monthmoneyroomh')
        price_select_object = Select(price_element)
        price_select_object.select_by_value('6.0')

        time.sleep(5)
        # 間取り
        floor_element = driver.find_element(By.ID,'cond_madori_13')
        if not floor_element.is_selected():
              floor_element.click()
        # 収集対象のURLを取得する
        # logger.info("start scrape item urls.")
        page_num = 0
=======
        price_element = driver.find_element(By.ID,'cond_monthmoneyroomh')
        price_select_object = Select(price_element)
        price_select_object.select_by_value('6.0')
        time.sleep(SLEEP_TIME)
        floor_element = driver.find_element(By.ID,'cond_madori_13')
        if not floor_element.is_selected():
              floor_element.click()
        time.sleep(SLEEP_TIME)

        page_num=0
>>>>>>> 2fd05722fcb0d9623b29c2c3a04eea0711d98ea6
        item_urls = list()
        while True: 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            print(urls)
            if is_last_page(driver):
                break
            else:
                page_num+=1
                update_page_num(driver, page_num)

        item_infos = list()
<<<<<<< HEAD
        # データの量を減らす
        item_urls = item_urls[:5]

        # logger.info("start scrape item info.")
=======
>>>>>>> 2fd05722fcb0d9623b29c2c3a04eea0711d98ea6
        for i_url in item_urls:
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            item_infos.append(get_item_info(driver))
        
<<<<<<< HEAD
        # return item_infos
    
    finally:
        # driver.save_screenshot('screenie.png')
        driver.quit()

    print(item_infos)
    df = pd.DataFrame(item_infos)
    df.to_csv(CSV_NAME, index=False)



if __name__=="__main__":
  scraping()
=======
        pd.DataFrame(item_infos).to_csv(CSV_NAME, index=False)
    
    finally:
        driver.quit()
>>>>>>> 2fd05722fcb0d9623b29c2c3a04eea0711d98ea6
