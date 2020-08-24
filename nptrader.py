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

	fig, axs = plt.subplots(len(sys.argv[1:]), 1, figsize=(10,4), sharex='col')

	for ax, stock in zip(axs, sys.argv[1:]):
		ax.set_title(stock)
		data = yfinance.Ticker(stock).history(period=longtime)['Close']
		x = data.index
		y = data.values
		ax.plot(x, y, color='black', label=stock)
		ax.legend()
		ax.grid(True)

	plt.show()
