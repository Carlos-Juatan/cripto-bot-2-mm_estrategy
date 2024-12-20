import pandas as pd
import os 
from sqlalchemy import create_engine
from binance.client import Client
import time

# Conectar ao banco de dados
engine = create_engine('postgresql://user:password@host:port/database')

# Criar um cliente Binance
client = Client(os.getenv('API_Key'), os.getenv('SECRET_KEY'))

# Função para obter os dados mais recentes e atualizar o banco de dados
def update_data():
    # Obter os dados mais recentes da Binance
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE", "1 day ago UTC")
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df.set_index('Open time', inplace=True)

    # Salvar os dados no banco de dados
    df.to_sql('btc_data', engine, if_exists='append', index=True)

# Função para gerar sinais de compra
def generate_signal():
    # Carregar os dados do banco de dados
    df = pd.read_sql_query('SELECT * FROM btc_data', engine)

    # Calcular as médias móveis e gerar sinais
    # ... (código similar ao seu código original)

    # Verificar se há um sinal de compra
    if signal_buy:
        # Enviar uma ordem de compra
        order = client.create_order(symbol='BTCUSDT', side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=1)
        print("Ordem de compra enviada:", order)

# Loop principal
while True:
    update_data()
    generate_signal()
    time.sleep(60)  
    
# Atualizar a cada minuto