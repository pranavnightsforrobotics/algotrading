import backtrader as bt
import datetime

class MyStrategy(bt.Strategy):
    def next(self):
        pass #Do something

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

class Fall3Times(bt.Strategy):

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

        if(self.dataclose[0] < self.dataclose[-1]):
            if(self.dataclose[-1] < self.dataclose[-2]):
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.buy()



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
                        
                        