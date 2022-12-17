# pd.read_htmlを使用するためにlxml, html5lib, bs4のインストール

# ライブラリのインポート
import pandas as pd

i = 0
for i in range(8):
    url = f'https://line-ranking.userlocal.jp/?page={i}'
    
    if i == 0:
        # 一度目は普通にDataframeを作成
        tmp = pd.read_html(url, encoding='UTF-8',index_col=0)
        data= tmp[0].drop('Unnamed: 1', axis=1)
        
    else:
        tmp = pd.read_html(url, encoding='UTF-8',index_col=0)
        tmp = tmp[0].drop('Unnamed: 1', axis=1)
        # 縦方向にDataframeを結合
        data = pd.concat([data,tmp])

data.to_csv('line_official_ranking.csv', encoding='utf_8_sig')
