import pandas as pd
from binance.client import Client

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_historical_data(self, symbol, interval, start_str):
        klines = self.client.get_historical_klines(symbol, interval, start_str)
        df = pd.DataFrame(klines, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        df['Close'] = pd.to_numeric(df['Close'])
        return df