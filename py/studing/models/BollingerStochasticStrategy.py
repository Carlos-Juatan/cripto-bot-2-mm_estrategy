import pandas as pd
import numpy as np

class BollingerStochasticStrategy:
    def __init__(self, data):
        self.data = data

    def calculate_bollinger_bands(self, period=20):
        # Média móvel simples
        self.data['SMA'] = self.data['close'].rolling(window=period).mean()
        # Desvio padrão
        std = self.data['close'].rolling(window=period).std()
        # Bandas de Bollinger
        self.data['BB_upper'] = self.data['SMA'] + 2 * std
        self.data['BB_middle'] = self.data['SMA']
        self.data['BB_lower'] = self.data['SMA'] - 2 * std

    def calculate_stochastic(self, fastk_period=14, slowk_period=3):
        # %K = (C - L14) / (H14 - L14) * 100
        # %D = SMA(%K, 3)
        c = self.data['close']
        l = self.data['low'].rolling(window=fastk_period).min()
        h = self.data['high'].rolling(window=fastk_period).max()
        k = (c - l) / (h - l) * 100
        d = k.rolling(window=slowk_period).mean()
        self.data['K'] = k
        self.data['D'] = d

    def generate_signals(self, overbought=80, oversold=20):
        buy_condition = (self.data['close'] < self.data['BB_lower']) & (self.data['K'] < oversold)
        sell_condition = (self.data['close'] > self.data['BB_upper']) & (self.data['K'] > overbought)

        self.data['signal'] = 0
        self.data.loc[buy_condition, 'signal'] = 1
        self.data.loc[sell_condition, 'signal'] = -1
