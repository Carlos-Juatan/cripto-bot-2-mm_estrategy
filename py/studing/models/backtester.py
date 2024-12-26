class Backtester:
    def __init__(self, data, initial_value, quantity, fee):
        self.data = data.copy()  # Avoid modifying original data
        self.initial_value = initial_value
        self.quantity = quantity
        self.fee = fee
        self.transaction_history = []

    def run(self):
        cash = self.initial_value
        position = 0  # 0: no position, 1: long, -1: short

        for index, row in self.data.iterrows():
            signal = row['signal']

            if signal == 1 and cash > 0 and position != 1:  # Buy signal
                # Calculate transaction cost
                transaction_cost = self.quantity * row['close'] * self.fee
                # Buy quantity
                quantity_bought = (cash - transaction_cost) / row['close']
                # Update cash and position
                cash -= quantity_bought * row['close'] + transaction_cost
                position = 1
                # Record transaction
                self.transaction_history.append({
                    "type": "buy",
                    "price": row['close'],
                    "quantity": quantity_bought,
                    "cash": cash,
                    "position": position
                })

            elif signal == -1 and position == 1:  # Sell signal
                # Calculate transaction cost
                transaction_cost = self.quantity * row['close'] * self.fee
                # Sell quantity
                quantity_sold = self.quantity
                # Update cash and position
                cash += quantity_sold * row['close'] - transaction_cost
                position = 0
                # Record transaction
                self.transaction_history.append({
                    "type": "sell",
                    "price": row['close'],
                    "quantity": quantity_sold,
                    "cash": cash,
                    "position": position
                })

        # Handle remaining position at the end
        if position == 1:
            cash += self.quantity * self.data['close'].iloc[-1]  # Sell at last close price
            self.transaction_history.append({
                "type": "sell",
                "price": self.data['close'].iloc[-1],
                "quantity": self.quantity,
                "cash": cash,
                "position": position
            })

        self.data['cash'] = cash

    def get_performance(self):
        # Calculate final portfolio value
        final_value = self.data['cash'].iloc[-1]

        # Calculate return
        return_pct = (final_value - self.initial_value) / self.initial_value * 100

        return final_value, return_pct
