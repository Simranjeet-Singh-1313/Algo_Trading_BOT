
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *
import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time
#Vars
orderId = 1

entry_trade ={'AAPL': 0, 'MSFT': 0,'HD': 0, 'GOOG': 0, 'AMZN': 0, 'FB': 0, 'TSLA': 0, 'DIS' : 0, 'BRK B': 0,'TSM':  0, 'NVDA': 0, 'V': 0, 'BABA': 0, 'JNJ': 0,'JPM': 0, 'WMT': 0, 'UNH': 0, 'MA': 0, 'PG': 0}
position = {'AAPL': 0, 'MSFT': 0,'HD': 0, 'GOOG': 0, 'AMZN': 0, 'FB': 0, 'TSLA': 0, 'DIS' : 0, 'BRK B': 0,'TSM':  0, 'NVDA': 0, 'V': 0, 'BABA': 0, 'JNJ': 0,'JPM': 0, 'WMT': 0, 'UNH': 0, 'MA': 0, 'PG': 0}
close_bar = {1:0, 2:0,3:0 ,4:0 ,5:0, 6: 0,7: 0, 8:0, 9:0, 10:0, 11: 0,12: 0, 13: 0,14: 0,15: 0,16: 0, 17: 0, 18: 0, 19: 0}
high_bar = {1:0, 2:0,3:0 ,4:0 ,5:0, 6: 0,7: 0, 8:0, 9:0, 10:0, 11: 0,12: 0, 13: 0,14: 0,15: 0,16: 0, 17: 0, 18: 0, 19: 0}
low_bar = {1:0, 2:0,3:0 ,4:0 ,5:0, 6: 0,7: 0, 8:0, 9:0, 10:0, 11: 0,12: 0, 13: 0,14: 0,15: 0,16: 0, 17: 0, 18: 0, 19: 0}

initial_pop = {1:0, 2:0,3:0 ,4:0 ,5:0, 6: 0,7: 0, 8:0, 9:0, 10:0, 11: 0,12: 0, 13: 0,14: 0,15: 0,16: 0, 17: 0, 18: 0, 19: 0}
stocks_reqIds = {1: 'AAPL', 2: 'MSFT',3:'HD',4:'GOOG',5: 'AMZN', 6:'FB',7: 'TSLA', 8:'DIS', 9:'BRK B', 10:'TSM', 11:'NVDA',12:'V', 13:'BABA',14: 'JNJ',15:'JPM',16: 'WMT', 17:'UNH', 18:'MA', 19:'PG'}


#Class for Interactive Brokers Connection
class IBApi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self, self)
    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId,bar,False)
        except Exception as e:
            print(e)
    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId,bar,True)
        except Exception as e:
            print(e)
    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        print(reqId)
    # Get next order id we can use
    def nextValidId(self, nextorderId):
        global orderId
        orderId = nextorderId
    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)
#Bar Object
class Bar:
    open = 0
    low = 0
    high = 0
    close = 0
    volume = 0
    date = datetime.now()
    def __init__(self):
        self.open = 0
        self.low = 0
        self.high = 0
        self.close = 0
        self.volume = 0
        self.date = datetime.now()
#Bot Logic
class Bot:
    ib = None
    barsize = 1
    currentBar = Bar()
    bars =[]

    my_bars = {'AAPL':[], 'MSFT': [],'HD': [], 'GOOG':[], 'AMZN':[], 'FB':[], 'TSLA': [], 'DIS' :[], 'BRK B' : [], 'TSM': [], 'NVDA': [], 'V':[], 'BABA': [], 'JNJ': [],'JPM': [], 'WMT': [], 'UNH': [], 'MA': [], 'PG': []}
    reqId = 1
    global orderId
    smaPeriod_10 = 10
    smaPeriod_15 = 15
    symbol = ""
    bartime = {'AAPL': 0, 'MSFT': 0,'HD': 0, 'GOOG': 0, 'AMZN': 0, 'FB': 0, 'TSLA': 0, 'DIS' : 0, 'BRK B': 0,'TSM':  0, 'NVDA': 0, 'V': 0, 'BABA': 0, 'JNJ': 0,'JPM': 0, 'WMT': 0, 'UNH': 0, 'MA': 0, 'PG': 0}
    initialbartime = datetime.now().astimezone(pytz.timezone("America/New_York"))



    def __init__(self):
        #Connect to IB on init
        self.ib = IBApi()
        self.ib.connect('127.0.0.1', 7496, 0)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        currentBar = Bar()
        #Get symbol info
        self.portfolio = ['AAPL', 'MSFT', 'HD', 'GOOG', 'AMZN', 'FB', 'TSLA', 'DIS', 'BRK B', 'TSM', 'NVDA', 'V', 'BABA', 'JNJ', 'JPM', 'WMT', 'UNH', 'MA', 'PG']
        #Get bar size
        self.barsize = int(input("Enter the barsize you want to trade in minutes : "))
        mintext = " min"
        if (int(self.barsize) > 1):
            mintext = " mins"





        # for Stock in self.portfolio:

        # my contracts from portfolio
        self.contract1 = Contract()
        self.contract1.symbol = "AAPL"
        self.contract1.secType = "STK"
        self.contract1.exchange = "SMART"
        self.contract1.currency = "USD"

        self.contract2 = Contract()
        self.contract2.symbol = 'MSFT'
        self.contract2.secType = "STK"
        self.contract2.exchange = "SMART"
        self.contract2.currency = "USD"


        self.contract3 = Contract()
        self.contract3.symbol = 'HD'
        self.contract3.secType = "STK"
        self.contract3.exchange = "SMART"
        self.contract3.currency = "USD"

        self.contract4 = Contract()
        self.contract4.symbol = 'GOOG'
        self.contract4.secType = "STK"
        self.contract4.exchange = "SMART"
        self.contract4.currency = "USD"

        self.contract5 = Contract()
        self.contract5.symbol = 'AMZN'
        self.contract5.secType = "STK"
        self.contract5.exchange = "SMART"
        self.contract5.currency = "USD"

        self.contract6 = Contract()
        self.contract6.symbol = 'FB'
        self.contract6.secType = "STK"
        self.contract6.exchange = "SMART"
        self.contract6.currency = "USD"

        self.contract7 = Contract()
        self.contract7.symbol = 'TSLA'
        self.contract7.secType = "STK"
        self.contract7.exchange = "SMART"
        self.contract7.currency = "USD"

        self.contract8 = Contract()
        self.contract8.symbol = 'DIS'
        self.contract8.secType = "STK"
        self.contract8.exchange = "SMART"
        self.contract8.currency = "USD"

        self.contract9 = Contract()
        self.contract9.symbol = 'BRK B'
        self.contract9.secType = "STK"
        self.contract9.exchange = "SMART"
        self.contract9.currency = "USD"

        self.contract10 = Contract()
        self.contract10.symbol = 'TSM'
        self.contract10.secType = "STK"
        self.contract10.exchange = "SMART"
        self.contract10.currency = "USD"

        self.contract11 = Contract()
        self.contract11.symbol = 'NVDA'
        self.contract11.secType = "STK"
        self.contract11.exchange = "SMART"
        self.contract11.currency = "USD"

        self.contract12 = Contract()
        self.contract12.symbol = 'V'
        self.contract12.secType = "STK"
        self.contract12.exchange = "SMART"
        self.contract12.currency = "USD"

        self.contract13 = Contract()
        self.contract13.symbol = 'BABA'
        self.contract13.secType = "STK"
        self.contract13.exchange = "SMART"
        self.contract13.currency = "USD"

        self.contract14 = Contract()
        self.contract14.symbol = 'JNJ'
        self.contract14.secType = "STK"
        self.contract14.exchange = "SMART"
        self.contract14.currency = "USD"

        self.contract15 = Contract()
        self.contract15.symbol = 'JPM'
        self.contract15.secType = "STK"
        self.contract15.exchange = "SMART"
        self.contract15.currency = "USD"

        self.contract16 = Contract()
        self.contract16.symbol = 'WMT'
        self.contract16.secType = "STK"
        self.contract16.exchange = "SMART"
        self.contract16.currency = "USD"

        self.contract17 = Contract()
        self.contract17.symbol = 'UNH'
        self.contract17.secType = "STK"
        self.contract17.exchange = "SMART"
        self.contract17.currency = "USD"

        self.contract18 = Contract()
        self.contract18.symbol = 'MA'
        self.contract18.secType = "STK"
        self.contract18.exchange = "SMART"
        self.contract18.currency = "USD"

        self.contract19 = Contract()
        self.contract19.symbol = 'PG'
        self.contract19.secType = "STK"
        self.contract19.exchange = "SMART"
        self.contract19.currency = "USD"

        self.ib.reqIds(-1)
        # Request Market Data
        #self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])
        self.ib.reqHistoricalData(self.reqId, self.contract1, "", "2 D", str(self.barsize)+mintext, "TRADES", 1, 1, True, [])
        self.ib.reqHistoricalData(self.reqId + 1, self.contract2, "", "2 D", str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 2, self.contract3,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 3, self.contract4,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 4, self.contract5,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 5, self.contract6,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 6, self.contract7,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 7, self.contract8,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 8, self.contract9,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 9, self.contract10,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 10, self.contract11,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 11, self.contract12,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 12, self.contract13,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 13, self.contract14,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 14, self.contract15,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 15, self.contract16,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 16, self.contract17,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 17, self.contract18,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])
        self.ib.reqHistoricalData(self.reqId + 18, self.contract19,"","2 D",str(self.barsize)+mintext,"TRADES",1,1,True,[])


    def InitialEntry(self, Initial_action, quantity):
        # Create Parent Order / Initial Entry
        parent = Order()
        parent.orderType = "MKT"
        parent.action = Initial_action
        parent.totalQuantity = quantity
        return parent

    #Listen to socket in seperate thread
    def run_loop(self):
        self.ib.run()

      #Pass realtime bar data back to our bot object
    def on_bar_update(self, reqId, bar, realtime):
        global orderId, entry_trade, position, close_bar, high_bar, low_bar, initial_pop
        #Historical Data to catch up

        if (realtime == False):

            if reqId == 1:
                self.bars = self.my_bars['AAPL']
                self.bars.append(bar)
                self.my_bars['AAPL'] = self.bars
            elif reqId == 2:
                self.bars = self.my_bars['MSFT']
                self.bars.append(bar)
                self.my_bars['MSFT'] = self.bars
            elif reqId == 3:
                self.bars = self.my_bars['HD']
                self.bars.append(bar)
                self.my_bars['HD'] = self.bars
            elif reqId == 4:
                self.bars = self.my_bars['GOOG']
                self.bars.append(bar)
                self.my_bars['GOOG'] = self.bars
            elif reqId == 5:
                self.bars = self.my_bars['AMZN']
                self.bars.append(bar)
                self.my_bars['AMZN'] = self.bars
            elif reqId == 6:
                self.bars = self.my_bars['FB']
                self.bars.append(bar)
                self.my_bars['FB'] = self.bars
            elif reqId == 7:
                self.bars = self.my_bars['TSLA']
                self.bars.append(bar)
                self.my_bars['TSLA'] = self.bars
            elif reqId == 8:
                self.bars = self.my_bars['DIS']
                self.bars.append(bar)
                self.my_bars['DIS'] = self.bars
            elif reqId == 9:
                self.bars = self.my_bars['BRK B']
                self.bars.append(bar)
                self.my_bars['BRK B'] = self.bars
            elif reqId == 10:
                self.bars = self.my_bars['TSM']
                self.bars.append(bar)
                self.my_bars['TSM'] = self.bars
            elif reqId == 11:
                self.bars = self.my_bars['NVDA']
                self.bars.append(bar)
                self.my_bars['NVDA'] = self.bars
            elif reqId == 12:
                self.bars = self.my_bars['V']
                self.bars.append(bar)
                self.my_bars['V'] = self.bars
            elif reqId == 13:
                self.bars = self.my_bars['BABA']
                self.bars.append(bar)
                self.my_bars['BABA'] = self.bars
            elif reqId == 14:
                self.bars = self.my_bars['JNJ']
                self.bars.append(bar)
                self.my_bars['JNJ'] = self.bars
            elif reqId == 15:
                self.bars = self.my_bars['JPM']
                self.bars.append(bar)
                self.my_bars['JPM'] = self.bars
            elif reqId == 16:
                self.bars = self.my_bars['WMT']
                self.bars.append(bar)
                self.my_bars['WMT'] = self.bars
            elif reqId == 17:
                self.bars = self.my_bars['UNH']
                self.bars.append(bar)
                self.my_bars['UNH'] = self.bars
            elif reqId == 18:
                self.bars = self.my_bars['MA']
                self.bars.append(bar)
                self.my_bars['MA'] = self.bars
            elif reqId == 19:
                self.bars = self.my_bars['PG']
                self.bars.append(bar)
                self.my_bars['PG'] = self.bars


        else:

            if reqId == 1:
                self.bars = self.my_bars['AAPL']
            elif reqId == 2:
                self.bars = self.my_bars['MSFT']
            elif reqId == 3:
                self.bars = self.my_bars['HD']
            elif reqId == 4:
                self.bars = self.my_bars['GOOG']
            elif reqId == 5:
                self.bars = self.my_bars['AMZN']
            elif reqId == 6:
                self.bars = self.my_bars['FB']
            elif reqId == 7:
                self.bars = self.my_bars['TSLA']
            elif reqId == 8:
                self.bars = self.my_bars['DIS']
            elif reqId == 9:
                self.bars = self.my_bars['BRK B']
            elif reqId == 10:
                self.bars = self.my_bars['TSM']
            elif reqId == 11:
                self.bars = self.my_bars['NVDA']
            elif reqId == 12:
                self.bars = self.my_bars['V']
            elif reqId == 13:
                self.bars = self.my_bars['BABA']
            elif reqId == 14:
                self.bars = self.my_bars['JNJ']
            elif reqId == 15:
                self.bars = self.my_bars['JPM']
            elif reqId == 16:
                self.bars = self.my_bars['WMT']
            elif reqId == 17:
                self.bars = self.my_bars['UNH']
            elif reqId == 18:
                self.bars = self.my_bars['MA']
            elif reqId == 19:
                self.bars = self.my_bars['PG']

            bartime = datetime.strptime(bar.date,"%Y%m%d %H:%M:%S").astimezone(pytz.timezone("America/New_York"))
            minutes_diff = (bartime-self.initialbartime).total_seconds() / 60.0



            self.currentBar.date = bartime
            if bar.close == 0.0:
                bar.close = close_bar[reqId]
                bar.high = high_bar[reqId]
                bar.low = low_bar[reqId]

            close_bar[reqId] = bar.close
            high_bar[reqId] = bar.high
            low_bar[reqId] = bar.low

            #On Bar Close


            if (minutes_diff > 0 and math.floor(minutes_diff) % self.barsize == 0):
                for no_stock in range(len(self.portfolio)):

                    reqId = no_stock + 1
                    # print(self.bars)
                    print("Stock reqId :", reqId)
                    print('Stock name:', stocks_reqIds[reqId])
                    # print(close_bar[reqId])

                    self.initialbartime = bartime
                    #Entry - If we have a higher high, a higher low and we cross the 10 SMA Buy
                    #1.) SMA




                    self.currentBar = Bar()
                    self.currentBar.close = close_bar[reqId]
                    self.currentBar.high = high_bar[reqId]
                    self.currentBar.low = low_bar[reqId]

                    if reqId == 1:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 2:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 3:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 4:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 5:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 6:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 7:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 8:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 9:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 10:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 11:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 12:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 13:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 14:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 15:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 16:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 17:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 18:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]
                    elif reqId == 19:
                        self.bars = self.my_bars[stocks_reqIds[reqId]]


                # create empty list to store data point of close bar point, low bar point and high bar point
                    close1, low1, high1 = [], [], []

                    # print(self.bars[-1:].close)
                    for i in self.bars:
                        close1.append(i.close)
                        high1.append(i.high)
                        low1.append(i.low)
                    if initial_pop[reqId] == 0:
                        print('active')
                        close1.pop(-1)
                        low1.pop(-1)
                        high1.pop(-1)
                        # initial_pop[reqId] = 1


                    close1.append(self.currentBar.close)
                    low1.append(self.currentBar.low)
                    high1.append(self.currentBar.high)


                    print('Stock: ', stocks_reqIds[reqId])
                    self.close_array = pd.Series(np.asarray(close1))


                    # SMA15
                    self.sma_15 = []
                    i = 0
                    while i < len(close1) - self.smaPeriod_15 + 1:
                        new_close = close1[i:i + self.smaPeriod_15]
                        close_average = sum(new_close) / self.smaPeriod_15
                        self.sma_15.append(close_average)
                        i += 1
                    last_SMA_15 = self.sma_15[len(self.sma_15) - 1]
                    print("SMA of 15 Days: " + str(last_SMA_15))

                    j = 0
                    self.sma_10 = []

                    while j < len(close1) - self.smaPeriod_10 + 1:
                        new_close_10 = close1[j:j + self.smaPeriod_10]
                        close_average_10 = sum(new_close_10) / self.smaPeriod_10
                        self.sma_10.append(close_average_10)
                        j += 1
                    last_SMA_10 = self.sma_10[len(self.sma_10) - 1]
                    print("SMA of 10 Days: " + str(last_SMA_10))


                    #2.) Calculate Higher Highs and Lows

                    lastLow = low1[-1]
                    secondLastLow = low1[-2]
                    lastHigh = high1[-1]
                    secondLastHigh = high1[-2]

                    print('comparing highs #####')
                    print('last low:', lastLow)
                    print('last high:', lastHigh)
                    print('second last LOW:', secondLastLow)
                    print('second last high:', secondLastHigh)

                    run_once = 0

                    my_quantity = 100

                    if reqId == 1:
                        contract = self.contract1
                    elif reqId == 2:
                        contract = self.contract2
                    elif reqId == 3:
                        contract = self.contract3
                    elif reqId == 4:
                        contract = self.contract4
                    elif reqId == 5:
                        contract = self.contract5
                    elif reqId == 6:
                        contract = self.contract6
                    elif reqId == 7:
                        contract = self.contract7
                    elif reqId == 8:
                        contract = self.contract8
                    elif reqId == 9:
                        contract = self.contract9
                    elif reqId == 10:
                        contract = self.contract10
                    elif reqId == 11:
                        contract = self.contract11
                    elif reqId == 12:
                        contract = self.contract12
                    elif reqId == 13:
                        contract = self.contract13
                    elif reqId == 14:
                        contract = self.contract14
                    elif reqId == 15:
                        contract = self.contract15
                    elif reqId == 16:
                        contract = self.contract16
                    elif reqId == 17:
                        contract = self.contract17
                    elif reqId == 18:
                        contract = self.contract18
                    elif reqId == 19:
                        contract = self.contract19



                    # Check Criteria
                    if (last_SMA_10 > last_SMA_15) and (position[stocks_reqIds[reqId]] != 1) and lastHigh > secondLastHigh:
                        # and currentHigh > lastHigh ):

                        if entry_trade[stocks_reqIds[reqId]] == 0:
                            Entry = self.InitialEntry("BUY", my_quantity/2)
                        elif entry_trade[stocks_reqIds[reqId]] == 1:
                            Entry = self.InitialEntry("BUY", my_quantity)

                        if Entry.action == 'BUY':
                            position[stocks_reqIds[reqId]] = 1
                        elif Entry.action == 'SELL':
                            position[stocks_reqIds[reqId]] = -1
                        #
                        self.ib.placeOrder(orderId, contract, Entry)
                        entry_trade[stocks_reqIds[reqId]] = 1
                        orderId += 1


                        # write_data(close1[-1], self.initialbartime, 'BUY')

                    elif (last_SMA_10 < last_SMA_15) and (position[stocks_reqIds[reqId]] != -1) and lastLow < secondLastLow :
                        if entry_trade[stocks_reqIds[reqId]] == 0:
                            Entry = self.InitialEntry("SELL", my_quantity/2)
                        elif entry_trade[stocks_reqIds[reqId]] == 1:
                            Entry = self.InitialEntry("SELL", my_quantity)

                        if Entry.action == 'BUY':
                            position[stocks_reqIds[reqId]] = 1
                        elif Entry.action == 'SELL':
                            position[stocks_reqIds[reqId]] = -1



                        # contract = Contract()
                        self.ib.placeOrder(orderId, contract, Entry)
                        entry_trade[stocks_reqIds[reqId]] = 1
                        orderId += 1


                    self.currentBar.close = bar.close
                    self.currentBar.close = close_bar[reqId]



                    if initial_pop[reqId] == 1:
                        self.bars.append(self.currentBar)

                    elif initial_pop[reqId] == 0:
                        initial_pop[reqId] = 1
                        self.bars[-1].close = close1[-1:][0]
                        self.bars[-1].low = low1[-1:][0]
                        self.bars[-1].high = high1[-1:][0]


                    if reqId == 1:
                        self.my_bars['AAPL'] = self.bars
                    elif reqId == 2:
                        self.my_bars['MSFT'] = self.bars
                    elif reqId == 3:
                        self.my_bars['HD'] = self.bars
                    elif reqId == 4:
                        self.my_bars['GOOG'] = self.bars
                    elif reqId == 5:
                        self.my_bars['AMZN'] = self.bars
                    elif reqId == 6:
                        self.my_bars['FB'] = self.bars
                    elif reqId == 7:
                        self.my_bars['TSLA'] = self.bars
                    elif reqId == 8:
                        self.my_bars['DIS'] = self.bars
                    elif reqId == 9:
                        self.my_bars['BRK B'] = self.bars
                    elif reqId == 10:
                        self.my_bars['TSM'] = self.bars
                    elif reqId == 11:
                        self.my_bars['NVDA'] = self.bars
                    elif reqId == 12:
                        self.my_bars['V'] = self.bars
                    elif reqId == 13:
                        self.my_bars['BABA'] = self.bars
                    elif reqId == 14:
                        self.my_bars['JNJ'] = self.bars
                    elif reqId == 15:
                        self.my_bars['JPM'] = self.bars
                    elif reqId == 16:
                        self.my_bars['WMT'] = self.bars
                    elif reqId == 17:
                        self.my_bars['UNH'] = self.bars
                    elif reqId == 18:
                        self.my_bars['MA'] = self.bars
                    elif reqId == 19:
                        self.my_bars['PG'] = self.bars


#Start Bot
bot = Bot()

