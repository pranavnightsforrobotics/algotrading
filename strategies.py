import backtrader as bt
import datetime

class GraphingTestig(bt.Strategy):
    def log(self, printTxt, date=None):
        ''' Logging function for this strategy'''
        date = date or self.datas[0].datetime.date(0)
        print('%s, %s' % (date.isoformat(), printTxt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period = 50)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

class PrintClosing(bt.Strategy):

    def log(self, printTxt, date=None):
        ''' Logging function for this strategy'''
        date = date or self.datas[0].datetime.date(0)
        print('%s, %s' % (date.isoformat(), printTxt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

class Fall3TimesWait5(bt.Strategy):
    
    # Customazaiable paramteres to easy adjusting code
    params = (
        ('exitbars', 5),
    )

    # Prints entered data for logging purposes
    def log(self, printTxt, date=None):
        ''' Logging function for this strategy'''
        date = date or self.datas[0].datetime.date(0)
        print('%s, %s' % (date.isoformat(), printTxt))

    # Initialize all variables that will be used thorughout the strategy
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

    # Learn status of order
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)

            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        # If Sell / Buy cycle is not completed yet
        if not trade.isclosed:
            return
        
        #If it is log profit for that particular cycle, NET profit is after commission
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Avoid's sending 2 orders
        if self.order:
            self.log("IN ORDER")
            return

        # Currently not in market, enter by buying if condition is true
        if not self.position:
            if(self.dataclose[0] < self.dataclose[-1]):
                if(self.dataclose[-1] < self.dataclose[-2]):
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.order = self.buy()

        # If currently in market(Have stocks), and previous order was atleast 5 time frames ago then sell
        else:
            if len(self) >= (self.bar_executed + self.params.exitbars):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                self.order = self.sell()

class SimpleMovingAverage(bt.Strategy):
    
    # Customazaiable paramteres to easy adjusting code
    params = (
        ('maperiod', 15),
        ('printlog', False),
    )

    # Prints entered data for logging purposes
    def log(self, printTxt, date=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            date = date or self.datas[0].datetime.date(0)
            print('%s, %s' % (date.isoformat(), printTxt))

    # Initialize all variables that will be used thorughout the strategy
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAvergaeSimple Indicator
        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

    # Learn status of order
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED: %.2f, Cost: %.2f, Comm: %.2f' % 
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                
                # Price of all stocks bought in that order
                self.buyprice = order.executed.price

                # Price of commission paid in that order
                self.buycomm = order.executed.comm

            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        # If Sell / Buy cycle is not completed yet
        if not trade.isclosed:
            return
        
        #If it is log profit for that particular cycle, NET profit is after commission
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Avoid's sending 2 orders
        if self.order:
            self.log("IN ORDER")
            return

        # Currently not in market, enter by buying if condition is true
        if not self.position:
            if(self.dataclose[0] > self.sma[0]):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        # If currently in market(Have stocks), and and condition true then sell
        else:
            if (self.dataclose[0] < self.sma[0]):
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
    
    # End of a Cerebro Simulation
    def stop(self):
        self.log('(MA Period: %2d) Ending Value: %.2f' % 
                 (self.params.maperiod, self.broker.getvalue()), doprint = True)

class MAcrossover(bt.Strategy): 
    # Moving average parameters
    params = (('pfast',20),('pslow',50),)

    def log(self, txt, dt=None):
        dt = "Close: " + str(dt) + " Date: " + str(self.datas[0].datetime.date(0))
        print(dt) #Print date and close

    def __init__(self):
        self.dataclose = self.datas[0].close
        
		# Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pfast)
        
    def notify_order(self, order):
	    # Check if an order has been completed
	    # Attention: broker could reject order if not enough cash
        if(order.status is order.Completed):
            if(order.isbuy()):
                self.log(f'BUY EXCUTED, {order.excuted.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXCUTED, {order.excuted.price:.2f}')
            self.bar_executed = len(self)
        elif(order.status in [order.Canceled, order.Margin, order.Rejected]):
            self.log('Order Canceled/Margin/Rejected')
        elif(order.status in [order.Submitted, order.Accepted]):
            return
        self.order = None
    
    def next(self):
        if self.order:
            return
        
	    # Check for open orders
        if not self.position:
            self.position
		    # We are not in the market, look for a signal to OPEN trades
			
		    #If the 20 SMA is above the 50 SMA
            if self.fast_sma[0] > self.slow_sma[0] and self.fast_sma[-1] < self.slow_sma[-1]:
                self.log(f'BUY CREATE {self.dataclose[0]:2f}')
			    # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

		    #Otherwise if the 20 SMA is below the 50 SMA   
            elif self.fast_sma[0] < self.slow_sma[0] and self.fast_sma[-1] > self.slow_sma[-1]:
                self.log(f'SELL CREATE {self.dataclose[0]:2f}')
			    # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        else:
		    # We are already in the market, look for a signal to CLOSE trades
            if len(self) >= (self.bar_executed + 5):
                self.log(f'CLOSE CREATE {self.dataclose[0]:2f}')
                self.order = self.close()
                        
                        