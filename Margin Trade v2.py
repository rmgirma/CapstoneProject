import os
import pandas as pd

# Constants
NAV = "\nPress any key to continue..."
PADDING = 115

# Utility Functions
def exit_program():
    print("Good Bye...")
    exit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Base Class for Margin Trades
class MarginTrade:
    def __init__(self, margin, initial_trade_amount, initial_unit_price, is_long):
        self.margin = margin
        self.trade_amount = initial_trade_amount
        self.unit_price = initial_unit_price
        self.asset_quantity = initial_trade_amount / initial_unit_price
        self.actual_cash_used = initial_trade_amount / margin
        self.cumulative_cash_used = self.actual_cash_used
        self.is_long = is_long
        self.liquidation_price = self.calculate_liquidation_price()
        self.trades = []
        self.record_trade(1, self.asset_quantity, self.unit_price, self.liquidation_price, initial_trade_amount)

    def calculate_liquidation_price(self):
        direction_factor = -1 if self.is_long else 1
        return self.unit_price * (1 + direction_factor * (1 / (self.margin + 0.2)))

    def place_trade(self, new_unit_price, new_trade_amount, trade_number):
        new_asset_quantity = new_trade_amount / new_unit_price
        self.asset_quantity += new_asset_quantity
        self.trade_amount += new_trade_amount
        self.unit_price = self.trade_amount / self.asset_quantity
        self.actual_cash_used = new_trade_amount / self.margin
        self.cumulative_cash_used += self.actual_cash_used
        self.liquidation_price = self.calculate_liquidation_price()
        self.record_trade(trade_number, new_asset_quantity, new_unit_price, self.liquidation_price, new_trade_amount)

    def next_liquidation_price(self):
        adjustment_factor = 1.005 if self.is_long else 0.995
        return self.liquidation_price * adjustment_factor

    def record_trade(self, trade_number, trade_qty, trade_price, liquidation_price, trade_amount):
        self.trades.append({
            "Order #": trade_number,
            "Trade Price": round(trade_price, 2),
            "Trade Amount": round(trade_amount, 2),
            "Cumulative Cash Used": round(self.cumulative_cash_used, 2),
            "Next Liquidation": round(liquidation_price, 2),
            "Quantity": round(trade_qty, 2),
            "Cumulative QTY": round(self.asset_quantity, 2),
            "AVG Price": round(self.unit_price, 2)
        })

    def get_trades_dataframe(self):
        return pd.DataFrame(self.trades)

# Menu Functions
def trade_menu(is_long):
    direction = "Buy/Long" if is_long else "Sell/Short"
    margin = get_float_input(f"Enter the leverage (e.g., 7 for 7x): ")
    initial_trade_amount = get_float_input(f"Enter the total amount to {direction} in USD (e.g., 2500): ")
    initial_unit_price = get_float_input("Enter Token's purchase unit price (e.g., 247.61): ")

    trade = MarginTrade(margin, initial_trade_amount, initial_unit_price, is_long)

    for i in range(2, 11):
        new_unit_price = trade.next_liquidation_price()
        new_trade_amount = trade.trade_amount
        trade.place_trade(new_unit_price, new_trade_amount, i)

    df = trade.get_trades_dataframe()
    print("\n" + "=" * PADDING)
    print(df)
    print("\n" + "=" * PADDING)
    input(NAV)

def main_menu():
    menu_options = {
        '1': lambda: trade_menu(is_long=True),
        '2': lambda: trade_menu(is_long=False),
        '3': exit_program
    }

    while True:
        clear_screen()
        print("\n" + "=" * PADDING)
        print("Leverage Trade Order Generator".center(PADDING))
        print("=" * PADDING)
        print("\nDeveloped by Abay GERD Token")
        print("Claim your free tokens at www.abaygerdtoken.com")
        print("\nHappy Uber Trading!")
        print("\nPlease select your trade direction and press ENTER:")
        print("\n     1. Long Trade - with Margin")
        print("     2. Short Trade - with Margin")
        print("     3. Exit")
        print("=" * PADDING)

        selected = input("Enter your choice (1-3): ")
        if selected in menu_options:
            menu_options[selected]()
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")
            input(NAV)

# Program Entry Point
if __name__ == "__main__":
    main_menu()
    