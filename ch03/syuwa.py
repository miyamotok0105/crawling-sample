import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs


class Syuwa_scraper:
    def __init__(self):
        # configから
        self.base_url = "https://www.shuwasystem.co.jp/search/index.php?search_genre=13280"
        
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver" # ここをconfigfileで
        # v4では以下の書き方になるらしい
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        self.driver = webdriver.Chrome(service=chrome_service)
    
    def update_page_num(self, page_num):
        """
        検索結果のページを次のページへ更新する。
    
        Parameters
        --------------------------------------
        pagenum:int
          更新後のページ数
        """
        base_url = "https://www.shuwasystem.co.jp/search/index.php?search_genre=13280"
        page_option = f"&page={page_num}"
        next_url = base_url + page_option
        self.driver.get(next_url)

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
        try:
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
          
        finally:
            self.driver.quit()  

if __name__=="__main__":
    scraper = Syuwa_scraper()
    scraper.scraping()