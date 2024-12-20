
##################### PRIMEIRA FORMA - LOGADO COM O CLIENTE DA BINANCE E PEGANDO A ULTIMA OPERAÇÃO DA MOEDA ###########################

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


symbol1 = "SOLUSDT"
# pegar o preço
transacao = cliente_binance.get_recent_trades(symbol=symbol1, limit=1)
#print(transacao) # dentro dessa transação tem o 'price' que é o ultimo preço negociado da moeda, ou seja o preço atual
price1 = transacao[0]['price'] # NOTA: a variável 'transacao' mesmo que só tenha 1 item, ainda é um 'list' e detro dela um 'dictionary'
# 'dictionary' ( dicionário ) é uma lista de coisas que podem possuir um chave relacionado a essa coisa para ficar fácil de pegar

##################### SEGUNDA FORMA - USANDO A API DE URL DA BINANCE E PEGANDO O VALOR DA MOEDA ###########################

import requests


symbol2 = 'SOLUSDT'

url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol2}'

# requisição online ( da até para acessar no navegador ou em html, js, etc...)
request = requests.get(url) 

# tranforma em um arquivo json
content = request.json()

# pega o valor de 'price' dentro desse json
price2 = content['price']


####################### COMPLUSÃO #######################################

print(f'O valor da primeira forma é {price1}, e o valor da segunda é {price2}')