# -*- coding: utf-8 -*-
import requests
import hashlib
import hmac
import time
import json
import urllib

class AuthException(Exception):
    def __init__(self):
        msg = "Please specify your valid API Key and API Secret."
        super(AuthException, self).__init__(msg)

class API(object):
    def __init__(self, api_key=None, api_secret=None):
        self.api_url = "https://api-trade.decurret.com"
        self.api_key = api_key
        self.api_secret = api_secret

    def request(self, endpoint, method="GET", params=None):
        url = self.api_url + endpoint
        body = ""
        auth_header = None
        if method == "POST":
            body = json.dumps(params)
        elif method == "PUT":
            body = json.dumps(params)
        elif method == "DELETE":
            if params:
                body = endpoint + "?" + urllib.parse.urlencode(params)
            else:
                body = endpoint
        else: # GET
            if params:
                body = endpoint + "?" + urllib.parse.urlencode(params)
            else:
                body = endpoint
        if self.api_key and self.api_secret:
            nonce = str(round(time.time() * 1000))
            message = nonce + body
            signature = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()
            auth_header = {
                'API-KEY': self.api_key,
                'NONCE': nonce,
                'SIGNATURE': signature,
                'Content-Type': 'application/json'
            }
        try:
            with requests.Session() as s:
                if auth_header:
                    s.headers.update(auth_header)
                if method == "GET":
                    response = s.get(url, params=params)
                elif method == "POST":
                    response = s.post(url, data=json.dumps(params))
                elif method == "PUT":
                    response = s.put(url, data=json.dumps(params))
                else: # DELETE
                    response = s.delete(url, params=params)
        except requests.RequestException as e:
            print("RequestException", e)
            raise e
        content = ""
        if len(response.content) > 0:
            try:
                content = json.loads(response.content.decode("utf-8"))
            except json.decoder.JSONDecodeError as e:
                print("JSON Decode Error", response.content)
        return content

    """HTTP Public API"""
    def get_candles(self, **params):
        """
        Name	        Type	Mandatory	Description
        symbolId	    long	YES	        symbolId
        candlestickType	string	YES	        1??????: PT1M, 1?????????: PT1H, ??????: P1D, ??????: P1W, ??????: P1M
        dateFrom	    long	NO	        ??????????????????
        dateTo	        long	NO	        ??????????????????
        """
        endpoint = "/api/v1/candlestick"
        return self.request(endpoint, params=params)

    def get_trades(self, **params):
        """
        Name    	Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        """
        endpoint = "/api/v1/trades"
        return self.request(endpoint, params=params)

    def get_ticker(self, **params):
        """
        Name    	Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        """
        endpoint = "/api/v1/ticker"
        return self.request(endpoint, params=params)

    def get_symbols(self, **params):
        """
        no query
        """
        endpoint = "/api/v1/symbol"
        return self.request(endpoint, params=params)

    def get_orderbook(self, **params):
        """
        Name	    Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        """
        endpoint = "/api/v1/orderbook"
        return self.request(endpoint, params=params)

    """HTTP Privarte API"""
    def get_asset(self, **params):
        """
        no query
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/asset"
        return self.request(endpoint, params=params)

    def get_orders(self, **params):
        """
        Name	    Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        id	        long	NO      	??????ID
        idFrom	    long	NO      	??????????????????ID
        idTo	    long	NO	        ??????????????????ID
        dateFrom	long	NO	        ??????????????????
        dateTo	    long	NO	        ??????????????????
        orderStatus	string	NO
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/spot/order"
        return self.request(endpoint, params=params)

    def get_active_orders(self, **params):
        """
        Name    	Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/spot/order/active"
        return self.request(endpoint, params=params)

    def post_order(self, **params):
        """
        Name	    Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        orderType	string	YES	        MARKET, LIMIT, STOP
        orderSide	string	YES	        SELL, BUY
        price	    decimal	NO	        ???????????????orderType=LIMIT????????????????????????
        amount	    decimal	YES	        ????????????
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/spot/order"
        return self.request(endpoint, method="POST", params=params)

    def cancel_order(self, **params):
        """
        Name	    Type	Mandatory	Description
        symbolId	long	YES	        symbolId
        id	        long	YES	        ??????id
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/spot/order"
        return self.request(endpoint, method="DELETE", params=params)

    def get_execution(self, **params):
        """
        Name	    Type	Mandatory	Description
        symbolId	long	NO	        symbolId
        id	        long	NO	        ??????ID
        idFrom	    long	NO	        ??????????????????ID
        idTo	    long	NO	        ??????????????????ID
        dateFrom	long	NO	        ??????????????????
        dateTo	    long	NO	        ??????????????????
        number	    int	    NO	        ??????????????????default: 0
        size	    int	    NO	        1?????????????????????????????????default: 30
        """
        if not all([self.api_key, self.api_secret]):
            raise AuthException()

        endpoint = "/api/v1/spot/trade"
        return self.request(endpoint, params=params)


if __name__ == '__main__':
    API_KEY = ''
    API_SECRET = ''
    dc = API(api_key=API_KEY, api_secret=API_SECRET)
    symbol = 1

    print("------public------")

    response = dc.get_orderbook(symbolId=symbol)
    print(response)

    response = dc.get_candles(symbolId=symbol,
                              candlestickType="PT1M")
    print(response)

    response = dc.get_symbols()
    print(response)

    response = dc.get_trades(symbolId=symbol)
    print(response)


    print("------private------")

    response = dc.get_asset()
    print(response)

    response = dc.get_active_orders(symbolId=symbol)
    print(response)

    response = dc.get_orders(symbolId=symbol,
                             size=20)
    print(response)

    response = dc.get_execution(symbolId=symbol,
                                size=20)
    print(response)

    # ???????????????????????????????????????????????????????????????
    # order(limit)
    # response = dc.post_order(symbolId=1,
    #                          orderType="LIMIT",
    #                          orderSide="BUY",
    #                          amount=0.0001,
    #                          price=5000000)
    # print(response)
    #
    # cancel
    # response = dc.cancel_order(symbolId=1,
    #                                id=999)
    # print(response)
    #