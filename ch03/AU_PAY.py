# -*- coding: utf-8 -*-

"""
削除？？？

AU Payマーケットのデータを取得する
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
import pandas as pd

PRODUCT_COUNT = 40

def update_page_num(page_num):
        page_num = page_num + 1
        return page_num

def get_item_urls(driver,page_num):
    url = f'https://wowma.jp/itemlist?e_scope=O&at=FP&non_gr=ex&spe_id=c_act_sc03&e=tsrc_topa_m&ipp=40&keyword=%83%7D%83%8A%83I%83X%83g%83%89%83C%83J%81%5B%83Y&page={page_num}&clk={page_num}'
    driver.get(url)
        
    time.sleep(1)
    element_class_list = driver.find_elements(By.CLASS_NAME, 'productItem') 

    time.sleep(1)
    for elem in element_class_list:
        elem_a = elem.find_element(By.TAG_NAME,'a')
        url_list.append(elem_a.get_attribute('href'))
    driver.quit()

def get_item_info(driver,url):
    driver.get(url)
    time.sleep(1)
    
    # 商品名
    table = driver.find_element(By.CLASS_NAME, 'pb20')
    item_name_list.append(table.find_element(By.CLASS_NAME, 'name').text)
    # ID
    item_id_list.append(driver.current_url)
    # 価格
    time.sleep(1)
    item_price_list.append(driver.find_element(By.ID, 'js-baseItemPrice').text)
    
    # 説明
    try:
        time.sleep(1)
        item_desc_list.append(driver.find_element(By.ID, 'itemSuperDetailAra').text)
    except:
        desc_table = driver.find_element(By.CLASS_NAME, 'fixedWidth')
        item_desc_list.append(desc_table.find_element(By.CLASS_NAME, 'inner').text)
    
    # 時間
    item_time_list.append(datetime.datetime.now().date())
    
    # URL
    item_url_list.append(driver.current_url)
    
    # 終了
    driver.quit()
    

# 商品URLを含んだクラスを保存するリスト
element_class_list = []

url_list = []
item_name_list = []
item_id_list = []
item_price_list = []
item_desc_list = []
item_time_list = []
item_url_list = []

driver = webdriver.Chrome()
url = 'https://wowma.jp/itemlist?e_scope=O&at=FP&non_gr=ex&spe_id=c_act_sc03&e=tsrc_topa_m&ipp=40&keyword=%83%7D%83%8A%83I%83X%83g%83%89%83C%83J%81%5B%83Y&page=1&clk=1'
driver.get(url)

# ページが何枚あるか数える
time.sleep(1)
real_page_table = driver.find_element(By.CLASS_NAME,'-headingSeachCount--headingSeachCount--1lTdy-')
real_page = int(real_page_table.find_element(By.TAG_NAME, 'span').text)
real_page = real_page // 40
driver.quit()

page_num = 1
while(page_num <= real_page + 1):
    time.sleep(1)
    driver = webdriver.Chrome()
    get_item_urls(driver,page_num)
    page_num = update_page_num(page_num)

# 商品情報取得
for url in url_list:
    time.sleep(3)
    driver = webdriver.Chrome()
    get_item_info(driver,url)

# 重複削除
# 1ページ内に重複するものが存在するのですが、うまく削除できなかったです。

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
df.to_csv('AuPay_result.csv', encoding='utf_8_sig')