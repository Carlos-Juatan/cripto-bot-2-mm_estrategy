import pandas as pd
import numpy as np
from binance.client import Client
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator

# Nescessário para mostrar os graficos na tela
import matplotlib.pyplot as plt

# Nescessário para mudar o tema dos gráficos
import mplcyberpunk 
plt.style.use("cyberpunk")



# Informações de autenticação da Binance (substitua pelas suas)
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Inicializa o cliente da Binance
client = Client(api_key, api_secret)

# Função para obter os dados históricos de preços
def get_historical_data(symbol, interval, start_str):
    klines = client.get_historical_klines(symbol, interval, start_str)
    df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df['Close'] = pd.to_numeric(df['Close'])
    return df

# Função para calcular a média móvel
def calculate_moving_average(df, column, window):
    df['MA_' + str(window)] = df[column].rolling(window=window).mean()
    return df

# Função para gerar sinais de compra e venda
def generate_signals(df, short_window, long_window):
    df['signal'] = np.where(df['MA_' + str(short_window)] > df['MA_' + str(long_window)], 1, 0)
    return df

# Exemplo de uso
symbol = 'SOLBRL'
interval = Client.KLINE_INTERVAL_1HOUR
start_str = '100 day ago UTC'

# Obtém os dados históricos
data = get_historical_data(symbol, interval, start_str)

# Calcula as médias móveis
data = calculate_moving_average(data, 'Close', 20)
data = calculate_moving_average(data, 'Close', 50)

# Gera os sinais de compra e venda
data = generate_signals(data, 20, 50)

###########################################################################################################################






valor_initial = 50
valor_atual = valor_initial
quantity = 0.015
taxa = 0.001 

data['lucro'] = 0
has_buy = False

print(data['Close'][1] * quantity)

for i in range(1, len(data)):
    data['lucro'][i] = valor_atual - valor_initial
    
    if(has_buy == False and data['signal'][i] == 1):
        has_buy = True
        valor_atual -= data['Close'][i] * quantity
        # print(f'foi comprado a {data['Close'][i] * quantity} e sobrou R${valor_atual} o lucro atua é de {data['lucro'][i]}')

    if(has_buy and data['signal'][i] == 0):
        has_buy = False
        valor_atual += data['Close'][i] * (quantity - taxa)
        # print(f'foi vendido a {data['Close'][i] * quantity} e sobrou R${valor_atual} o lucro atua é de {data['lucro'][i]}')


data['mostrar_lucro'] = data['Close'] + data['lucro']

print(f'O lucro final é de {valor_atual - valor_initial}')

# # Visualizar os sinais
plt.figure(figsize=(1080,720))
plt.plot(data['Close'], label='Preço de Fechamento')
plt.plot(data['mostrar_lucro'], label='lucro')
plt.scatter(data.index[data['signal'] == 1], data['Close'][data['signal'] == 1], marker='^', color='green', label='Sinal de Compra')
plt.scatter(data.index[data['signal'] == 0], data['Close'][data['signal'] == 0], marker='v', color='red', label='Sinal de Venda')
plt.legend()
plt.show()