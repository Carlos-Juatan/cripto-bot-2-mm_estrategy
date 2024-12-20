import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import talib

plt.style.use("cyberpunk")

def fetch_and_preprocess_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data['SMA20'] = talib.SMA(data['Close'], 20)  # Média móvel simples de 20 períodos
    return data

def generate_signals(data, condition):
    data['signal'] = (data['Close'] > data['SMA20']).astype(int) if condition == 'buy' else (data['Close'] < data['SMA20']).astype(int)
    return data

def backtest(data):
    data['position'] = data['signal'].diff()
    data['returns'] = data['Close'].pct_change()
    data['strategy_returns'] = data['position'] * data['returns']
    return data

# ... restante do código

ticker = "BTC-USD"
data = fetch_and_preprocess_data(ticker, "2000-01-01", "2024-11-30")

# Gerar sinais de compra e venda
data = generate_signals(data, 'buy')
data = generate_signals(data, 'sell')

# Backtest
backtest_results = backtest(data)

# Plotar resultados
backtest_results['strategy_returns'].cumsum().plot()
plt.show()