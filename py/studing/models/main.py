from binanceAPI import BinanceAPI
#from mm_strategy import MMStrategy
# from RSIStochasticStrategy import RSIStochasticStrategy
from BollingerStochasticStrategy import BollingerStochasticStrategy
from backtester import Backtester
from visualizer import Visualizer

# Informações de autenticação da Binance (substitua pelas suas)
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Inicializa o cliente da Binance
binaceApi = BinanceAPI(api_key, api_secret)

# Exemplo de uso
symbol = 'SOLBRL'
interval = '5m'
start_str = '10 day ago UTC'

# Obtém os dados históricos
data = binaceApi.get_historical_data(symbol, interval, start_str)


###########################################################################################################################


# ma_short_window = 20
# ma_long_window = 500
# bb_window = 20
 
#  # Cria uma instância da classe TechnicalIndicators
# indicators = MMStrategy(data)

# # Calcula os indicadores
# indicators.calc_moving_averages(ma_short_window, ma_long_window)

# # Calcular as Bandas de Bollinger
# indicators.calc_bollinger_bands(bb_window)

# # Gera os sinais
# indicators.generate_signals(ma_short_window, ma_long_window)


###########################################################################################################################


# # RSI
# rsi_min_period = 8
# rsi_max_period = 8

# # SMA
# sma_period = 14

# # Stochastic Oscillator
# stochastic_min_period=14
# stochastic_max_period=14

# # MACD
# fastperiod=12
# slowperiod=26 
# signalperiod=9

# # Buy and Sell Signals
# overbought=80
# oversold=20

# # Cria uma instância da classe RSIStochasticStrategy
# indicators = RSIStochasticStrategy(data)

# # Calcula o RSI
# indicators.calculate_rsi(rsi_min_period, rsi_max_period)

# # Calcular a Média Móvel Simples (SMA)
# indicators.calculate_rsi_sma(sma_period)

# # Calcular o Stochastic Oscillator
# indicators.calculate_stochastic(stochastic_min_period, stochastic_max_period)

# # Calcular a Média Móvel Simples (SMA)
# indicators.calculate_macd(fastperiod, slowperiod, signalperiod)

# # Gera os sinais
# indicators.generate_signals(overbought, oversold)


###########################################################################################################################


# Exemplo de uso:
strategy = BollingerStochasticStrategy(data)
strategy.calculate_bollinger_bands()
strategy.calculate_stochastic()
strategy.generate_signals()





###########################################################################################################################


initial_value = 500
quantity = 0.15
fee = 0.001 

backtester = Backtester(data, initial_value, quantity, fee)
print(backtester.initial_value)

backtester.run()


###########################################################################################################################


# # # Visualizar os sinais
visualizer = Visualizer()
visualizer.plot_results(data, backtester)
# print(type(backtester.transaction_history))