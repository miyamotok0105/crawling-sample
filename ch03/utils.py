import requests
from logging import getLogger, basicConfig()

class item_info:
    self.id = None
    self.title = None
    self.price = None
    self.url = None
    self.get_date = None
    self.sale_date = None
    self.category = None
    self.description = None
    self.store = None
    self.is_sale = None

def slack_post(url, title, detail):
    target_data = {"text": message, "attachmentts":[{"text":detail}]}
    response = requests.post(url, json=target_data)