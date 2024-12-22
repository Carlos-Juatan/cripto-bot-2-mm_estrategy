from mm_strategy import MMStrategy
from binanceAPI import BinanceAPI
from backtester import Backtester
from visualizer import Visualizer

# Informações de autenticação da Binance (substitua pelas suas)
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Inicializa o cliente da Binance
binaceApi = BinanceAPI(api_key, api_secret)

# Exemplo de uso
symbol = 'SOLBRL'
interval = '1h'
start_str = '100 day ago UTC'

# Obtém os dados históricos
data = binaceApi.get_historical_data(symbol, interval, start_str)


###########################################################################################################################


ma_short_window = 20
ma_long_window = 200
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


initial_value = 50
quantity = 0.015
fee = 0.001 

backtester = Backtester(indicators.df, initial_value, quantity, fee)

final_profit = backtester.run()


###########################################################################################################################


# # Visualizar os sinais
visualizer = Visualizer()
visualizer.plot_results(backtester.data)