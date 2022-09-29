import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
# from PyPDF2 import PdfFileMerger
from selenium.webdriver.common.action_chains import ActionChains

SLEEP_TIME = 5
CSV_NAME = "insta_ranking.csv"
SEARCH_WORD = "栽培　トマト"
DATA_DIR = ""

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

def binnd_pdf(dir, name):
    file_names = os.listdir(dir)
    file_paths = [os.path.join(dir,i) for i in file_names]

    pdf_file_merger = PdfFileMerger()
    for i_path in file_paths:
        pdf_file_merger.append(i_path)
    
    pdf_file_merger.write(name)
    pdf_file_merger.close()
    
if __name__ == "__main__":
    try:
        CHROMEDRIVER = "/usr/lib/chromium-browser/chromedriver"
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        driver = webdriver.Chrome(service=chrome_service)

        driver.get("https://www.j-platpat.inpit.go.jp/s0100")

        time.sleep(SLEEP_TIME)
        driver.save_screenshot("tmp_ss.png")

        driver.find_element(By.ID, "s01_srchCondtn_txtSimpleSearch").send_keys(SEARCH_WORD)
        driver.find_element(By.ID, "s01_srchBtn_btnSearch").click()
        time.sleep(SLEEP_TIME*3)


        scroll_all(driver)

        a_elements = get_link_element(driver)
        input(f"stop {len(a_elements)}")
        

        for i_element in a_elements: # 特許ごと
            i_element.click()
            time.sleep(SLEEP_TIME)
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            time.sleep(SLEEP_TIME)

            # get id
            patent_id = driver.find_element(By.TAG_NAME, "h2").text
            # click pdf radio button
            driver.find_element(By.ID, "rdoTxtPdfView_1-input")

            # 

            # get pdf page num
            # generate pdf url 
            pdf_url = [i for i in range(1, pdf_page_num)]

            patent_dir = os.path.join(DATA_DIR, patent_id)
            if not os.path.exists(patent_dir):
                os.makedirs(patent_dir)
            
            for i_url in pdf_url:
                download_pdf(patent_dir, i_url)
            
            # bind pdf
            pdf_name = f"{patent_id}.pdf"
            binnd_pdf(patent_dir, pdf_name)
            result.append(get_user_info(driver))

        pd.DataFrame.to_csv(CSV_NAME)

    finally:
        driver.quit()
