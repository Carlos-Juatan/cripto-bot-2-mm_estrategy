import getPrice

coin = 'SOLUSDT'
price = getPrice.get_price_binance(coin)






import pandas as pd
import os 
import time 
from binance.client import Client
from binance.enums import *

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("KEY_BINANCE")
secret_key = os.getenv("SECRET_BINANCE")

client = Client(api_key, secret_key)


trades = client.get_my_trades(symbol='SOLBRL')

print(trades)