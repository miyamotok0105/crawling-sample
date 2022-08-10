import pandas as pd
import requests
import json 

def get_events_df(keyword, ym, output):
    # クエリの作成
    base_url = "https://connpass.com/api/v1/event/?"
    keyword_query = f"keyword={keyword}"
    ym_query = f"ym={ym}"
    query =  base_url + "&".join([keyword_query, ym_query])

    # APIからデータの取得
    event_json = json.loads(requests.get(query).text)["events"]
    df = pd.DataFrame(event_json)
    
    # ここから前処理
    df = df.loc[:, ['title', 'catch', 'started_at', 'event_url']]
    return df.to_csv(output)

if __name__=="__main__":
    KEYWORD = "Python"
    YM = 202207
    OUTPUT = "test.csv"

    print(get_events_df(KEYWORD, YM, OUTPUT))