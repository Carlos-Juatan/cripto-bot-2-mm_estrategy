import requests

def get_price_binance(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    request = requests.get(url)
    content = request.json()
    return content['price']