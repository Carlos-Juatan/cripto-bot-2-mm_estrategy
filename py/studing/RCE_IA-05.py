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

# 2 Obter os Dados de Preços:

# Substitua por suas credenciais da Binance
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

client = Client(api_key, api_secret)
klines = client.get_historical_klines("SOLBRL", Client.KLINE_INTERVAL_15MINUTE, "10 day ago UTC")

# Converter os dados para um DataFrame do pandas
df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
df['Close'] = df['Close'].astype(float)



# 3 Calcular as Bandas de Bollinger:

indicator_bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
df['bb_high'] = indicator_bb.bollinger_hband()
df['bb_low'] = indicator_bb.bollinger_lband()

# 4 Visualizar os Dados:

# plt.legend()
# plt.show()


# 5 Gerar Sinais de Negociação (Opcional):-

# Exemplo de sinal de compra quando o preço cruza a banda inferior
#df['buy_signal'] = np.where(df['Close'] < df['bb_low'], 1, 0)







# Código Completo:

# ... (código anterior)

# Gerar sinais de compra (exemplo)


# Calcular médias móveis
sma_short = SMAIndicator(close=df['Close'], window=10)
sma_long = SMAIndicator(close=df['Close'], window=20)
df['sma_short'] = sma_short.sma_indicator()
df['sma_long'] = sma_long.sma_indicator()

# Gerar sinais de compra e venda
df['buy_signal'] = np.where((df['Close'] < df['bb_low']) & (df['sma_short'] > df['sma_long']), 1, 0)
df['sell_signal'] = np.where((df['Close'] > df['bb_high']) & (df['sma_short'] < df['sma_long']), -1, 0)

valor_initial = 50
valor_atual = valor_initial
quantity = 0.015
taxa = 0.001 

df['lucro'] = 0
has_buy = False

print(df['Close'][1] * quantity)

for i in range(1, len(df)):
    df['lucro'][i] = valor_atual - valor_initial
    
    if(has_buy == False and df['buy_signal'][i] == 1):
        has_buy = True
        valor_atual -= df['Close'][i] * quantity
        print(f'foi comprado a {df['Close'][i] * quantity} e sobrou R${valor_atual} o lucro atua é de {df['lucro'][i]}')

    if(has_buy and df['sell_signal'][i] == -1):
        has_buy = False
        valor_atual += df['Close'][i] * (quantity - taxa)
        print(f'foi vendido a {df['Close'][i] * quantity} e sobrou R${valor_atual} o lucro atua é de {df['lucro'][i]}')



# print(df['sell_signal'])
# with open('output.txt', 'w') as f:
#     print(df['sell_signal'], file=f)

# for signal in range(1, len(df)):

#     if (has_buy == False and )

# # Visualizar os sinais
# plt.figure(figsize=(1080,720))
# plt.plot(df['Close'], label='Preço de Fechamento')
# # plt.plot(df['bb_high'], label='Banda Superior')
# # plt.plot(df['bb_low'], label='Banda Inferior')
# # plt.plot(df['sma_short'], label='SMA Curta')
# # plt.plot(df['sma_long'], label='SMA Longa')
# plt.scatter(df.index[df['buy_signal'] == 1], df['Close'][df['buy_signal'] == 1], marker='^', color='green', label='Sinal de Compra')
# plt.scatter(df.index[df['sell_signal'] == -1], df['Close'][df['sell_signal'] == -1], marker='v', color='red', label='Sinal de Venda')
# plt.legend()
# plt.show()

