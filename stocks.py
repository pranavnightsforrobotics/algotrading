'''
    Pranav Neti
    6/8/2023
    This is the simulator where I can run through historic stock data and apply my trading strategies to test their effectiveness
'''

import numpy as np
import backtrader as bt
import datetime
from strategies import *

#Default Cerebro Size
#cerebro.addsizer(bt.sizers.SizerFix, stake=100)

if __name__ == '__main__':
    #Initialize Cerebro and set base cash to 100,000
    cerebro = bt.Cerebro()
    
    # Add a strategy
    #cerebro.addstrategy(RSI, maperiod = 15)

    # Simple CrossOver optimization
    """strats = cerebro.optstrategy(
        CrossOver,
        maperiod = range(5, 50, 1))"""

    # Simple BollingerBands optimization
    """strats = cerebro.optstrategy(
        BollingerBandsPct,
        ActionStart = np.arange(0, 5, 0.1))"""

    # Advanced AverageTrueRange optimization
    """strats = cerebro.optstrategy(
        AverageTrueRange,
        AccVolit = np.arange(6, 8, 0.04))"""

    # Advanced AverageDirectionalMovementIndex optimization
    """strats = cerebro.optstrategy(
        AverageDirectionalMovementIndex,
        tradeStarter = range(10, 40, 1))"""

    # Basic AccelerationDecelerationOscillator optimizaion!
    """strats = cerebro.optstrategy(
        AccelerationDecelerationOscillator,
        startAction = np.arange(0, 5, 0.1))"""

    # Optomize a strategy with ceartin range for the indicators
    """strats = cerebro.optstrategy(
        SimpleMovingAverage,
        maperiod = range(5, 50, 1)
    )"""

    #Add data of Microsoft to Cerebro
    data = bt.feeds.YahooFinanceCSVData(dataname='MSFT.csv', 
                                        fromdate = datetime.datetime(2022, 6, 1),
                                        todate = datetime.datetime(2023, 6, 1),
                                        reverse = False)
    cerebro.adddata(data)


    # Set starting cash
    cerebro.broker.setcash(100000.0)

    # Adjust weight of each trade
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set commision
    cerebro.broker.setcommission(commission=0.001)

    # Run Cerebro Engine
    start_portfolio_value = cerebro.broker.getvalue()

    cerebro.run(maxcpus = 1)

    end_portfolio_value = cerebro.broker.getvalue()
    pnl = end_portfolio_value - start_portfolio_value
    print(f'Starting Portfolio Value: {start_portfolio_value:2f}')
    print(f'Final Portfolio Value: {end_portfolio_value:2f}')
    print(f'PnL: {pnl:.2f}')

    cerebro.plot()