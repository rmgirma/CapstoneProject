import os
import pandas as pd

# constant declarations:
nav = "\nPress any key to continue..."  # used to pause the flow
padding = 115  # length of character for padding

def exit_program():
    print("Good Bye...")
    exit()

def clear_screen():  # function to clear the screen between menu changes
    _ = os.system('cls')  

def main_menu():  # Main Menu function
    menu_option = {
        '1': margin_trade_long_menu,
        '2': margin_trade_short_menu,
        '3': exit_program
    }

    while True:
        clear_screen()
        print("\n" + "=" * padding)
        print("Leverage Trade Order Generator".center(padding))
        print("=" * padding)
        print("\nDeveloped by Abay GERD Token")
        print("Claim your free tokens at www.abaygerdtoken.com")
       # print("Uber Trading")
       # print("\n" + "=" * padding)
       # print("\nThis code helps generate up to 10 trade levels, allowing you to open both long and short trades simultaneously")
       # print("preventing liquidation up to your desired level, normally 3rd or 4th level in my case but feel free to experiment.")
       # print("\nAs soon as your trade gains exceed $20, you can take profits and open a new order at the current market price.") 
       # print("You continue trading this way, consistently collecting profits at your chosen threshold.") 
       # print("This strategy, called 'Uber Trading,' is designed to continuously generate profits throughout the days ahead.")
        print("\nHappy Uber Trading !")
        print("\nPlease select your trade direction and press ENTER:")
        print(" ")
        print("     1. Long Trade- with Margin")
        print("     2. Short Trade - with Margin")
        print("     3. Exit")
        print("=" * padding)
        selected = input("Enter your choice (1-3): ")

        if selected in menu_option:
            menu_option[selected]()  # calls the selected function
        else:
            print("\nInvalid choice. Please enter a number between 1 and 3.")
            input(nav)


# Function to safely get a float input
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


class MarginTradeLong:
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
        return self.liquidation_price * 1.005

    def record_trade(self, trade_number, trade_qty, trade_price, liquidation_price, trade_amount):
        self.trades.append({
            "Order #": trade_number,
            "Trade Price": round(trade_price, 2),
            "Trade Amount": round(trade_amount, 2),
            "Cumulative Cash Used": round(self.cumulative_cash_used, 2),
            "Next Liquidation": round(liquidation_price, 2),
            "Quantity": round(trade_qty, 4),
            "Cumulative QTY": round(self.asset_quantity, 4),
            "AVG Price": round(self.unit_price, 2)            
        })

    def get_trades_dataframe(self):
        return pd.DataFrame(self.trades)


class MarginTradeShort:
    def __init__(self, margin, initial_trade_amount, initial_unit_price):
        self.margin = margin
        self.trade_amount = initial_trade_amount
        self.unit_price = initial_unit_price
        self.asset_quantity = initial_trade_amount / initial_unit_price
        self.actual_cash_used = initial_trade_amount / margin
        self.cumulative_cash_used = self.actual_cash_used
        self.liquidation_price = self.unit_price * (1 + (1 / (margin + 0.2)))
        self.trades = []
        self.record_trade(1, self.asset_quantity, self.unit_price, self.liquidation_price, initial_trade_amount)

    def place_trade(self, new_unit_price, new_trade_amount, trade_number):
        new_asset_quantity = new_trade_amount / new_unit_price
        self.asset_quantity += new_asset_quantity
        self.trade_amount += new_trade_amount
        self.unit_price = self.trade_amount / self.asset_quantity
        self.actual_cash_used = new_trade_amount / self.margin
        self.cumulative_cash_used += self.actual_cash_used
        self.liquidation_price = self.unit_price * (1 + (1 / (self.margin + 0.2)))
        self.record_trade(trade_number, new_asset_quantity, new_unit_price, self.liquidation_price, new_trade_amount)

    def next_liquidation_price(self):
        return self.liquidation_price * 0.995

    def record_trade(self, trade_number, trade_qty, trade_price, liquidation_price, trade_amount):
        self.trades.append({
            "Order #": trade_number,
            "Trade Price": round(trade_price, 3),
            "Trade Amount": round(trade_amount, 0),
            "Cumulative Cash Used": round(self.cumulative_cash_used, 0),
            "Next Liquidation": round(liquidation_price, 3),
            "Quantity": round(trade_qty, 3),
            "Cumulative QTY": round(self.asset_quantity, 3),
            "AVG Price": round(self.unit_price, 2)            
        })

    def get_trades_dataframe(self):
        return pd.DataFrame(self.trades)


def margin_trade_long_menu():
    # Prompt the user for inputs with validation
    margin = get_float_input("Enter the leverage (e.g., 7 for 7x): ")
    initial_trade_amount = get_float_input("Enter the total amount to Buy/Long in USD (e.g., 2500): ")
    initial_unit_price = get_float_input("Enter Token's purchase unit price (e.g., 247.61): ")

    # Initialize the first trade
    trade = MarginTradeLong(margin, initial_trade_amount, initial_unit_price)

    # Place subsequent trades
    for i in range(2, 11):  # Continue until the 10th trade
        new_unit_price = trade.next_liquidation_price()
        new_trade_amount = trade.trade_amount  # New trade amount equals the previous cumulative trade amount
        trade.place_trade(new_unit_price, new_trade_amount, i)

    # Retrieve and display the trades in a DataFrame
    df = trade.get_trades_dataframe()
    print("\n" + "=" * padding)
    print(df)
    print("\n" + "=" * padding)
    input(nav)  # Pause before returning to the menu


def margin_trade_short_menu():
    # Prompt the user for inputs with validation
    margin = get_float_input("Enter the leverage (e.g., 7 for 7x): ")
    initial_trade_amount = get_float_input("Enter the total amount to Sell/Short in $ (e.g., 2500): ")
    initial_unit_price = get_float_input("Enter Token's purchase unit price (e.g., 247.61): ")

    # Initialize the first trade
    trade = MarginTradeShort(margin, initial_trade_amount, initial_unit_price)

    # Place subsequent trades
    for i in range(2, 11):  # Continue until the 10th trade
        new_unit_price = trade.next_liquidation_price()
        new_trade_amount = trade.trade_amount  # New trade amount equals the previous cumulative trade amount
        trade.place_trade(new_unit_price, new_trade_amount, i)

    # Retrieve and display the trades in a DataFrame
    df = trade.get_trades_dataframe()
    print("\n" + "=" * padding)
    print(df)
    print("\n" + "=" * padding)
    input(nav)  # Pause before returning to the menu


# program starts here . Run the Main Menu
main_menu()
