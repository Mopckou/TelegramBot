import requests
import json, time

def get_inquiry():
    try:
        req = requests.get(url='https://api.exmo.com/v1/ticker/')
    except requests.ConnectionError:
        print('Ошибка соединения')
    else:
        return req.content

def btc_in_usd(req):
    answer = json.loads(req)
    return [answer['BTC_USD']['buy_price'], answer['BTC_USD']['sell_price'], answer['BTC_USD']['last_trade']]