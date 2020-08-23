#!/usr/bin/python3

import numpy as np
import yfinance as yf
import sys

scope = 20
timeframe = "3y"


if __name__ == "__main__":
	# show usage and quit if no args were fed
	if len(sys.argv) == 1:
		print("Usage: ./algotrader amd aapl msft nvda")
		exit()

	# pragmatically choose number of subplots
	# https://stackoverflow.com/questions/12319796/dynamically-add-create-subplots-in-matplotlib
	fig = plt.figure()

	for stock in sys.argv[1:]:
		prices = yf.Ticker(arg).history(period=timeframe)['Close'].values

