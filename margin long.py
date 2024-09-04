import pandas as pd

class MarginTrade:
    def __init__(self, margin, initial_trade_amount, initial_unit_price):
        self.margin = margin
        self.trade_amount = initial_trade_amount
        self.unit_price = initial_unit_price
        self.asset_quantity = initial_trade_amount / initial_unit_price
        self.actual_cash_used = initial_trade_amount / margin
        self.cumulative_cash_used = self.actual_cash_used
        self.liquidation_price = self.unit_price * (1 - (1 / (margin + 0.2)))
        self.trades = []

        self.record_trade(1, self.asset_quantity, self.unit_price, self.liquidation_price, initial_trade_amount)

    def place_trade(self, new_unit_price, new_trade_amount, trade_number):
        new_asset_quantity = new_trade_amount / new_unit_price
        self.asset_quantity += new_asset_quantity
        self.trade_amount += new_trade_amount
        self.unit_price = self.trade_amount / self.asset_quantity
        self.actual_cash_used = new_trade_amount / self.margin
        self.cumulative_cash_used += self.actual_cash_used
        self.liquidation_price = self.unit_price * (1 - (1 / (self.margin + 0.2)))

        self.record_trade(trade_number, new_asset_quantity, new_unit_price, self.liquidation_price, new_trade_amount)

    def next_liquidation_price(self):
        return self.liquidation_price * 1.01

    def record_trade(self, trade_number, trade_qty, trade_price, liquidation_price, trade_amount):
        self.trades.append({
            "T #": trade_number,
            "Trade QTY": round(trade_qty, 4),
         #   "Asset Quantity": round(self.asset_quantity, 4),
            "Trade Price": round(trade_price, 2),
         #   "Unit Price": round(self.unit_price, 2),
         #  "Total Margin": round(self.trade_amount, 2),
            "Trade Amount": round(trade_amount, 2),
            "Actual Cash": round(self.actual_cash_used, 2),
         #  "Cumulative Cash Used": round(self.cumulative_cash_used, 2),
            "Liquidation": round(liquidation_price, 2) #,
         #  "101 PCT": round(liquidation_price * 1.01, 2)
        })

    def get_trades_dataframe(self):
        return pd.DataFrame(self.trades)


# Function to safely get a float input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Prompt the user for inputs with validation
margin = get_float_input("Enter the margin (e.g., 7): ")
initial_trade_amount = get_float_input("Enter the initial trade amount (e.g., 2000): ")
initial_unit_price = get_float_input("Enter the initial unit price (e.g., 61005): ")

# Initialize the first trade
trade = MarginTrade(margin, initial_trade_amount, initial_unit_price)

# Place subsequent trades
for i in range(2, 11):  # Continue until the 10th trade
    new_unit_price = trade.next_liquidation_price()
    new_trade_amount = trade.trade_amount  # New trade amount equals the previous cumulative trade amount
    trade.place_trade(new_unit_price, new_trade_amount, i)

# Retrieve and display the trades in a DataFrame
df = trade.get_trades_dataframe()
print(df)
