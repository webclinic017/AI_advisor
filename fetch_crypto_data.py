import json

import numpy as np
import pandas as pd

# External lib, works to get a fear and greed amount. However, we're reversing that. At > 60, sell. At < 40, buy.
import fear_and_greed

"""

Functions to add: MSE
target = 0

mse = np.square(prediction - target) //https://en.wikipedia.org/wiki/Mean_squared_error

FOR EACH COIN IN THE TOP 100:
    COMPARE STOCH RSI
    
    COMPARE MACD
        
    BINARY GATES
        IF MACD IS DECREASING AND STOCH RSI > 80: 
            SELL
        IF MACD IS INCREASING AND RSI < 80:
            BUY
        IF MACD IS INCREASING AND RSI > 80:
                
    Quantitative value investing… Predict 6-month price movements based fundamental indicators from companies’ quarterly reports.
    
    Forecasting… Build time series models, or even recurrent neural networks, on the delta between implied and actual volatility.
    
    Statistical arbitrage… Find similar stocks based on their price movements and other factors and look for periods when their prices diverge.
    
"""


class CryptoData:
    def __init__(self):
        self.data = self.fetch_data()
        self.top_risers = self.get_weekly_risers()

        self.best_to_buy = []
        self.best_to_sell = []
        self.fear_and_greed = fear_and_greed.get().value
        self.buy_signal = False

    # FOR LIVE DATA USE THIS
    # def fetch_data(self):
    #     raw = requests.get(
    #         "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=true")
    #     data = np.array(raw.json())
    #     return data

    def fetch_data(self):
        # this is for not blowing up CoinGecko's API. Use for dev.
        with open('data/old.json') as old:
            data = json.load(old)
        return data

    def moving_average(self, a, n=7):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def get_weekly_risers(self):
        top_risers = []
        for coin in self.data[0:100]:
            id = coin["id"]
            sparkline = coin["sparkline_in_7d"]["price"]
            moving_avg = self.moving_average(sparkline)
            # moving_avg = (sum(sparkline) / len(sparkline)) / 7
            top_risers.append((id, moving_avg))
        # top_risers = sorted(top_risers, key = lambda t: t[1], reverse=True)
        print(top_risers)
        return top_risers


if __name__ == '__main__':
    data = CryptoData()
    print(data.top_risers)
    print(data.fear_and_greed)

    # Add data to a dictionary. If it's in the dict 3 times, then print a medium buy signal.
