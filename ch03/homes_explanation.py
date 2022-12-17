import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import configparser
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.select import Select
import pandas as pd 

class Suumo_item:
      name = None
      price = None
      floor_plan = None
      address = None
      url = None


def update_page_num(driver, page_num):
    """
    検索結果のページを次のページへ更新する。

    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver
      
    pagenum:int
      更新後のページ数
    """
    base_url = "https://www.homes.co.jp/chintai/tokyo/list/?page=2"
    next_url = base_url + f"?page={page_num}"
    driver.get(next_url)


def get_item_urls(driver):
    """
    検索結果のペ1ージから商品のURLのみを取得する
    
    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver
    Returns
    --------------------------------------
    
    """
    detail_elements = driver.find_elements(By.CLASS_NAME, "detail")
    hrefs = list()
    for i in detail_elements:
          try:
            a_element = i.find_element(By.TAG_NAME,"a")
            hrefs.append(a_element.get_attribute("href"))
          except:
            pass
    return hrefs

def is_last_page(driver):
    paging_element = driver.find_element(By.XPATH, '//*[@id="searchResult"]/div[3]')
    print(paging_element.text)
    return not "次" in paging_element.text

def set_option(driver):
    """
    オプションを設定するためにドライバをいじる関数
    
    Parameters
    --------------------------------------
    driver:
      商品一覧ページを表示した状態のchrome driver
    """
    # 要素の選択
    select_object.select_by_value('value1')
    
def get_item_info(driver):
    """
    商品ページから必要なデータを取得し、
    結果を専用のデータ型に書き込み返す。
    Parameters
    ---------------------------------
    driver:
      商品紹介ページを表示した状態のchrome driver
      
    Returns
    ---------------------------------
    result: 
      データを纏めたオブジェクト
    """
    #mainContents > div:nth-child(8) > div.mt20 > table.mt15.bdGrayT.bdGrayL.bgWhite.pCell10.bdclps.wf
    # get table tag 
    # table_element = driver.find_element(By.CLASS_NAME, ".mt15.bdGrayT.bdGrayL.bgWhite.pCell10.bdclps.wf")
    table_element = driver.find_element(By.CSS_SELECTOR, ".mt15.bdGrayT.bdGrayL.bgWhite.pCell10.bdclps.wf")
    df = pd.read_html(table_element.get_attribute("outerHTML"))[0]
    
    # 
    first_df = df.iloc[:, :2]
    # first_df.iloc[:,0] = [i.replace("  ヒント", "") for i in first_df.iloc[:,0].tolist()]
    keys = [i.replace("  ヒント", "") for i in first_df.iloc[:,0].tolist()]
    vals = first_df.iloc[:,1].tolist()
    ({i_key:i_val for i_key, i_val in zip(keys, vals)})
    second_df = df.iloc[:, 2:]

    # print(first_df)
    # print(second_df)
    # 物件名
    # 価格
    # 間取り
    # 住所
    # URL


def scraping():
    """
    上記コードを組み合わせて、クローリング&スクレーピングを行う

    Returns 
    ----------------------------------------
    item_infos:
        商品データを纏めたデータ型のリスト
    """

    try:
        # logger = getLogger(__name__)
        # formatter = '[%(levelname)s] %(asctime)s %(filename)s.%(funcName)s.l%(lineno)d: %(message)s'
        # logging.basicConfig(level=logging.INFO, format=formatter)
        # fh = logging.FileHandler('spam.log') # logファイルの
        # logger.addHandler(fh)3

        # 運用後に変更が考えられる変数は外部ファイルで操作したい
        # logger.info("start crawling")
        # config_ini = configparser.ConfigParser()
        # config_ini.read('config.ini', encoding='utf-8')

        # v4では以下の書き方になるらしい
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/home/nanashino/Downloads/chromedriver",options=chrome_options)
        # driver.get('https://www.google.nl/')

        target_url = "https://www.homes.co.jp/chintai/tokyo/list/?cond%5Broseneki%5D%5B43704833%5D=43704833&cond%5Bmonthmoneyroomh%5D=0&cond%5Bhousearea%5D=0&cond%5Bhouseageh%5D=0&cond%5Bwalkminutesh%5D=0&bukken_attr%5Bcategory%5D=chintai&bukken_attr%5Bpref%5D=13" # 検索後の画面が出てくるURL
        driver.get(target_url)   

        time.sleep(15)

        # ページ設定
        # 賃料
        price_element = driver.find_element(By.ID,'cond_monthmoneyroomh')
        price_select_object = Select(price_element)
        price_select_object.select_by_value('6.0')

        time.sleep(13)
        # 間取り
        floor_element = driver.find_element(By.ID,'cond_madori_13')
        if not floor_element.is_selected():
              floor_element.click()



        # 収集対象のURLを取得する
        # logger.info("start scrape item urls.")
        page_num=0
        item_urls = list()
        while True:   # ページ数がわかるならforがいい。tqdm使えるし。
            time.sleep(5) 
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            print(urls)
            if is_last_page(driver): # 最終ページ
                break
            else:
                page_num+=1
                update_page_num(driver, page_num)

        # 商品ごとに収集する
        item_infos = list()
        # logger.info("start scrape item info.")
        for i_url in item_urls:
            print(i_url)
            time.sleep(1)
            driver.get(i_url)   
            item_infos.append(get_item_info(driver))
        
        return item_infos
    
    finally:
      pass
        # driver.quit()
        # logger.info('end crawring')       


if __name__=="__main__":
  scraping()
