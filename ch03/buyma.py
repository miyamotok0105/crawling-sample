import time
import requests
import datetime
from tqdm import tqdm
import logging
from logging import config, getLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
import configparser

def update_page_num(driver, search_word, page_num):
    """
    検索結果のページを次のページへ更新する。

    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver
      
    pagenum:int
      更新後のページ数
    """

    base_url = "https://www.buyma.com/r/"
    next_url = base_url + search_word + f"_{page_num}"
    driver.get(next_url)

def get_item_urls(driver):
    """
    検索結果のページから商品のURLのみを取得する
    
    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver

    Returns
    --------------------------------------
    """
    a_tag_elements = driver.find_elements(by=By.TAG_NAME, value="a")
    hrefs = [i.get_attribute("href") for i in a_tag_elements]
    hrefs = [i for i in hrefs if not i == None]
    result = [i for i in hrefs if "item" in i]
    return result

def get_item_info(driver):
    """
    商品ページから必要なデータを取得し、
    結果を専用のデータ型に書き込み返す。

    PArameters
    ---------------------------------
    driver:
      商品紹介ページを表示した状態のchrome driver
      
    Returns
    ---------------------------------
    result: 
      データを纏めたオブジェクト
    """
     # id
    result.id = driver.current_url.split("/")[-1]
    # datetime
    now = datetime.datetime.now()
    result.datetime = now.strftime('%y/%m/%d %H:%M:%S')    
    # title
    title_element = driver.find_element(By.CSS_SELECTOR, '#item-info > section:nth-child(1) > div.mer-spacing-b-12 > mer-heading')
    result.title = title_element.text
    # price
    price_element = driver.find_element(By.CSS_SELECTOR, "#item-info > section:nth-child(1) > section:nth-child(2) > div > mer-price")
    result.price = price_element.text
    # description
    description_element = driver.find_element(By.CSS_SELECTOR, "#item-info > section:nth-child(2) > mer-show-more > mer-text")
    result.description = description_element.text
    # sip cost
    postage_sections = driver.find_element(By.CSS_SELECTOR, "#item-info > section.layout__StyledSection-sc-1lyi7xi-7.kdAFPN > div > mer-display-row:nth-child(4) > span:nth-child(2)")
    result.postage = postage_sections.text
    # images 


    
if __name__=="__main__":
    # try:
        logger = getLogger(__name__)
        formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        fh = logging.FileHandler('spam.log') # logファイルの
        logger.addHandler(fh)

        # 運用後に変更が考えられる変数は外部ファイルで操作したい
        logger.info("start crawling")
        # config_ini = configparser.ConfigParser()
        # config_ini.read('config.ini', encoding='utf-8')
        
        # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") # ここは要調整
        # driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver") # ここは要調整
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
 
        # ドライバー指定でChromeブラウザを開く


        driver = webdriver.Chrome(ChromeDriverManager().install())

        # chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        # driver = webdriver.Chrome(service=chrome_service)
                
        
        
        base_url = "https://www.buyma.com/r/"
        search_word = "ネクタイ%20細い"
        target_url = base_url + search_word # 検索後の画面が出てくるURL
        driver.get(target_url)   
        first_page_url = driver.current_url

        time.sleep(5)


        # 収集対象のURLを取得する

        logger.info("start scrape item urls.")
        page_num=0
        item_urls = list()
        while True:   # ページ数がわかるならforがいい。tqdm使えるし。
            time.sleep(3) 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            page_num+=1
            update_page_num(driver, search_word, page_num)
            print(driver.current_url, first_page_url)
            if driver.current_url.lower() == first_page_url: # 最終ページ
                break

        # 商品ごとに収集する
        item_infos = list()
        logger.info("start scrape item info.")
        for i_url in tqdm(item_urls):
            driver.get(i_url)   
            time.sleep(5)
            item_infos.append(get_item_info(driver))

        # except Exception as e :
        # #     logger.error(e)       
        # finally:
        #   driver.quit()
        #   logger.info('end crawring')       