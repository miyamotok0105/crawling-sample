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

        base_url = "https://bitflyer.com/ja-jp/virtual-currency-chart"
        
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        driver.get(base_url)
        
        time.sleep(5)
        
        btc_file_name = "btc.csv"
        f_btc = open(btc_file_name, "a")

        eth_file_name = "eth.csv"
        f_eth = open(eth_file_name, "a")

        usdt_file_name = "xrp.csv"
        f_xrp = open(usdt_file_name, "a")

        table_elements = driver.find_element(By.CSS_SELECTOR, "#Chart > div > table")
            
        while True:
            df = pd.read_html(table_elements.get_attribute("outerHTML"))[0]
            btc_price = df.loc[0, "価格"]
            xrp_price = df.loc[1, "価格"]
            eth_price = df.loc[2, "価格"]

            now = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
            
            f_btc.write(f"{btc_price.replace(',','')},{now}\n")
            f_eth.write(f"{eth_price.replace(',','')},{now}\n")
            f_xrp.write(f"{xrp_price.replace(',','')},{now}\n")

            time.sleep(2)
    
    finally:
        driver.quit()
