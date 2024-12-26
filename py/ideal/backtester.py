class Backtester:
    def __init__(self, data, indicators, initial_value, quantity, fee):
        self.data = data.copy()  # Avoid modifying original self.data
        self.indicators = indicators.copy()
        self.initial_value = initial_value
        self.quantity = quantity
        self.fee = fee