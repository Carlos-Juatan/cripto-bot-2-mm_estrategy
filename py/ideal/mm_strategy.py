import pandas as pd
import numpy as np
from ta.volatility import BollingerBands
from ta.trend import SMAIndicator

class MMStrategy:
    def __init__(self, data, close_column='close'):
        self.data = data.copy()
        self.close_column = close_column