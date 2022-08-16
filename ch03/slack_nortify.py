import requests
import sys
def slack_post(url, title, detail):
    target_data = {"text": message, "attachmentts":[{"text":detail}]}
    response = requests.post(url, json=target_data)

if __name__=="__main__":
    target_url = ""
    message = sys.argv[1]
    slack_post(target_url, message)
