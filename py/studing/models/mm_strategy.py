import pandas as pd
import numpy as np
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator

class MMStrategy:
    def __init__(self, df, close_column='Close'):
        self.df = df
        self.close_column = close_column

    def calc_moving_averages(self, short_window, long_window):
        # self.df['MA_' + str(short_window)] = self.df[self.close_column].rolling(window=short_window).mean()
        # self.df['MA_' + str(long_window)] = self.df[self.close_column].rolling(window=long_window).mean()
        self.df['MA_short'] = self.df[self.close_column].rolling(window=short_window).mean()
        self.df['MA_long'] = self.df[self.close_column].rolling(window=long_window).mean()

    def calc_bollinger_bands(self, window, num_std=2):
        # Initialize Bollinger Bands Indicator
        indicator_bb = BollingerBands(close=self.df[self.close_column], window=window, window_dev=num_std)

        # Add Bollinger Bands features
        self.df['bb_bbm'] = indicator_bb.bollinger_mavg()
        self.df['bb_bbh'] = indicator_bb.bollinger_hband()
        self.df['bb_bbl'] = indicator_bb.bollinger_lband()

        # Add Bollinger Band high indicator
        self.df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

        # Add Bollinger Band low indicator
        self.df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

    def generate_signals(self, short_window, long_window):
        # Sinal de compra: 
        # 1. Média móvel curta acima da média móvel longa
        # 2. Preço de fechamento acima da banda superior de Bollinger
        # buy_condition1 = self.df['MA_' + str(short_window)] > self.df['MA_' + str(long_window)] 
        buy_condition1 = self.df['MA_short'] > self.df['MA_long'] 
        buy_condition2 = self.df['Close'] > self.df['bb_bbh']
        buy_signal = np.where((buy_condition1) & (buy_condition2), 1, 0)

        # Sinal de venda:
        # 1. Média móvel curta abaixo da média móvel longa
        # 2. Preço de fechamento abaixo da banda inferior de Bollinger
        # sell_condition1 = self.df['MA_' + str(short_window)] < self.df['MA_' + str(long_window)]
        sell_condition1 = self.df['MA_short'] < self.df['MA_long']
        sell_condition2 = self.df['Close'] < self.df['bb_bbl']
        sell_signal = np.where((sell_condition1) & (sell_condition2), -1, 0)

        # Combinação dos sinais
        self.df['signal'] = buy_signal + sell_signal 