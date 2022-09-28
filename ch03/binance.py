import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
import pandas as pd

if __name__=="__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        CSV_NAME = "tmp.csv"

        base_url = "https://www.binance.com/ja/markets"
        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(base_url)
        
        time.sleep(5)
        
        btc_file_name = "btc.csv"
        f_btc = open(btc_file_name, "a")

        eth_file_name = "eth.csv"
        f_eth = open(eth_file_name, "a")

        usdt_file_name = "usdt.csv"
        f_usdt = open(usdt_file_name, "a")

        
        coin_elements = driver.find_elements(By.CLASS_NAME, "css-vlibs4")
            
        while True:
            btc_price = coin_elements[0].find_element(By.CSS_SELECTOR, "div > div.css-ydcgk2").text
            eth_price = coin_elements[1].find_element(By.CSS_SELECTOR, "div > div.css-ydcgk2").text
            usdt_price = coin_elements[2].find_element(By.CSS_SELECTOR, "div > div.css-ydcgk2").text
            now = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
            
            print(btc_price)
            print(eth_price)
            print(usdt_price)
            print("="*100)

            f_btc.write(f"{btc_price.replace(',','')},{now}\n")
            f_eth.write(f"{eth_price.replace(',','')},{now}\n")
            f_usdt.write(f"{usdt_price.replace(',','')},{now}\n")

            time.sleep(2)
    
    finally:
        driver.quit()

    df = pd.DataFrame(results, index=False)
    df.to_csv("tmp.csv")