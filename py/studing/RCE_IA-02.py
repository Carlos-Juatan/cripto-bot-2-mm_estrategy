import pandas as pd
import os 
import pymongo
from binance.client import Client
import time

# Conectar ao MongoDB
client = pymongo.MongoClient(os.getenv('URI'))
db = client[os.getenv('DB')]
collection = db[os.getenv('COLLECTION_BTC')]

# Criar um cliente Binance
client_binance = Client(os.getenv('API_Key'), os.getenv('SECRET_KEY'))

# Função para obter os dados mais recentes e atualizar o MongoDB
def update_data():
    # Obter os dados mais recentes da Binance
    klines = client_binance.get_historical_klines(symbol = "BTCUSDT", interval = Client.KLINE_INTERVAL_1MINUTE, limit = "1 day ago UTC")
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df.set_index('Open time', inplace=True)

    # Inserir os dados no MongoDB
    records = df.to_dict('records')
    collection.insert_many(records)

# Função para gerar sinais de compra
def generate_signal():
    # Carregar os dados do MongoDB
    pipeline = [
        {
            '$sort': { 'Open time': -1 }  # Ordenar por data em ordem decrescente
        },
        {
            '$limit': 1000  # Limitar o número de registros para otimizar a consulta
        }
    ]
    data = list(collection.aggregate(pipeline))
    df = pd.DataFrame(data)

    # Calcular as médias móveis e gerar sinais
    # ... (código similar ao seu código original)

    # Verificar se há um sinal de compra
    if signal_buy:
        # Enviar uma ordem de compra
        order = client_binance.create_order(symbol='BTCUSDT', side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=1)
        print("Ordem de compra enviada:", order)

# Loop principal
while True:
    update_data()
    generate_signal()
    time.sleep(60)  # Atualizar a cada minuto