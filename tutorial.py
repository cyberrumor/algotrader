#!/usr/bin/python3
# https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e
# import yahoo finance, pip module
import yfinance as yf
# import tkinter for the matplotlib visual backend, requires tk on Arch and python3-tkinter on Debian.
import tkinter
# import matplotlib for graph construction
import matplotlib

# set variable for the yahoo finance stock data object
msft = yf.Ticker("MSFT")

# get some stock info (takes several seconds to do this)
# print(msft.info)

# get historical market data
hist = msft.history(period="5d")

# history supports other methods as well, besides period:
# interval - data interval. If it?s intraday data, the interval needs to be set within 60 days
#	1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
# start - If period is not set- Download start date string (YYYY-MM-DD) or datetime
#	2020-03-18
# end - If period is not set - Download end date string (YYYY-MM-DD) or datetime
#	2020-03-19
# prepost -  Boolean value to include Pre and Post market data (default is False, can set to True)
# auto_adjust - Boolean value to adjust all OHLC (default is True)
# actions -  Boolean value download stock dividends and stock splits events (default is true)

# Plot data points of closing values from the history we imported earlier.
hist['Close'].plot(figsize=(16, 9))

# show the graph
matplotlib.pyplot.show()
