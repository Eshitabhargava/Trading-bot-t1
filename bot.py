import websocket
import json
import pprint

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
closes=[]

def on_open(ws):
    print('Connection Opened')

def on_close(ws):
    print('Connection Closed')

def on_message(ws, message):
    print('Message Received')
    msg = json.loads(message)
    pprint.pprint(msg)

    candle = msg['k']
    is_candle_clsoed = candle['x']
    close = candle['c']

    if is_candle_clsoed:
        print("candle closed at {}".format(close))
        closes.append(close)
        print("closes")
        print(closes)


ws = websocket.WebSocketApp(SOCKET, on_open=on_open ,on_close=on_close ,on_message=on_message)
ws.run_forever()