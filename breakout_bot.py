import MetaTrader5 as mt5
import time

# Constants
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M5  # 5-minute timeframe
LOT_SIZE = 0.1
STOP_LOSS = 20  # in pips
TAKE_PROFIT = 40  # in pips

# Define breakout levels (can be dynamically adjusted)
RESISTANCE_LEVEL = 1.1000  # Example resistance level
SUPPORT_LEVEL = 1.0950  # Example support level

# Initialize MT5 connection
def connect_mt5():
    if not mt5.initialize():
        print("MT5 Initialization failed")
        return False
    return True

# Function to get the latest price data
def get_price():
    tick = mt5.symbol_info_tick(SYMBOL)
    return tick.bid, tick.ask

# Function to place a buy order
def place_buy_order():
    price = mt5.symbol_info_tick(SYMBOL).ask
    sl = price - (STOP_LOSS * 0.0001)
    tp = price + (TAKE_PROFIT * 0.0001)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT_SIZE,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "Breakout Buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    print(f"Buy Order Sent: {result}")

# Function to place a sell order
def place_sell_order():
    price = mt5.symbol_info_tick(SYMBOL).bid
    sl = price + (STOP_LOSS * 0.0001)
    tp = price - (TAKE_PROFIT * 0.0001)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT_SIZE,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 123456,
        "comment": "Breakout Sell",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    print(f"Sell Order Sent: {result}")

# Main trading logic
def breakout_strategy():
    while True:
        bid, ask = get_price()
        print(f"Current Price: {bid}")

        if bid > RESISTANCE_LEVEL:
            print("Breakout above resistance! Placing Buy Order...")
            place_buy_order()

        elif bid < SUPPORT_LEVEL:
            print("Breakout below support! Placing Sell Order...")
            place_sell_order()

        time.sleep(10)  # Check every 10 seconds

# Run the bot
if __name__ == "__main__":
    if connect_mt5():
        breakout_strategy()
    mt5.shutdown()