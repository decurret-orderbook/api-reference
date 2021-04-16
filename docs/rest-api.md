# REST APIs

## 接続先URL（エンドポイント）
https://api-trade.decurret.com

## APIの制限について
APIにはIPアドレスごとに以下の回数制限があります。上限を超えた場合はエラーレスポンスが返却されます。

|対象|回数制限|
|---|-------|
|IPアドレス|5,000回/分|

### リクエストの仕様について
* 適切なHTTPメソッドを設定して下さい。
* リクエストパラメーターについて
  * GET, DELETEはクエリパラメーターにて指定して下さい。
  * POST, PUTはリクエストボディにて指定して下さい。

#### 認証の方法
プライベートAPIを利用するためには、あらかじめ発行したAPIキーとAPIシークレットを用いた\
認証ヘッダーを設定する必要があります。
* API-KEY, NONCE, SIGNATUREをリクエストヘッダーに付けて通信する。
  * API-KEY: 取引所ページでユーザー毎に発行するAPIキー
  * SECRET: API-KEYと同時に発行されるAPIシークレット
  * NONCE: ミリ秒のtimestamp
  * SIGNATURE: 下記の通り生成するユニーク値

#### SIGNATUREの作り方
* 下記文字列を、SECRETを使ってHMAC SHA-256でハッシュ化する
* GET, DELETE: NONCE + URI + queryString
  * 1586345939000/v1/spot/order/65?id=1
* POST, PUT: NONCE + Json encoded request body
  * 1586345939000{"label":"apiKeyLabel"}

### レスポンスの仕様について
* 通信の成否は全てレスポンスのHTTPステータスコードで判別します。


## パブリックAPI


### symbol
通貨ペア情報の取得
```
GET /api/v1/symbol
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
#### response
```json
[
  {
    "id": 1,
    "tradeType": "SPOT",
    "currencyPair": "BTC_JPY",
    "startAt": null,
    "endAt": null,
    "baseCurrency": "BTC",
    "quoteCurrency": "JPY",
    "basePrecision": 5,
    "quotePrecision": 0,
    "makerTradeFeePercent": -0.03,
    "takerTradeFeePercent": 0.23,
    "tradable": true,
    "enabled": true
  },
  ...
]
```


### ticker
ティッカーの取得
```
GET /api/v1/ticker
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
#### response
```json
{
  "symbolId": 1,
  "bestAsk": 6885501.0,
  "bestBid": 6880225.0,
  "open": 6883783,
  "high": 6886751,
  "low": 6881398,
  "last": 6884332,
  "volume": 94.71371641,
  "timestamp": 1618577903540
}
```


### candlestick
過去のローソク足の取得
```
GET /api/v1/candlestick
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
candlestickType | string | YES | ローソク足の種類。ISO8601に準拠しています。 ex) 1分足: PT1M, 1時間足: PT1H, 日足: P1D, 週足: P1W, 月足: P1M
dateFrom | long | NO | 取得開始日時
dateTo | long | NO | 取得終了日時
#### response
```json
{
  "symbolId": 1,
  "candlesticks": [
    {
      "open": 6883783.0,
      "high": 6885002.0,
      "low": 6882987.0,
      "close": 6883923.0,,
      "volume": 94.713,
      "time": 1618546680000
    },
    ...
  ],
  "timestamp": 1618576651985
}
```


### orderbook
オーダーブックの取得
```
GET /api/v1/orderbook
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
#### response
```json
{
  "symbolId": 1,
  "asks": [
    {
      "price": 6885501.0,
      "amount": 0.1
    },
    ...
  ],
  "bids": [
    {
      "price": 6880225.0,
      "amount": 0.00396
    },
    ...
  ],
  "timestamp": 1618576807625,
  "bestBid": 6880225.0,
  "bestAsk": 6885501.0,
  "averageBid": 6918910.099045686,
  "averageAsk": 6729394.106051771,
  "midPrice": 6882863.0,
  "spread": 5276.0
}
```

### trades
約定履歴（歩み値）の取得
```
GET /api/v1/trades
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
#### response
```json
{
  "symbolId": 1,
  "trades": [
    {
      "id": 789,
      "orderSide": "BUY",
      "price": 6883783.0,
      "amount": 0.04,
      "tradedAt": 1618449345751
    },
    ...
  ]
  "timestamp": 1618577999520
}
```


## プライベートAPI ##
上述した認証ヘッダーが必要なAPIです。

### asset
残高の取得
```
GET /api/v1/asset
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
#### response
```json
[
  {
    "userId": 123,
    "currency": "BTC",
    "jpyOnhandAmount": 7000000,
    "jpyLockedAmount": 2100000,
    "onhandAmount": "1.00000001",
    "lockedAmount": "0.30000001",
    "unlockedAmount": "0.7",
  },
  ...
]
```


### get spot order
注文明細の取得（詳細な条件を指定可能）
```
GET /api/v1/spot/order
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
id | long | NO | 注文ID
idFrom | long | NO | 検索開始注文ID
idTo | long | NO | 検索終了注文ID
dateFrom | long | NO | 取得開始日時
dateTo | long | NO | 取得終了日時
orderStatus | string | NO | WAITING, UNFILLED, PARTIALLY_FILLED
orderType | string | NO | MARKET, LIMIT
orderSide | string | NO | SELL, BUY
number | int | NO | ページ番号。default: 0
size | int | NO | 1ページに表示する件数。default: 30
#### response
```json
[
  {
    "id": 123,
    "symbolId": 1,
    "userId": 123,
    "orderSide": "BUY",
    "orderType": "LIMIT",
    "price": 6800000.0,
    "averagePrice": 0,
    "amount": 0.1,
    "remainingAmount": 0.1,
    "orderStatus": "UNFILLED",
    "orderOperator": "USER",
    "orderChannel": "PC_WEB",
    "createdAt": 1618577044481,
    "updatedAt": 1618577044481,
  },
  ...
]
```

### get active spot order
オープンな注文明細の取得
```
GET /api/v1/spot/order/active
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
#### response
```json
[
   {
    "id": 123,
    "symbolId": 1,
    "userId": 123,
    "orderSide": "BUY",
    "orderType": "LIMIT",
    "price": 6800000.0,
    "averagePrice": 0,
    "amount": 0.1,
    "remainingAmount": 0.1,
    "orderStatus": "UNFILLED",
    "orderOperator": "USER",
    "orderChannel": "PC_WEB",
    "createdAt": 1618577044481,
    "updatedAt": 1618577044481,
  },
  ...
]
```

### post spot order
成行・指値の発注
```
POST /api/v1/spot/order
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
orderType | string | YES | MARKET, LIMIT
orderSide | string | YES | SELL, BUY
price | decimal | NO | 注文価格。orderType=LIMITの時に指定する。
amount | decimal | YES | 注文数量
#### response
```json
{
  "id": 123,
  "symbolId": 1,
  "userId": 123,
  "orderSide": "BUY",
  "orderType": "LIMIT",
  "price": 6800000.0,
  "averagePrice": 0,
  "amount": 0.1,
  "remainingAmount": 0.1,
  "orderStatus": "UNFILLED",
  "orderOperator": "USER",
  "orderChannel": "API_KEY",
  "createdAt": 1618577044481,
  "updatedAt": 1618577044481,
}

```

### delete spot order
指値注文のキャンセル
```
DELETE /api/v1/spot/order
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
id | long | YES | 注文id
#### response
```json
{
  "id": 123,
  "symbolId": 1,
  "userId": 123,
  "orderSide": "BUY",
  "orderType": "LIMIT",
  "price": 6800000.0,
  "averagePrice": 0,
  "amount": 0.1,
  "remainingAmount": 0.1,
  "orderStatus": "UNFILLED_CANCELED",
  "orderOperator": "USER",
  "orderChannel": "API_KEY",
  "createdAt": 1618577044481,
  "updatedAt": 1618577044481,
}
```

### get spot trade
約定明細の取得
```
GET /api/v1/spot/trade
```
#### parameters
Name | Type | Mandatory | Description
--- | --- | --- | ---
symbolId | long | YES | symbolId
id | long | NO | 注文ID
idFrom | long | NO | 検索開始注文ID
idTo | long | NO | 検索終了注文ID
dateFrom | long | NO | 取得開始日時
dateTo | long | NO | 取得終了日時
orderType | string | NO | MARKET, LIMIT
orderSide | string | NO | SELL, BUY
number | int | NO | ページ番号。default: 0
size | int | NO | 1ページに表示する件数。default: 30
#### response
```json
[
  {
    "id": 123,
    "symbolId": 1,
    "userId": 123,
    "orderSide": "BUY",
    "orderType": "LIMIT",
    "price": 6883783.0,
    "amount": 0.1,
    "tradeAction": "MAKER",
    "orderId": 456,
    "fee": -64.0,
    "orderChannel": "PC_WEB",
    "jpyConversion": 1,
    "createdAt": 1611029776000,
    "updatedAt": 1611029776000
  },
  ...
]
```


