## websocket APIs


### 接続先URI（エンドポイント）
wss://api-trade.decurret.com/ws
<br><br>

### リクエストの仕様について
一般的に利用される様々なwebsocketの接続方法をご利用いただけます。\
websocket-client==1.31.22を用いたサンプルは以下の通りです。


```python
import websocket
import json

def on_message(wsapp, message):
    print(message)


def on_open(wsapp):
    wsapp.send(json.dumps({"op": "subscribe", "args": ["trade"]}))


if __name__ == '__main__':
    wsapp = websocket.WebSocketApp("wss://api-trade.decurret.com/ws",
                                   on_message=on_message,
                                   on_open=on_open)
    wsapp.run_forever()
```

<br><br>

#### 認証の方法
現在ご提供しているチャンネルはパブリックデータのみですので認証は不要です。
<br><br>

#### 接続上限について
上限はIPごとに2接続となっております。それ以上接続しようとしますとsubscribeできませんのでご注意ください。
<br><br>

#### 切断タイミング
以下を契機にwebsocketの接続が切断されます。
- 10分間受信がない
- 2時間接続後
- メンテナンス
<br><br>

#### 注意事項
受信するデータの順序性は保証できかねますので、受信種別によってはtimestampを確認しデータの破棄等を行うことを推奨いたします。\
また、現在はβバージョンであり、稀に3秒程度遅延が生じることがございます。予めご了承ください。


## パブリックAPI


### ticker
通貨ペア情報の取得
```
{"op": "subscribe", "args": ["ticker"]} # 全ての通貨ペアを取得
{"op": "subscribe", "args": ["ticker:1"]}  # BTCJPYを取得
```
#### parameters
値 | 通貨ペア|
--- | --- |
1|BTC_JPY
2|ETH_BTC
3|ETH_JPY 
8|XRP_JPY
9|ONT_JPY
10|QTUM_JPY

#### response
```json
type TickerResponse = {
  symbolId: number,
  bestAsk: number,
  bestBid: number,
  open: number,
  high: number,
  low: number,
  last: number,
  volume: number,
  timestamp: number;
	channel: "ticker"
}
```


### trade
約定明細の取得
```
{"op": "subscribe", "args": ["trade"]}　# すべての通貨ペアの約定を取得
{"op": "subscribe", "args": ["trade:2"]} # ETHBTCの約定明細を取得
```

#### parameters
値 | 通貨ペア|
--- | --- |
1|BTC_JPY
2|ETH_BTC
3|ETH_JPY 
8|XRP_JPY
9|ONT_JPY
10|QTUM_JPY

#### response
```json
type TradeResponse = {
  symbolId: number,
  trades: Trade[],
  timestamp: number,
	channel: "trade"
}

type Trade = {
  id: number,
  orderSide: "BUY" | "SELL",
  price: number,
  amount: number,
  tradedAt: number,
}
```


### orderbook
板データの取得
```
{"op": "subscribe", "args": ["orderbook"]} # すべての通貨ペアの板データを取得
{"op": "subscribe", "args": ["orderbook:3"]} # ETHJPの板データを取得
```
#### parameters
値 | 通貨ペア|
--- | --- |
1|BTC_JPY
2|ETH_BTC
3|ETH_JPY 
8|XRP_JPY
9|ONT_JPY
10|QTUM_JPY

#### response
```json
type OrderbookMessage = {
  symbolId: number,
  asks: OrderMessage[],
  bids: OrderMessage[],
  timestamp: number,
  bestBid: number,
  bestAsk: number,
  midPrice: number,
  spread: number,
	channel: "orderbook"
}

type OrderMessage = {
  action: action -> "insert" | "update" | "delete"
  side: side,    -> "Ask" | "Bid"
  price: number,
  amount: number,
}
```




