import pandas as pd
import numpy as np

class Backtester:
    def __init__(self, data, initial_value, quantity, fee):
        self.data = data
        self.initial_value = initial_value
        self.atual_value = initial_value
        self.quantity = quantity
        self.fee = fee
        self.data['lucro'] = 0
        self.has_buy = False

    def run(self):
        for i in range(1, len(self.data)):
            self.data['lucro'][i] = self.atual_value - self.initial_value
            
            if(self.has_buy == False and self.data['signal'][i] == 1):
                self.has_buy = True
                self.atual_value -= self.data['Close'][i] * self.quantity

            if(self.has_buy and self.data['signal'][i] == 0):
                self.has_buy = False
                self.atual_value += self.data['Close'][i] * (self.quantity - self.fee)


        self.data['mostrar_lucro'] = self.data['Close'] + self.data['lucro']
        return self.data