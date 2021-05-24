import websocket
import json
import pprint
import talib
import numpy
import config
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05

closes=[]
in_position = False

#initialised a new client
client = Client(config.API_KEY, config.API_SECRET, tld='us')

#the folln func works for both buying and selling
def order(symbol, side, order_type, quantity):
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol,side=side,type=order_type,quantity=qty)
        print(order)
        return True
    except Exception as e:
        return False

def on_open(ws):
    print('Connection Opened')

def on_close(ws):
    print('Connection Closed')

def on_message(ws, message):
    print('Message Received')
    msg = json.loads(message)
    #pprint.pprint(msg)

    candle = msg['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

    if len(closes) > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        print("All RSIs calculated")
        print(rsi)
        last_rsi = rsi[-1]
        print("Current RSI: {}".format(last_rsi))

        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                print("Sell!")
                #binance sell logic here
                success = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if success:
                    in_position = False
            else:
                print("Overbought but We dont own any")

        if last_rsi < RSI_OVERSOLD:
            if  in_position:
                print("Oversold and already acquired. Nothing to do now")
            else:
                print("BUY!")    
                #binance buy order logic here
                success = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if success:
                    in_position = True


ws = websocket.WebSocketApp(SOCKET, on_open=on_open ,on_close=on_close ,on_message=on_message)
ws.run_forever()