import requests
import time
import hashlib
import hmac
import json
import os
from dotenv import load_dotenv

# Load your API credentials from environment variables
load_dotenv()

API_KEY = 'mx0vglk6hwL0j8EEa7'
API_SECRET = 'e956137e68294e8c81411fcb784a39f6'

BASE_URL = "https://api.mexc.com"

def create_signature(params, secret_key):
    # Sort parameters and create query string without URL encoding
    sorted_params = sorted(params.items())
    query_string = '&'.join([f"{key}={value}" for key, value in sorted_params])
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
        "quantity": str(quantity),  # Convert to string
        "timestamp": str(int(time.time() * 1000))  # Convert timestamp to string
    }
    
    if order_type == 'LIMIT':
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        params['price'] = str(price)  # Convert price to string
        params['timeInForce'] = 'GTC'  # Good till canceled
    
    # Generate signature
    signature = create_signature(params, API_SECRET)
    
    # Important: Don't include signature in params used for signature generation
    params['signature'] = signature
    
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
    symbol = 'WBTCUSDT'  # Pair to trade
    side = 'BUY'  # BUY or SELL
    order_type = 'MARKET'  # Order type
    quantity = 0.0005  # Amount of BTC to buy
    
    try:
        order_response = place_order(symbol, side, order_type, quantity)
        print(f"Order placed successfully: {order_response}")
    except Exception as e:
        print(f"Error placing order: {str(e)}")