import yfinance as yf
import yfinance.data as da
import matplotlib.pyplot as plt
import pandas as pd
import backtrader as bt
import datetime
from strategies import *

#Default Cerebro Size
#cerebro.addsizer(bt.sizers.SizerFix, stake=100)

if __name__ == '__main__':
    #Initialize Cerebro and set base cash to 100,000
    cerebro = bt.Cerebro()
    
    # Add a strategy
    cerebro.addstrategy(Fall3Times)

    #Add data of Microsoft to Cerebro
    data = bt.feeds.YahooFinanceCSVData(dataname='MSFT.csv', 
                                        fromdate = datetime.datetime(2022, 6, 1),
                                        todate = datetime.datetime(2023, 6, 1),
                                        reverse = False)
    cerebro.adddata(data)


    # Set starting cash
    cerebro.broker.setcash(100000.0)


    # Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run()

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    cerebro.plot()