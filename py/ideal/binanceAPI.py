import pandas as pd
from binance.client import Client

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_historical_data(self, symbol, interval, start_str):
        klines = self.client.get_historical_klines(symbol, interval, start_str)
        df = pd.DataFrame(klines, columns=['open time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'quote asset volume', 'number of trades', 'taker buy base asset volume', 'taker buy quote asset volume', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        return df