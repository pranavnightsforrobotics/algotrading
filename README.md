# Algorithimic Trading

## Table of contents
1. [Inspiration](#Inspiration)
2. [Strategies](#Strategies)
    1. [SimpleMovingAverage](#SimpleMovingAverage)
    2. [AccelerationDecelerationOscillator](#AcclerationDecelerationOscillator)
    3. [AverageDirectionalMovementIndex](#AverageDirectionalMovementIndex)
    4. [AverageTrueRange](#AverageTrueRange)
    5. [BollingerBandsPct](#BollingerBandsPct)
    6. [CrossOver](#CrossOver)
    7. [RSI](#RSI)
3. [Results](#Results)

## Inspiration
This was my second-semester project for my advanced topics and projects class. This project was inspired by trading bots and the numerous indicators that exist within the stock market.

There are thousands if indicators in the trading world and it is often very confusing to find out which one is the best. To test these indicators and find the best one I decided to do some backtesting. Backtesting is where you do trading using historic data and see the results in an offline market. To do this I used the BackTrader library since it had incredible documentation, and was basically a finished product.

Here are the indicators I used
1. SimpleMovingAverage
2. AccelerationDecelerationOscillator
3. AverageDirectionalMovementIndex
4. AverageTrueRange
5. BollingerBandsPct
6. CrossOver
7. RSI

## Strategies
### SimpleMovingAverage
A SMA(SimpleMovingAverage) is a simple indicator which trades based on the average of a bunch of previous stocks. It assumes that a stock will alwalys return to its average, this average has differnet time frames based on how volatile the stock is. If the stock is lower than the average then you buy and if its greater then you sell.

### AccelerationDecelerationOscillator
An ADO(AcclerationDecelerationOscillator) is a predictive indicator since it tries to notice a falling, or rising stock using its accleration in a similar manner to physics. When it notices that the stock is not rising as fast as it was before then there is a negative accleration, and you can buy the stock, when it is rising faster than before then you can sell the stock.

### AverageDirectionalMovementIndex
An ADX(Average Directional Movement Index) is a lagging strength indicator, meaning that a trend must already be established and it will help predict the strength of the trend. Buy's if the stock has significant strength and the Weighted moving average is greater than a simple moving average (since the WMA signifies current rises and falls better than the SMA).

### AverageTrueRange
An ATR(AverageTrueRange) is a The ATR is a volatility indicator, meaning it does not predict what the future of the stock will be but rather describes the volatility of the stock currently, volatility is the ease at which a stock price can experience change. We use a similar strategy to the last one to trade, but buys if volatility is low, and profit for current stock is existent, and sells if volatility is high or the current stock is losing value.

### BollingerBandsPct
The Bollinger Band is a multifaceted indicator in that it can be used to make decisions on buying, but can also be used to find volatility. The Band makes a 3 line diagram on every stock plot, one upper, one lower, and one middle, buys were conducted when the closing price of the stocks hit the lower line, and sells were conducted when the closing price hit the middle line.

### CrossOver
The crossover indicator is similar to a strategy that I unknowingly used before, when I compared a weighted MA and a simple MA. Essentially the crossover just finds when one indicator is greater than the other. A buy is called when the weighted MA is greater than the MA, and the opposite for sells.

### RSI
The RSI is classified as a momentum oscillator, measuring the velocity and magnitude of price movements. Momentum is the rate of the rise or fall in price. If the momentum of the price is rising and the recent stock is rising then buys were conducted, if the momentum of the price is falling or the recenet stock is falling then sells were conducted.

## Results
