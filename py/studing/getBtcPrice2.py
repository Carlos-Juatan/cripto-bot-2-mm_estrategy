import pandas as pd
import os 
import time 
from binance.client import Client
from binance.enums import *

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("KEY_BINANCE")
secret_key = os.getenv("SECRET_BINANCE")

cliente_binance = Client(api_key, secret_key)


symbol = "SOLUSDT"
# pegar o preço
transacao = cliente_binance.get_recent_trades(symbol=symbol, limit=1)
print(transacao) # dentro dessa transação tem o 'price' que é o ultimo preço negociado da moeda, ou seja o preço atual