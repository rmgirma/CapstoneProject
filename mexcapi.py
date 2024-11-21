import requests
import time
import hashlib
import hmac
import json
import os
from dotenv import load_dotenv

# Load your API credentials from environment variables
load_dotenv()

API_KEY = os.getenv('mx0vglNKKDb7Vvecq8')
API_SECRET = os.getenv('3b487f2afa6a4b1c9f2e0945162d4936')

BASE_URL = "https://api.mexc.com"

def create_signature(params, secret_key):
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params)])
    return hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def place_order(symbol, side, order_type, quantity, price=None):
    """
    Place a trade order on MEXC
    
    :param symbol: e.g. 'BTCUSDT'
    :param side: 'BUY' or 'SELL'
    :param order_type: 'LIMIT' or 'MARKET'
    :param quantity: Amount to buy or sell
    :param price: Required for LIMIT orders
    """
    endpoint = '/api/v3/order'
    url = BASE_URL + endpoint
    
    # Create the parameters for the request
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "timestamp": int(time.time() * 1000)  # Unix timestamp in milliseconds
    }
    
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        params['price'] = price
        params['timeInForce'] = 'GTC'  # Good till canceled
    
    # Generate signature
    params['signature'] = create_signature(params, API_SECRET)
    
    # Create headers
    headers = {
        'X-MEXC-APIKEY': API_KEY
    }
    
    # Make the POST request to place the order
    response = requests.post(url, headers=headers, params=params)
    
    # Handle the response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to place order: {response.status_code}, {response.text}")

# Example usage:
if __name__ == "__main__":
    symbol = 'BTCUSDT'  # Pair to trade
    side = 'BUY'  # BUY or SELL
    order_type = 'MARKET'  # Order type
    quantity = 0.0001  # Amount of BTC to buy
    
    try:
        order_response = place_order(symbol, side, order_type, quantity)
        print(f"Order placed successfully: {order_response}")
    except Exception as e:
        print(f"Error placing order: {str(e)}")
