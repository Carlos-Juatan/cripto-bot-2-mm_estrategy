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
    # Calcular a média móvel de 20 períodos
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Gerar sinal de compra
    signal_buy = df['Close'].iloc[-1] > df['MA20'].iloc[-1]

    # Verificar se há um sinal de compra
    if signal_buy and not position_active:
        # Enviar uma ordem de compra
        # order = client_binance.create_order(symbol='BTCUSDT', side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=1)
        # print("Ordem de compra enviada:", order)
        position_active = True

        # testando apenas, sem arriscar comprar nada
        price = 0
        print(f'Pedido de compra envidado: ${price}')

# Loop principal
while True:
    update_data()
    generate_signal()
    time.sleep(60)  # Atualizar a cada minuto