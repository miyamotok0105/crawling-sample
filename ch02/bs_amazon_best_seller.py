# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re


url = "https://www.amazon.co.jp/gp/bestsellers/books/466298"


print(url)
# response = requests.get(url)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
response = requests.get(url, headers=headers)

print(response)

soup = BeautifulSoup(response.text, 'html.parser')
print(type(soup))

#p13n-asin-index-0 > div.zg-grid-general-faceout > div > a:nth-child(2) > span > div

#$$('css selector')
#$x('xpath')

#$$('.zg-grid-general-faceout')

#$$('.zg-grid-general-faceout')[0].textContent
#'統計学の基礎から学ぶExcelデータ分析の全知識（できるビジネス） できるビジネスシリーズ三好大悟5つ星のうち4.2 185Kindle版￥1,881900ポイント(48%)'


items = soup.select('.zg-grid-general-faceout')

for item in items:
    print(item.text)

