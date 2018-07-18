"""
    Author: Lee Gim Yuen
    License: Apache 2.0 License
    Copyright 2015
"""
import json
from CITool import *
import pprint as pp
import requests
from Singleton import *

"""
Market Tag ID Lookup Table
=============================
Tag ID    Description
80    FX
81    FX FX-Major
82    FX AUD-Crosses
83    FX CHF-Crosses
84    FX EUR-Crosses
85    FX GBP-Crosses
86    FX Scandies-Crosses
87    FX JPY-Crosses
88    FX EM-Europe
89    FX EM-Asia
90    Indices
91    Indices UK
92    Indices US
93    Indices Europe
94    Indices Asia
95    Indices Australia
96    Commodities
97    Commodities Energy
98    Commodities Grain
99    Commodities Soft
100    Commodities Other
101    Commodities Options
102    Equities
103    Equities UK
104    Equities US
105    Equities Europe
106    Equities Asia
107    Equities Austria
108    Equities Belgium
109    Equities Canada
110    Equities Denmark
111    Equities France
112    Equities Germany
113    Equities Ireland
114    Equities Italy
115    Equities Netherlands
116    Equities Norway
117    Equities Poland
118    Equities Portugal
119    Equities Spain
120    Equities Sweden
121    Equities Switzerland
122    Equities Finland
123    Sectors
124    Sectors UK
125    Metals
126    Bonds
127    Interest Rates
128    iShares
129    iShares UK
130    iShares US
131    iShares Asia
132    iShares Australia
133    iShares Emerging-Markets
134    Options
135    Options UK 100
136    Options Germany 30
137    Options US SP 500
138    Options Wall Street
139    Options Australia 200
140    Options US Crude Oil
141    Options GBP/USD
142    Options EUR/USD
143    Options AUD/USD
144    Options Gold
145    Equities Australia
146    Popular
147    Popular Spreads
150    Popular Australia
"""


class COrderList:
    def __init__(self, orders):
        if len(orders) <= 0:
            self.orders = []
            return
        self.orders = orders

    def select_orders_by_marketID(self, marketID):
        orders = []
        for order in self.orders:
            if order["MarketId"] == marketID:
                orders.append(order)
        return orders


class API(Singleton):
    """Summary of API
    This is a Cityindex API Class.
    Features:
        * Authentication
            - login
            - logout
        * Account Information
            -Get Client and Trading Account
        * Margin
            - Get Client Account Margin
        * Market
            - Full Search With Tags
        * Trades and Orders
            - send a Market Order
            - simulate Trade order
            - Modify Order
        * Price History

    """
    OP_BUY = "buy"
    OP_SELL = "sell"

    def __init__(self, uid, password, isLive=True):
        """

        :param uid:         Username
        :param password:    Password
        :param isLive:      Live or Production
        :return:
        """
        self.uid = uid
        self.password = password
        self.trading_account_info = {}
        self.client_account_margin = {}
        if isLive:
            self.APIURL = 'https://ciapi.cityindex.com/TradingAPI'
        else:
            self.APIURL = "https://ciapipreprod.cityindextest9.co.uk/TradingApi/"

    """
            Authentication
    ===============================
    """

    def login(self):
        """
        Login to CityIndex
        :return:
        """
        data = {'Password': self.password,
                'AppVersion': '1',
                'AppComments': 'LoginFromPython',
                'Username': self.uid,
                'AppKey': 'cipythonAPP'}
        url = self.APIURL + '/session'
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json.dumps(data), headers=headers)
        if response.status_code != 200:
            print("Failed Login " + str(response.status_code))
            return False

        self.login_resp = response.json()
        self.session = response.json()["Session"]
        return True

    def logout(self):
        """
        Logout of Cityindex
        :return:
        """
        data = {"Username": self.uid, "Session": self.session}
        url = self.APIURL + '/session/deleteSession?Username=' + self.uid + '&Session=' + self.session
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json.dumps(data), headers)
        if response.status_code != 200:
            print("Failed Logout " + str(response.status_code))
            return False

        return True

    """
            Account Information
    ===============================

    """

    def get_trading_account_info(self):
        """
        Get User's ClientAccountId and a list of their TradingAccounts
        :return: [dictionary] AccountInformationResponseDTO
        """
        data = {"Username": self.uid, "Session": self.session}
        url = self.APIURL + "/useraccount/ClientAndTradingAccount"
        response = requests.get(url, data)

        if response.status_code != 200:
            print("Error retrieving Trading Acc info: " + str(response.status))
            return False

        self.trading_account_info = response.json()
        return self.trading_account_info

    """
            Margin
    ===============================
    """

    def get_client_account_margin(self):
        """
        Retrieves the current margin values for the logged-in client account.
        :return: ApiClientAccountMarginResponseDTO
        """
        url = self.APIURL + '/margin/clientaccountmargin?Username=' + self.uid + '&Session=' + self.session
        response = requests.get(url)
        if response.status_code != 200:
            print("Error getting clientaccountmargin : " + str(response.status_code))
            return False
        self.client_account_margin = response.json()
        return self.client_account_margin

    """
            Market
    ===============================
    """

    def get_full_market_info(self, tagId="0"):
        """
        Return market information
        :param tagId: [string] market Tag IDs
        :return: [Dictionary] market_info[UnderlyingRicCode]
        """

        url = self.APIURL + "/market/fullsearchwithtags?Username=" + self.uid + "&Session=" + self.session + "&maxResults=200&tagId=" + tagId
        response = requests.get(url)
        if response.status_code != 200:
            return False

        response = json.loads(response.text)
        self.market_info = {}
        for symbol in response["MarketInformation"]:
            self.market_info[symbol["UnderlyingRicCode"]] = symbol

        return self.market_info

    """
            Price History
    ===============================
    """

    def get_pricebar_history(self, symbol, interval="HOUR", span="1", pricebars="65535", priceType="BID"):
        """
        Get historic price bars for the specified market in OHLC (open, high, low, close) format,
        suitable for plotting in candlestick charts. Returns price bars in ascending order up to the current time.
        When there are no prices for a particular time period, no price bar is returned.
        Thus, it can appear that the array of price bars has "gaps", i.e.
        the gap between the date & time of each price bar might not be equal to interval x span.

        :param symbol: ricCode (not the marketTagID)
        :param interval: [string] (TICK, MINUTE, HOUR, DAY, WEEK)
        :param span: [string] (1, 2, 3, 5, 10, 15, 30 MINUTE) and (1, 2, 4, 8 HOUR) TICK, DAY and WEEK must be supplied with a span of 1
        :param pricebars: [string] number of pricebars in string
        :param priceType: [string] BID, MID, ASK
        :return: GetPriceBarResponseDTO
        """
        url = self.APIURL + "/market/" + str(
            self.market_info[symbol][
                "MarketId"]) + "/barhistory?Username=" + self.uid + "&Session=" + self.session + "&interval=" + interval + "&span=" + span + "&PriceBars=" + pricebars + "&PriceType=" + priceType
        response = requests.get(url)
        if (response.status_code != 200):
            print("GetPriceBarHistory: HTTP Error " + str(response.status_code))
            return False

        return response.json()

    """
            Trades and Orders
    ===============================
    """

    def simulate_trade_order(self, symbol, cmd, qty, data):
        """

        :param symbol:
        :param cmd:
        :param qty:
        :return:
        """

        url = self.APIURL + '/order/simulate/newtradeorder?Username=' + self.uid + "&Session=" + self.session
        data = {
            "OcoOrder": None,
            "Applicability": None,
            "Direction": cmd,
            "BidPrice": data["Bid"],
            "AuditId": data["AuditId"],
            "AutoRollover": False,
            "MarketId": self.market_info[symbol]["MarketId"],
            "isTrade": True,
            "OfferPrice": data["Offer"],
            "Quantity": qty,
            "QuoteId": None,
            "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
            "PositionMethodId": 1,
            "IfDone": []
        }

        pp.pprint(data)

        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json.dumps(data), headers=headers)
        if response.status_code != 200:
            print("Error SimulateTrade : " + str(response.status_code))
            print("Reason: " + response.reason)
            print("URL " + url)
            return False
        pp.pprint(response.json())
        return response.json()

    def orders_total(self):
        url = self.APIURL + '/order/openpositions'
        data = {"Username": self.uid, "Session": self.session,
                "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
                "maxResults": 10000}
        response = requests.get(url, data)
        if response.status_code != 200:
            print("ListOpenPositions Error: " + str(response.status_code))
            return False

        return len(response.json()["OpenPositions"])

    def get_orders(self):
        url = self.APIURL + '/order/openpositions'
        data = {"Username": self.uid, "Session": self.session,
                "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
                "maxResults": 10000}
        response = requests.get(url, data)
        if response.status_code != 200:
            print("ListOpenPositions Error: " + str(response.status_code))
            return False
        orders = COrderList(response.json()["OpenPositions"])
        return orders

    def get_order_history(self):
        url = self.APIURL + '/order/tradehistory'
        data = {"Username": self.uid, "Session": self.session,
                "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
                "maxResults": 10000}
        response = requests.get(url, data)
        if response.status_code != 200:
            print("ListOpenPositions Error: " + str(response.status_code))
            return False
        orders = COrderList(response.json()["TradeHistory"])
        return orders

    def get_order(self, orderId):
        """

        :param orderId:
        :return:
        """
        url = self.APIURL + "/order/" + str(orderId) + "?UserName=" + self.uid + "&Session=" + self.session
        print("Get Order URL : " + url)
        response = requests.get(url)
        if response.status_code != 200:
            print("Get Order Error: " + str(response.status_code))
            return False
        pp.pprint(response.json())
        return response.json()

    def close_order(self, symbol, order, data):
        """

        :return:
        """
        orderID = order["OrderId"]
        cmd = order["Direction"]
        qty = order["Orders"][0]["Quantity"]

        if cmd == self.OP_BUY:
            oppcmd = self.OP_SELL
        else:
            oppcmd = self.OP_BUY

        data = {
            "PositionMethodId": None,
            "BidPrice": data["Bid"],
            "OfferPrice": data["Offer"],
            "AuditId": data["AuditId"],
            "MarketId": self.market_info[symbol]["MarketId"],
            "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
            "Direction": oppcmd,  # must have!
            "Quantity": qty,
            "Close": [orderID]
        }
        url = self.APIURL + '/order/newtradeorder?Username=' + self.uid + "&Session=" + self.session
        headers = {'Content-type': 'application/json'}
        pp.pprint(data)
        response = requests.post(url, json.dumps(data), headers=headers)
        if response.status_code != 200:
            print("Error Update Trade : " + str(response.status_code))
            print("Reason: " + response.reason)
            print("URL " + url)
            return False
        pp.pprint(response.json())
        return response.json()

    def modify_order(self, symbol, order, stoploss=0.0, takeprofit=0.0, Guaranteed=False):
        orderID = order["OrderId"]
        qty = order["Orders"][0]["Quantity"]
        IfDone = order["Orders"][0]["IfDone"]
        cmd = order["Direction"]

        if cmd == self.OP_BUY:
            oppcmd = self.OP_SELL
        else:
            oppcmd = self.OP_BUY

        stoploss = round(stoploss, self.market_info[symbol]["PriceDecimalPlaces"])
        takeprofit = round(takeprofit, self.market_info[symbol]["PriceDecimalPlaces"])

        data = {
            "MarketId": self.market_info[symbol]["MarketId"],
            "OrderId": orderID,
            "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
            "IfDone": [],
            "Direction": cmd  # must have!
        }

        if stoploss > 0.0:
            stopLossData = {"Stop": {
                "TriggerPrice": stoploss,
                # "OrderId" : order["Orders"][0]["IfDone"][0]["Stop"]["OrderId"],
                "Direction": oppcmd,
                "Quantity": qty
                # "ParentOrderId":order["Orders"][0]["IfDone"][]
            }}

            for stoplimitorder in IfDone:
                if stoplimitorder["Stop"] is not None:
                    stopLossData["Stop"]["OrderId"] = stoplimitorder["Stop"]["OrderId"]

            data["IfDone"].append(stopLossData)

        if takeprofit > 0.0:
            limitData = {"Limit": {
                "TriggerPrice": takeprofit,
                "Direction": cmd,
                "Quantity": qty
                # "ParentOrderId":orderID
            }}
            for stoplimitorder in IfDone:
                if stoplimitorder["Limit"] is not None:
                    limitData["Limit"]["OrderId"] = stoplimitorder["Limit"]["OrderId"]
            data["IfDone"].append(limitData)

        url = self.APIURL + '/order/updatetradeorder?Username=' + self.uid + "&Session=" + self.session
        headers = {'Content-type': 'application/json'}
        pp.pprint(data)
        response = requests.post(url, json.dumps(data), headers=headers)
        if response.status_code != 200:
            print("Error Update Trade : " + str(response.status_code))
            print("Reason: " + response.reason)
            print("URL " + url)
            return False
        pp.pprint(response.json())
        return response.json()

    def send_market_order(self, symbol, cmd, qty, data, stoploss=0.0, takeprofit=0.0, Guaranteed=False):
        """
        Place a trade on a particular market using market price

        :param symbol: [string] ricCode
        :param cmd: [string] OP_BUY or OP_SELL
        :param qty: [integer] qty of contract to place
        :param stoploss: [double] stop loss price
        :param takeprofit: [double] take profit price
        :param Guaranteed: [Boolean] To be Implemented
        :return: False if failed, True return ApiTradeOrderResponseDTO
        """
        stoploss = round(stoploss, self.market_info[symbol]["PriceDecimalPlaces"])
        takeprofit = round(takeprofit, self.market_info[symbol]["PriceDecimalPlaces"])
        qty = round(qty, 0)

        if qty < self.market_info[symbol]['WebMinSize']:
            print("qty " + str(qty) + " < WebminSize[" + str(self.market_info[symbol]['WebMinSize']) + "]")
            return False

        if cmd == self.OP_BUY and qty > self.market_info[symbol]['MaxLongSize']:
            print("qty " + str(qty) + " > MaxLongSize[" + str(self.market_info[symbol]['MaxLongSize']) + "]")
            return False

        if cmd == self.OP_SELL and qty > self.market_info[symbol]['MaxShortSize']:
            print("qty " + str(qty) + " > MaxShortSize[" + str(self.market_info[symbol]['MaxShortSize']) + "]")
            return False

        url = self.APIURL + '/order/newtradeorder?Username=' + self.uid + "&Session=" + self.session
        data = {
            "IfDone": [],
            "Direction": cmd,
            # "ExpiryDateTimeUTCDate":null,
            # "LastChangedDateTimeUTCDate":null,
            # "OcoOrder":null,
            # "Type":null,
            # "ExpiryDateTimeUTC":null,
            # "Applicability":null,
            # "TriggerPrice":null,
            "BidPrice": data["Bid"],
            "AuditId": data["AuditId"],
            "AutoRollover": True,
            "MarketId": self.market_info[symbol]["MarketId"],
            "OfferPrice": data["Offer"],
            # "OrderId":0,
            "Currency": self.market_info[symbol]["MarketSizesCurrencyCode"],
            "Quantity": qty,
            "QuoteId": None,
            # "LastChangedDateTimeUTC":None,
            "PositionMethodId": 2,
            "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
            # "MarketName":"Wall Street CFD",
            # "Status":null,
            "isTrade": True
            # "Reference":"PythonAPI"
        }

        if cmd == self.OP_BUY:
            oppcmd = self.OP_SELL
        else:
            oppcmd = self.OP_BUY

        if stoploss > 0.0:
            data["IfDone"].append({"Stop": {
                # "Guaranteed" : Guaranteed,
                "TriggerPrice": stoploss,
                "Direction": oppcmd,
                "MarketId": self.market_info[symbol]["MarketId"],
                "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
                "Quantity": qty
                # "ExpiryDateTimeUTC" : None,
                # "Applicability" : "GTC",
                # "ParentOrderId" : 0
            }})

        if takeprofit > 0.0:
            data["IfDone"].append({"Limit": {
                "TriggerPrice": takeprofit,
                "Direction": oppcmd,
                "MarketId": self.market_info[symbol]["MarketId"],
                "TradingAccountId": self.trading_account_info["TradingAccounts"][0]["TradingAccountId"],
                "Quantity": qty
                # "Guaranteed" : Guaranteed,
                # "TriggerPrice" : takeprofit,
                # "ExpiryDateTimeUTC" : None,
                # "Applicability" : "GTC",
                # "ParentOrderId" : 0
            }})
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, json.dumps(data), headers=headers)
        if (response.status_code != 200):
            print("Error SimulateTrade : " + str(response.status_code))
            print("Reason: " + response.reason)
            print("URL " + url)
            return False

        jsonData = response.json()
        pp.pprint(jsonData)
        jsonData["Direction"] = cmd
        return jsonData

    def cross_rate(self, symbol, cmd, data):
        """
        Return the conversion rate from Trading Currency to Home Currency
        e.g. If you are trading US stock in USD and your home currency is SGD. The rate is to convert USD to SGD
        e.g. If you trading EURJPY currency in JPY and your home is SGD. The rate convert JPY to SGD

        Rate = Trading Currency / Home Currency
        (how much Trading Currency per $1 Home Currency)

        :param symbol:
        :param cmd:
        :return: cross_rate
        """
        qty = self.market_info[symbol]["WebMinSize"]

        simulatedOrder = self.simulate_trade_order(symbol, cmd, qty, data)
        if not simulatedOrder:
            return False

        if simulatedOrder["Status"] != 1:
            return False

        if simulatedOrder["StatusReason"] != 1:
            return False

        #Total Margin required after this trade
        SimulatedTotalMarginRequirement = simulatedOrder["SimulatedTotalMarginRequirement"]
        #Total current Margin
        actualTotalMargin = simulatedOrder["ActualTotalMarginRequirement"]

        SimulatedTotalMarginRequirement = SimulatedTotalMarginRequirement - actualTotalMargin

        if SimulatedTotalMarginRequirement <= 0.0:
            return False

        marginUnit = self.market_info[symbol]["MarginFactorUnits"]
        marginFactor = self.market_info[symbol]["MarginFactor"]
        marginMultiplier = 1.0

        if marginUnit == 26:  # %
            marginMultiplier = marginFactor / 100.0
        elif marginFactor == 27:
            marginMultiplier = marginFactor

        qtyMultiplier = 1.0 / self.market_info[symbol]["BetPer"]
        qty = qty * qtyMultiplier

        if cmd == self.OP_BUY:
            totalTradingCash = qty * data["Offer"] * marginMultiplier
        else:
            totalTradingCash = qty * data["Bid"] * marginMultiplier

        crossRate = totalTradingCash / SimulatedTotalMarginRequirement

        return crossRate


class Context:
    lightstreamer_url = 'https://push.cityindex.com'

    def __init__(self, symbol, ea_param, time_interval, time_span, handle_data, bars_count="65000"):
        self.high = []
        self.low = []
        self.close = []
        self.open = []
        self.time = []
        self.data = {}
        self.indicators = []
        self.clientAccountMarginData = {}
        self.EAParam = ea_param
        self.symbol = symbol
        self.TimeInterval = time_interval
        self.TimeSpan = time_span
        self.BarsCount = bars_count
        self.handle_data = handle_data
        self.LS_PRICE_DATA_ADAPTER = "PRICES"
        self.LS_PRICE_ID = "PRICE."
        self.LS_PRICE_SCHEMA = ["MarketId", "AuditId", "Bid",
                                "Offer", "Change", "Direction",
                                "High", "Low", "Price", "StatusSummary",
                                "TickDate"]
        self.LS_MARGIN_DATA_ADAPTER = "CLIENTACCOUNTMARGIN"
        self.LS_MARGIN_ID = "CLIENTACCOUNTMARGIN"
        self.LS_MARGIN_SCHEMA = ["Cash",
                                 "CurrencyId",
                                 "CurrencyISO",
                                 "Margin",
                                 "MarginIndicator",
                                 "NetEquity",
                                 "OpenTradeEquity",
                                 "TradeableFunds",
                                 "PendingFunds",
                                 "TradingResource",
                                 "TotalMarginRequirement"]

    def init_data(self):
        api = API()
        self.LS_PRICE_ID = self.LS_PRICE_ID + str(api.market_info[self.symbol]["MarketId"])
        self.clientAccountMarginData = api.get_client_account_margin()

        priceBars = False
        while not priceBars:
            priceBars = api.get_pricebar_history(self.symbol,
                                                 self.TimeInterval,
                                                 self.TimeSpan,
                                                 self.BarsCount)

        for counter, price in enumerate(priceBars["PriceBars"]):
            self.high.insert(0, price["High"])
            self.low.insert(0, price["Low"])
            self.close.insert(0, price["Close"])
            self.open.insert(0, price["Open"])
            self.time.insert(0, wcfDate2Sec(price["BarDate"]))

        partialBar = priceBars["PartialPriceBar"]

        self.high.insert(0, partialBar["High"])
        self.low.insert(0, partialBar["Low"])
        self.close.insert(0, partialBar["Close"])
        self.open.insert(0, partialBar["Open"])
        self.time.insert(0, wcfDate2Sec(partialBar["BarDate"]))

    def update_data(self):
        api = API()
        last_time_sec = self.time[0];
        time_diff = int((time.time() - last_time_sec) / intervalUnitSec(self))

        priceBars = False
        while not priceBars:
            priceBars = api.get_pricebar_history(self.symbol,
                                                 self.TimeInterval,
                                                 self.TimeSpan,
                                                 str(time_diff + 2))

        partialBar = priceBars["PartialPriceBar"]
        curTime = wcfDate2Sec(partialBar["BarDate"])

        self.high[0] = partialBar["High"]
        self.low[0] = partialBar["Low"]
        self.open[0] = partialBar["Open"]
        self.close[0] = partialBar["Close"]
        self.time[0] = curTime

        for counter, price in enumerate(priceBars["PriceBars"]):
            time_sec = wcfDate2Sec(price["BarDate"])
            time_diff = int((time_sec - self.time[1]) / intervalUnitSec(self))

            if time_diff > 0:
                self.high.insert(1, price["High"])
                self.low.insert(1, price["Low"])
                self.close.insert(1, price["Close"])
                self.open.insert(1, price["Open"])
                self.time.insert(1, time_sec)

    def prepare_data(self, data):
        tableNo = data["_tableIdx_"]
        if tableNo == 1:
            data['TickDate'] = wcfDate2Sec(data['TickDate'])
            if data['Offer']:
                data['Offer'] = float(data['Offer'])
            else:
                if len(self.data) > 0:
                    if self.data["Offer"]:
                        data['Offer'] = self.data["Offer"]

            if data['Bid']:
                data['Bid'] = float(data['Bid'])
            else:
                if len(self.data) > 0:
                    if self.data["Bid"]:
                        data['Bid'] = self.data["Bid"]
            self.data = data

            self.update_data()

            for counter, indicator in enumerate(self.indicators):
                indicator.onCalculate(self, len(self.time))
            self.handle_data(self, data)
        elif tableNo == 2:
            if data["Cash"]:
                self.clientAccountMarginData["Cash"] = data["Cash"]
            if data["CurrencyISO"]:
                self.clientAccountMarginData["CurrencyISO"] = data["CurrencyISO"]
            if data["CurrencyId"]:
                self.clientAccountMarginData["CurrencyId"] = data["CurrencyId"]
            if data["Margin"]:
                self.clientAccountMarginData["Margin"] = data["Margin"]
            if data["MarginIndicator"]:
                self.clientAccountMarginData["MarginIndicator"] = data["MarginIndicator"]
            if data["NetEquity"]:
                self.clientAccountMarginData["NetEquity"] = data["NetEquity"]
            if data["OpenTradeEquity"]:
                self.clientAccountMarginData["OpenTradeEquity"] = data["OpenTradeEquity"]
            if data["PendingFunds"]:
                self.clientAccountMarginData["PendingFunds"] = data["PendingFunds"]
            if data["TotalMarginRequirement"]:
                self.clientAccountMarginData["TotalMarginRequirement"] = data["TotalMarginRequirement"]
            if data["TradeableFunds"]:
                self.clientAccountMarginData["TradeableFunds"] = data["TradeableFunds"]
            if data["TradingResource"]:
                self.clientAccountMarginData["TradingResource"] = data["TradingResource"]


if __name__ == "__main__":
    accid = raw_input("Enter City Index account ID: ")
    password = raw_input("Enter City Index password: ")

    api = API(accid, password)

    print("Test Login...")
    if api.login():
        print("\tSuccess!\n\n")
    else:
        print("\tFailed\n\n")
        exit()

    print("Test Trading Account Information...")
    if api.get_trading_account_info():
        pp.pprint(api.trading_account_info)
        print("\tSuccess!")
    else:
        print("\tFailed\n\n")
        api.logout()
        exit()

    print("Test Margin Info...")
    if api.get_client_account_margin():
        pp.pprint(api.client_account_margin)
        print("\tSuccess!")
    else:
        print("\tFailed\n\n")
        api.logout()
        exit()

    print("Test get FX-major (81) market info...")
    if api.get_full_market_info("81"):
        pp.pprint(api.market_info)
        print("\tSuccess!")
    else:
        print("\tFailed\n\n")
        api.logout()
        exit()

    print("Test Get 3x EUR/USD 1 HOUR BID price Bar History...")
    price_bars = api.get_pricebar_history("41", "HOUR", "1", "3", "3")
    if price_bars:
        pp.pprint(price_bars)
        print("\tSuccess!")
    else:
        print("\tFailed\n\n")
        api.logout()
        exit()

    print("Test Get Order History...")
    orders = api.get_order_history()
    if orders:
        pp.pprint(orders.orders)
        print("\tSuccess!")
    else:
        print("\tFailed\n\n")
        api.logout()
        exit()

    print("Test Logout...")
    if api.logout():
        print("\tSuccess!\n\n")
    else:
        print("\tFailed\n\n")
