# -*- coding: utf-8 -*-

"""
特許情報を取得する
"""
import os
import time
import requests
import pandas as pd
from PyPDF2 import PdfFileMerger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager

SLEEP_TIME = 6
CSV_NAME = "tokkyo.csv"
SEARCH_WORD = "栽培　トマト"
DATA_DIR = "output"

def scroll_all(driver):
    pre_html = None
    while not driver.page_source == pre_html:
        pre_html = driver.page_source
        driver.execute_script("window.scrollBy(0, 7000);")
        time.sleep(SLEEP_TIME)

def get_link_element(driver):
    result = list()
    tbody_element = driver.find_element(By.TAG_NAME, "tbody")
    tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")
    for i_tr in tr_elements:
        p_element = i_tr.find_element(By.ID, "patentUtltyIntnlSimpleBibLst_tableView_docNum")
        result.append(p_element.find_element(By.TAG_NAME, "a"))
    return result

def download_pdf(dir, url):
    file_name = url.split("/")[-1]
    file_path = os.path.join(dir, file_name)

    content_data = requests.get(url).content
    time.sleep(SLEEP_TIME)
    with open(file_path ,'wb') as f:
        f.write(content_data)

def sort_pdf(pdf_paths):
    file_name = [os.path.splitext(os.path.basename(i))[0] for i in pdf_paths]
    file_num = [int(i.split("-")[-1]) for i in file_name]
    path_dict = {i_num:i_path for i_num, i_path in zip(file_num, pdf_paths)}
    return [i[1] for i in sorted(path_dict.items(), key=lambda x:x[0])]

def binnd_pdf(dir, name):
    file_names = os.listdir(dir)
    file_paths = sort_pdf([os.path.join(dir,i) for i in file_names if ".pdf" in i])

    pdf_file_merger = PdfFileMerger()
    for i_path in file_paths:
        pdf_file_merger.append(i_path)
    
    pdf_file_merger.write(name)
    pdf_file_merger.close()
    
if __name__ == "__main__":
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.j-platpat.inpit.go.jp/s0100")
        time.sleep(SLEEP_TIME)
        driver.find_element(By.ID, "s01_srchCondtn_txtSimpleSearch").send_keys(SEARCH_WORD)
        driver.find_element(By.ID, "s01_srchBtn_btnSearch").click()
        time.sleep(SLEEP_TIME)

        scroll_all(driver)

        a_elements = get_link_element(driver)

        for i_element in a_elements:
            i_element.click()
            time.sleep(SLEEP_TIME)
            driver.switch_to.window(driver.window_handles[1])

            patent_id = driver.find_element(By.TAG_NAME, "h2").text
            pdf_label_element = driver.find_element(By.ID, "rdoTxtPdfView_1")
            pdf_label_element.click()
            time.sleep(SLEEP_TIME)

            pdf_page_num = int(driver.find_element(By.ID, 'p02_main_lblTotalPageCount').text)
            pdf_urls = list()
            for i_num in range(1, pdf_page_num+1):
                driver.find_element(By.ID, "p02_main_txtPage").clear()
                driver.find_element(By.ID, "p02_main_txtPage").send_keys(i_num)
                driver.find_element(By.ID, "p02_main_btnDisplay").click()
                time.sleep(SLEEP_TIME)
                pdf_urls.append(driver.find_element(By.ID, "p0201_pdfObj").get_attribute("src"))

            patent_dir = os.path.join(DATA_DIR, patent_id)
            if not os.path.exists(patent_dir):
                os.makedirs(patent_dir)
            
            for i_url in pdf_urls:
                print(i_url)
                download_pdf(patent_dir, i_url)
                time.sleep(SLEEP_TIME)
            
            pdf_name = f"{patent_id}.pdf"
            binnd_pdf(patent_dir, pdf_name)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        pd.DataFrame().to_csv(CSV_NAME)

    finally:
        driver.quit()


# "/html/body/div[1]/div[1]/div[5]/div[4]/div"
# [i.get_attribute("href") for i in xpath. "h2 > a")]
# /html/body/div[1]/div[1]/div[5]/div[4]/div[8]/div/div[2]/div/div/h2/a

