import pandas as pd
import numpy as np
from binance.client import Client
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator

# Necessary for showing plots
import matplotlib.pyplot as plt

# Necessary for changing the theme of the plots
import mplcyberpunk

plt.style.use("cyberpunk")


#######################################################################

def analyze_parameters(api_key, api_secret, symbol, interval, min_window, max_window, bb_window, bb_dev):
  """
  Analyzes various combinations of moving average and Bollinger Band parameters
  and returns the combination with the highest profit.

  Args:
      api_key (str): Your Binance API key.
      api_secret (str): Your Binance API secret.
      symbol (str): The cryptocurrency symbol (e.g., "SOLBRL").
      interval (str): The time interval for historical data (e.g., "15MINUTE").
      min_window (int): Minimum window size for the short moving average.
      max_window (int): Maximum window size for the long moving average.
      bb_window (int): Window size for the Bollinger Bands.
      bb_dev (int): Number of standard deviations for the Bollinger Bands.

  Returns:
      tuple: A tuple containing the best combination of parameters and the 
              corresponding maximum profit.
  """

  client = Client(api_key, api_secret)
  klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, "1000 day ago UTC")

  # Convert data to a pandas DataFrame
  df = pd.DataFrame(klines, columns=[
      'Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
      'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
      'Taker buy quote asset volume', 'Ignore'])
  df['Close'] = df['Close'].astype(float)

  best_profit = 0
  best_params = None

  for sma_short in range(min_window, max_window + 1):
    for sma_long in range(sma_short + 1, max_window + 1):
      for bb_dev in range(1, 5):

        # Calculate Bollinger Bands
        indicator_bb = BollingerBands(close=df['Close'], window=bb_window, window_dev=bb_dev)
        df['bb_high'] = indicator_bb.bollinger_hband()
        df['bb_low'] = indicator_bb.bollinger_lband()

        # Calculate moving averages
        sma_short_indicator = SMAIndicator(close=df['Close'], window=sma_short)
        sma_long_indicator = SMAIndicator(close=df['Close'], window=sma_long)
        df['sma_short'] = sma_short_indicator.sma_indicator()
        df['sma_long'] = sma_long_indicator.sma_indicator()

        # Generate buy/sell signals
        df['buy_signal'] = np.where((df['Close'] < df['bb_low']) & (df['sma_short'] > df['sma_long']), 1, 0)
        df['sell_signal'] = np.where((df['Close'] > df['bb_high']) & (df['sma_short'] < df['sma_long']), -1, 0)

        valor_initial = 50
        valor_atual = valor_initial
        quantity = 0.015
        taxa = 0.001

        df['lucro'] = 0
        has_buy = False

        for i in range(1, len(df)):
          df['lucro'][i] = valor_atual - valor_initial

          if (has_buy == False and df['buy_signal'][i] == 1):
            has_buy = True
            valor_atual -= df['Close'][i] * quantity

          if (has_buy and df['sell_signal'][i] == -1):
            has_buy = False
            valor_atual += df['Close'][i] * (quantity - taxa)

        current_profit = valor_atual - valor_initial

        # Update best parameters if current profit is higher
        if current_profit > best_profit:
          best_profit = current_profit
          best_params = {
            'sma_short': sma_short,
            'sma_long': sma_long,
            'bb_window': bb_window,
            'bb_dev': bb_dev
          }

        if current_profit == best_profit:
          # Plot the results for the best combination
          plt.figure(figsize=(1080, 720))
          # ... (your plotting code here)

        return {'best_params': best_params, 'max_profit': best_profit}

# Example usage:
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

result = analyze_parameters(api_key, api_secret, 'SOLBRL', '15m', 10, 30, 20, 2, plot=True)
print(result)