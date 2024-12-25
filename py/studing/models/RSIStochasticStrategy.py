import pandas as pd
import numpy as np

class RSIStochasticStrategy:
    def __init__(self, data):
        self.data = data

    def calculate_rsi(self, rsi_min_period=14, rsi_max_period=14):
        delta = self.data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=rsi_min_period).mean()
        avg_loss = loss.rolling(window=rsi_max_period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.data['RSI'] = rsi


    def calculate_rsi_sma(self, period=14):
        self.data['RSI_SMA'] = self.data['RSI'].rolling(window=period).mean()

    def calculate_stochastic(self, stochastic_min_period=14, stochastic_max_period=14):
        # %K = (C - L14) / (H14 - L14) * 100
        # %D = SMA(%K, 3)
        c = self.data['close']
        l14 = self.data['low'].rolling(window=stochastic_min_period).min()
        h14 = self.data['high'].rolling(window=stochastic_max_period).max()
        k = (c - l14) / (h14 - l14) * 100
        d = k.rolling(window=3).mean()
        self.data['K'] = k
        self.data['D'] = d

    def calculate_macd(self, fastperiod=12, slowperiod=26, signalperiod=9):
        ema_fast = self.data['close'].ewm(span=fastperiod, adjust=False).mean()
        ema_slow = self.data['close'].ewm(span=slowperiod, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=signalperiod, adjust=False).mean()
        self.data['MACD'] = macd
        self.data['MACDsignal'] = signal

    def generate_signals(self, overbought=80, oversold=20):
        # Condições de compra
        buy_condition = (
            (self.data['MACD'] > 0) &  # Histograma MACD acima de zero
            (self.data['K'] < oversold) &  # Stochastic em sobrevenda
            (self.data['RSI'] > self.data['RSI_SMA'])  # RSI cruza acima da média móvel
        )

        # Condições de venda
        sell_condition = (
            (self.data['MACD'] < 0) &  # Histograma MACD abaixo de zero
            (self.data['K'] > overbought) &  # Stochastic em sobrecompra
            (self.data['RSI'] < self.data['RSI_SMA'])  # RSI cruza abaixo da média móvel
        )

        self.data['signal'] = 0
        self.data.loc[buy_condition, 'signal'] = 1
        self.data.loc[sell_condition, 'signal'] = -1


    def backtest(self):
        """
        Executa o backtest da estratégia.
        """
        # Aqui você implementaria a lógica de backtest, considerando as posições, cálculos de lucro/prejuízo, etc.
        # Você pode utilizar a classe backtester.py existente para essa parte.

        # Exemplo simplificado:
        self.calculate_indicators()
        self.generate_signals()
        # ... (restante do backtest)