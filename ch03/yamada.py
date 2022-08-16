# 必要なライブラリをインポート
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
import pandas as pd

# 1ページに表示される商品数を定数化
PRODUCT_COUNT = 20

# ページを更新する関数
def update_page_num(page_num):
    page_num = page_num + PRODUCT_COUNT
    return page_num
    
# URLを取得する関数
def get_item_urls(driver,page_num):
    url = f'https://ymall.jp/search?s9%5B%5D=yamadamobile&s9%5B%5D=ymall&s9o=1&q=COMPA&path=MALL2%3A0030_30_%E3%83%9A%E3%83%83%E3%83%88%E3%83%BB%E8%8A%B1%E3%83%BBDIY&o={page_num}'
    driver.get(url)
        
    time.sleep(1)
    element_class_item = driver.find_element(By.CLASS_NAME, 'item_list') 
    
    time.sleep(1)
    element_class_item_list = element_class_item.find_elements(By.CLASS_NAME, 'item_name')

    time.sleep(1)
    for elem in element_class_item_list:
        elem_a = elem.find_element(By.TAG_NAME,'a')
        url_list.append(elem_a.get_attribute('href'))
    driver.quit()
    
def get_item_info(driver,url):
    driver.get(url)
    time.sleep(1)
    
    if('store' in driver.current_url):
        # 商品名
        item_name_list.append(driver.find_element(By.ID,'shop_cart_name').text)
        
        # ID
        time.sleep(1)
        item_id_list.append(driver.current_url)
        
        # 商品価格
        time.sleep(1)
        item_price_list.append(driver.find_element(By.CLASS_NAME,'shop_cart_price_p').text)
        
        # 商品説明
        try:
            time.sleep(1)
            item_desc_list.append(driver.find_element(By.CLASS_NAME,'cart_detail1_left_free').text)
        
        except:
            item_desc_list.append(driver.find_element(By.CLASS_NAME,'cart_detail5_right_free').text.split('【商品説明】')[-1])
        
        # スクレイピング日付
        item_time_list.append(datetime.datetime.now().date())
        
        # URL
        item_url_list.append(driver.current_url)
        
        
    elif('kaden' in driver.current_url):
        
        # 商品名
        item_name_list.append(driver.find_element(By.CSS_SELECTOR,'.item-name.set').text)
        
        # ID
        item_id_list.append(driver.current_url)
        
        # 商品価格
        time.sleep(1)
        item_price_list.append(driver.find_element(By.CSS_SELECTOR, '.highlight.x-large').text)
        
        # 商品説明
        time.sleep(1)
        item_desc_list.append(driver.find_element(By.CSS_SELECTOR, '.item-list-vertical.line').text.split('【商品詳細】')[-1])
        
        # スクレイピング日付
        item_time_list.append(datetime.datetime.now().date())
        
        # URL
        item_url_list.append(driver.current_url)
    # 終了
    driver.quit()

# 商品URLを含んだクラスを保存するリスト
element_class_item_list = []
# 商品URLを保存するリスト
url_list = []
# 商品名を保存するリスト
item_name_list = []
# IDを保存するリスト
item_id_list = []
# 価格を保存するリスト
item_price_list = []
# 商品説明を保存するリスト
item_desc_list = []
# 情報を取得した日付を保存するリスト
item_time_list = []
# 商品URLを保存リスト
item_url_list = []

driver = webdriver.Chrome()
url = 'https://ymall.jp/search?s9%5B%5D=yamadamobile&s9%5B%5D=ymall&s9o=1&q=COMPA&path=MALL2%3A0030_30_%E3%83%9A%E3%83%83%E3%83%88%E3%83%BB%E8%8A%B1%E3%83%BBDIY&o=0'
driver.get(url)

# ページが何枚あるか数える
time.sleep(1)
real_page = int(driver.find_element(By.CLASS_NAME,'highlight').text)
driver.quit()

page_num = 0
while(page_num<=real_page):
    time.sleep(1)
    driver = webdriver.Chrome()
    # URL取得
    get_item_urls(driver,page_num)
    # ページ数更新
    page_num = update_page_num(page_num)

# 商品情報取得
for url in url_list:
    time.sleep(3)
    driver = webdriver.Chrome()
    get_item_info(driver,url)

# DataFrame型を作成
df = pd.DataFrame({
    '商品名':item_name_list,
    'ID':item_id_list,
    '価格':item_price_list,
    '説明':item_desc_list,
    '情報取得日':item_time_list,
    'URL':item_url_list
    })

# CSVへ出力
df.to_csv('yamada_result.csv', encoding='utf_8_sig')