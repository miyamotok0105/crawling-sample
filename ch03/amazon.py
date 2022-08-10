import time
import requests
import datetime
from tqdm import tqdm
import logging
from logging import config, getLogger
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class Mercari_serch_option:
    """
    """
    def __init__(self, base_url,
                 keyword,
                 order_by = None,
                 category = None,
                 sub_category_1 = None,
                 sub_category_2 = list(),
                 max_price = None,
                 min_price = None,
                 condition = None,
                 sales_status= None):
    def convert_keyword(self):
        
    self.base_url = base_url
    self.keyword = keyword.replace(" ", "%20").replace("　", "%20")
    self.order_by = None
    self.category = None
    self.sub_category_1 = None
    self.sub_category_2 = list()
    self.max_price = None
    self.min_price = None
    self.condition = None
    self.sales_status= None

    sort=created_time&order=desc # 新しい順
    sort=score # おすすめ
    order=asc&sort=price # 安い順
    sort=price&order=desc # 高い順
    order=desc&sort=num_likes


class Mercari_item_info:
    id = None
    url = None
    datetime = None
    title = None
    price = None
    stock = None
    postage = None
    description = None
    image_urls = list()

# class Mercari_scrape(Mercari_item_info, Mercari_serch_option):
    # def __init__(self):
    #     logger = getLogger(__name__)
    #     formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
    #     logging.basicConfig(level=logging.DEBUG, format=formatter)

    # def export_csv(item_infos, out_path):
    #     info_vec_2d = 
    #     columns = ["id", "title", "price", "postage", "description", ""]
    #     df = pd.Dataframe(info_vec_2d)
    #     df.to_csv(out_path)
    
def update_page_num(driver, page_num):
    page_option = f"&page={page_num}"
    driver.get(target_url + page_option)

def get_item_urls(driver):
    item_elements = driver.find_elements(By.CSS_SELECTOR, ".a-section a-spacing-base".replace(" ", "."))
    a_tag_elements = [i.find_element(By.TAG_NAME, "a") for i in item_elements]
    hrefs = [i.get_attribute("href") for i in a_tag_elements]
    item_urls = list(set(hrefs))
    return item_urls

def get_item_info(driver):
    result = Mercari_item_info()

    # id
    result.id = driver.current_url.split("/")[-2]
    result.url = driver.current_url
    # datetime
    now = datetime.datetime.now()
    result.datetime = now.strftime('%y/%m/%d %H:%M:%S')
    # title
    title_element = driver.find_element(By.ID, 'title')
    result.title = title_element.text
    # price
    price_element = driver.find_element(By.CLASS_NAME, "a-price-whole")
    result.price = price_element.text
    # is stock
    stock_element = driver.find_element(By.ID, "availability")
    result.stock = "In Stock" in stock_element.text
    # description
    description_element = driver.find_element(By.ID, "feature-bullets")
    result.description = description_element.text
    # sip cost
    try:
        postage_sections = driver.find_element(By.ID, "deliveryBlockMessage")
        result.postage = postage_sections.text
    except:
        result.postage = None
    # images 
    images_section= driver.find_element(By.ID, "imageBlock")
    image_tags = images_section.find_elements(By.TAG_NAME, "img")
    srcs = list(set([i.get_attribute("src") for i in image_tags]))
    result.image_urls.append(srcs)
    return result

    
if __name__=="__main__":
    try:
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        # target_url = "https://www.amazon.co.jp/s?k=シンセサイザー"
        target_url = "https://www.amazon.co.jp/s?k=シンセサイザー+novation"
        driver.get(target_url)   
        driver.maximize_window()

        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s / %(filename)s.%(funcName)s.L%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)

        logger.info("start scrape item urls.")
        time.sleep(5)
        page_num=1
        item_urls = list()
        while True:
            time.sleep(5)
            urls = get_item_urls(driver)
            if len(urls) < 1: # 最終ページ
                break
            else:
                item_urls.extend(urls)
                page_num+=1
                update_page_num(driver, page_num)

        item_infos = list()
        logger.info("start scrape item info.")
        for i_url in tqdm(item_urls):
            driver.get(i_url)   
            time.sleep(5)
            try:
                item_infos.append(get_item_info(driver))
            except Exception as e:
                logger.info(f"coudn't parse page.{e}(url:{i_url})")

    except Exception as e :
        logger.error(e)       
    finally:
        driver.quit()
        logger.info('end crawring')       