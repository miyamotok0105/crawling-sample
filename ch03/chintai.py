import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

def update_page_num(driver, page_num):
    """
    検索結果のページを次のページへ更新する。

    Parameters
    --------------------------------------
    pagenum:int
      更新後のページ数
    """
    pager_element = driver.find_element(By.CLASS_NAME, "list_pager")
    nextbutton_element = pager_element.find_element(By.CLASS_NAME, "next")
    nextbutton_element.click()

def get_item_urls(self):
    """
    検索結果のページから商品のURLのみを取得する
    
    Returns
    --------------------------------------
    result: list[str]
        商品ページを纏めたもの
    """
    ro_element = self.driver.find_element(By.CLASS_NAME, "bookWrap")
    ttl_elements = ro_element.find_elements(By.CLASS_NAME, "ttl")
    a_elements = [i.find_element(By.TAG_NAME, "a") for i in ttl_elements]
    return [i.get_attribute("href") for i in a_elements]
def get_item_info(self):
    """
    商品ページから必要なデータを取得し、
    結果を専用のデータ型に書き込み返す。
      
    Returns
    ---------------------------------
    result: list[items]"
      データを纏めたオブジェクト
    """
    result = dict()
    # title
    titie_element = self.driver.find_element(By.CLASS_NAME, "titleWrap")
    result["title"] = titie_element.text
    # price
    price_element = self.driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/div[2]/table/tbody/tr[6]/td')
    result["price"] = price_element.text
    
    # author
    author_element = self.driver.find_element(By.CSS_SELECTOR, "#main > div.detail > div.right > table > tbody > tr:nth-child(1) > td > a")
    result["author"] = author_element.text
    
    # describe
    describe_element = self.driver.find_element(By.ID, "bookSample")
    result["describe"] = describe_element.text
    
    print(result)
    return result
def is_last_page(self):
    """
    driverの画面が最終ページか判断する関数
    Returns
    ------------------------------------
    result: bool
      最終ページの場合
    """
    pagingWrap_element = self.driver.find_element(By.CLASS_NAME, "pagingWrap")
    paging_text = pagingWrap_element.find_element(By.CLASS_NAME, "right").text
    
    return not "次" in paging_text
def scraping(self):
    """
    上記コードを組み合わせて、クローリング&スクレーピングを行う

    Returns 
    ----------------------------------------
    item_infos:
        商品データを纏めたデータ型のリスト
    """
    
    self.base_url = "https://www.chintai.net/list/?o=10&pageNoDisp=20%E4%BB%B6&o=10&rt=51&prefkey=tokyo&ue=000004864&urlType=dynamic&cf=0&ct=60&k=1&m=2&jk=0&jl=0&sf=0&st=0&j=&h=99&b=1&b=2&b=3&jks="
    
    CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver" # ここをconfigfileで
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    self.driver = webdriver.Chrome(service=chrome_service)

    # 運用後に変更が考えられる変数は外部ファイルで操作したい
    self.driver.get(self.base_url)   
    time.sleep(10)

    # 収集対象のURLを取得する
    page_num = 1
    item_urls = list()
    while True:   # ページ数がわかるならforがいい。tqdm使えるし。
        time.sleep(5) 
        urls = self.get_item_urls()
        print(urls)
        item_urls.extend(urls)
        if self.is_last_page(): # 最終ページ
            break
        else:
            page_num+=1
            self.update_page_num(page_num)
    # 商品ごとに収集する
    item_infos = list()
    for i_url in item_urls:
        self.driver.get(i_url)   
        time.sleep(5)
        item_infos.append(self.get_item_info())
    
    return item_infos
      
if __name__=="__main__":
    scraper = Syuwa_scraper()
    scraper.scraping()