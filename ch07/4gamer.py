# -*- coding: utf-8 -*-

"""
ゲーム情報を取得する
"""
import datetime
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 分単位で掲載されることがあるので、実際のサイトと取得できるものが異なる場合がある

# 各記事のURLを格納するリスト
article_url = list()
# 掲載日を格納するリスト
publication_date_list = list()
# 記事名を格納するリスト
article_name_list = list()
# 記事の内容を格納するリスト
desc_list = list()
# 情報取得日を格納するリスト
scraping_date_list = list()
# 各記事の現在のURLを格納するリスト
url_list = list()

def main():
    option = Options()
    option.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    get_article_urls(driver)

    for url in tqdm(article_url):
        option = Options()
        option.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        get_article_info(driver, url)
        
    # DataFrame型を作成
    df = pd.DataFrame({
        '掲載日':publication_date_list,
        '記事名':article_name_list,
        '記事内容':desc_list,
        '情報取得日':scraping_date_list,
        'URL':url_list
    })

    # CSVへ出力
    df.to_csv('output/4gamer.csv', encoding='utf_8_sig')

def get_article_urls(driver):
    url = 'https://www.4gamer.net/'
    driver.get(url)
    
    for num in tqdm(range(1, 2)):
        driver.implicitly_wait(10)
        select_day = driver.find_element(By.ID, f'NEWS_SELECT_DAY_{num}')
        articles = select_day.find_elements(By.XPATH, 'div')
        # データの量を減らす
        articles = articles[:2]

        for article in articles:
            v2_article_tags = article.find_elements(By.CLASS_NAME, 'V2_article_tag')
            for v2_article_tag in v2_article_tags:
                if '広告企画' in v2_article_tag.get_attribute('innerHTML'):
                    pass
                else:
                    h2_tag = article.find_element(By.TAG_NAME, 'h2')
                    a_tag = h2_tag.find_element(By.TAG_NAME, 'a')
                    article_url.append(a_tag.get_attribute('href'))
    driver.quit()

def get_article_info(driver, url):
    driver.get(url)
    try:
        # 掲載日
        finding = driver.find_element(By.CLASS_NAME, 'finding')
        publication_date_list.append(finding.find_element(By.TAG_NAME, 'span').text)

    except:
        # 書き方が違う場合
        publication_date_list.append(driver.find_element(By.CLASS_NAME, 'uptime').text)
    
    finally:
        # 記事名
        main_contents = driver.find_element(By.CLASS_NAME, 'main_contents')
        container = main_contents.find_element(By.CLASS_NAME, 'container')
        article_name_list.append(container.find_element(By.TAG_NAME, 'h1').text)
        
        # 記事
        num = list(filter(None, driver.current_url.split('/')))[-1]
        f = open(f'./output/4gamer/{num}.txt', 'w')
        f.write(container.find_element(By.CLASS_NAME, 'maintxt').text)
        f.close()
        desc_list.append(f'{num}.txt')
        
        # スクレイピング日
        scraping_date_list.append(datetime.datetime.now().date())
        
        # URL
        url_list.append(driver.current_url)
        
        # 終了
        driver.quit()
if __name__ == '__main__':
    main()
