import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 4
CSV_NAME = "yahoo_auction.csv"

def update_page_num(driver, page_num, show_num=50):
    b_num = page_num*show_num + 1
    page_option = f"&b={b_num}"
    url = "https://auctions.yahoo.co.jp/search/search?p=novation&va=novation&exflg=1&n=50&s1=popular" + page_option
    driver.get(url)

def get_item_urls(driver):
    a_elements = driver.find_elements(By.CSS_SELECTOR, ".Product__titleLink.js-rapid-override.js-browseHistory-add")
    return [i.get_attribute('href') for i in a_elements]

def get_item_info(driver):
    result = dict()

    result["title"] = driver.find_element(By.CLASS_NAME, "ProductTitle__text").text
    result["price"] = driver.find_elements(By.CLASS_NAME, "Price__value")[0].text

    # # prompt_decision_price
    # if len(driver.find_elements(By.CLASS_NAME, "Price__value")) == 2:
    #     element = driver.find_elements(By.CLASS_NAME, "Price__value")[1]
    #     result.prompt_decision_price = element.text
    
    result["postage"] = driver.find_element(By.CLASS_NAME, "Price__postageValue").text
    result["bid_number"] = driver.find_elements(By.CLASS_NAME, "Count__number")[0].text.rsplit('\n', 1)[0].replace('\n', ' ')
    result["time_left"] = driver.find_elements(By.CLASS_NAME, "Count__number")[1].text.rsplit('\n', 1)[0].replace('\n', ' ')
    productdetail_elements = driver.find_element(By.CLASS_NAME, "ProductDetail")
    dt_elements = productdetail_elements.find_elements(By.TAG_NAME, "dt")
    dd_elements = productdetail_elements.find_elements(By.TAG_NAME, "dd")
    for i_dt, i_dd in zip(dt_elements, dd_elements):
        result[i_dt.text] = i_dd.text

    # l_element = element.find_element(By.CLASS_NAME, "l-left")
    # elements = l_element.find_elements(By.CLASS_NAME, "ProductDetail__description")
    # details = [i.text.replace('：', '') for i in elements]
    # result.start_time = details[0]
    # result.end_time = details[1]
    # result.automatic_extension = details[2]
    # result.early_termination = details[3]

    # r_element = element.find_element(By.CLASS_NAME, "l-right")
    # elements = r_element.find_elements(By.CLASS_NAME, "ProductDetail__description")
    # details = [i.text.replace('：', '') for i in elements]
    # result.returns = details[0]
    # result.bidder_appraisal_restriction = details[1]
    # result.bidder_verification_limit = details[2]
    # result.highest_bidder = details[3]
    # result.starting_price = details[4]
    # result.id = details[5]

    # # seller 
    # element = driver.find_element(By.CLASS_NAME, "Seller__name").find_element(By.TAG_NAME, "a")
    # result.seller = element.get_attribute("href")

    # # comprehensive_evaluation
    # element = driver.find_element(By.CLASS_NAME, "Seller__ratingSum").find_element(By.TAG_NAME, "a")
    # result.comprehensive_evaluation = element.text

    # # percentage_of_good_reviews
    # element = driver.find_element(By.CLASS_NAME, "Seller__ratingGood").find_element(By.TAG_NAME, "a")
    # result.percentage_of_good_reviews = element.text

    # # seller_region
    # element = driver.find_element(By.CLASS_NAME, "Seller__areaName")
    # result.percentage_of_good_reviews = element.text

    return result

if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)
        target_url = "https://auctions.yahoo.co.jp/search/search?va=novation&s1=popular"

        page_num = 0
        item_urls = list()
        while True:
            update_page_num(driver, page_num)
            time.sleep(SLEEP_TIME)
            urls = get_item_urls(driver)
            item_urls.extend(urls)
            page_num += 1
            if len(urls) == 0:
                break

        results = list()
        for i_url in item_urls:
            driver.get(i_url)   
            time.sleep(SLEEP_TIME)
            results.append(get_item_info(driver))

        pd.DataFrame(results).to_csv(CSV_NAME)

    finally:
        driver.quit()