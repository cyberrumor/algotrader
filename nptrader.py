#!/usr/bin/python3

import numpy as np
import yfinance
import matplotlib.pyplot as plt
import sys

shorttime = 20
longtime = '3y'


if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Usage: ./algotrader amd aapl msft nvda')
		exit()

	fig, axes = plt.subplots(len(sys.argv[1:]), 1, figsize=(10, 4), sharex='col')

	for stock in sys.argv[1:]:
		print('plotting ' + stock)

		# select the subplot(columns, rows, index of selected plot).
		plt.subplot(len(sys.argv[1:]), 1, sys.argv.index(stock))

		plt.title(stock)

		# Get the data
		data = yfinance.Ticker(stock).history(period=longtime)['Close']
		x = data.index
		y = data.values
		plt.plot(x, y, color='black', label=stock)
		plt.legend()
		plt.grid(True)

	plt.show()
