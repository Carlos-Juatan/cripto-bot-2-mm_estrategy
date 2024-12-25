import pandas as pd
import numpy as np

class Backtester:
  def __init__(self, data, initial_value, quantity, fee):
    self.data = data
    # self.data = data.copy()  # Avoid modifying original data
    self.initial_value = initial_value
    self.quantity = quantity
    self.fee = fee
    self.cash = initial_value
    self.hasBuied = False
    self.data['event'] = 0

  def run(self):
    for row in range(len(self.data) - 1):
      if self.hasBuied == False and self.data.loc[row, 'signal'] == 1:
          self.buy(self.data.loc[row+1,'close'])
      elif self.hasBuied == True and self.data.loc[row, 'signal'] == -1:
          self.sell(self.data.loc[row+1,'close'])


  def buy(self, price, stop_loss=None, take_profit=None):
    self.hasBuied = True
    self.data['event'] = 1
    self.cash -= price * self.quantity
    
  def sell(self, price):
    self.hasBuied = False
    self.data['event'] = -1
    self.cash += price * self.quantity - self.fee
    