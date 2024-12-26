from binanceAPI import BinanceAPI
from mm_strategy import MMStrategy
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


ma_short_window = 20
ma_long_window = 500
bb_window = 20
 
 # Cria uma instância da classe TechnicalIndicators
indicators = MMStrategy(data)

# Calcula os indicadores
indicators.calc_moving_averages(ma_short_window, ma_long_window)

# Calcular as Bandas de Bollinger
indicators.calc_bollinger_bands(bb_window)

# Gera os sinais
indicators.generate_signals(ma_short_window, ma_long_window)


###########################################################################################################################


initial_value = 500
quantity = 0.15
fee = 0.001 

backtester = Backtester(data, indicators.data, initial_value, quantity, fee)
print(backtester.initial_value)

backtester.run()

###########################################################################################################################


# # # Visualizar os sinais
visualizer = Visualizer()
visualizer.show_graphics(backtester.df_retorno_acumulado, backtester.df_retorno_acumulado, symbol)
# visualizer.plot_results(data, backtester)
# print(type(backtester.transaction_history))