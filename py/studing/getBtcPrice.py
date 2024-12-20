import requests

coin = 'SOL'

brlsymbol = 'BRL'
usdtsymbol = 'USDT'

symbol = coin + usdtsymbol

url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'

request = requests.get(url)

content = request.json()

price = content['price']

print(f'O valor do símbolo {symbol} é {price}')