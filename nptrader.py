#!/usr/bin/python3

import numpy as np
import yfinance
import matplotlib.pyplot as plt
import sys
import time


shorttime = 20
longtime = '3y'


def movingstd(x, y):
	return [0] * y + [np.std(x[e:y + e]) for e in range(0, len(x) - y)]

def movingmean(x, y):
	return [0] * y + [np.mean(x[e:y + e]) for e in range(0, len(x) - y)]


def addlist(x, y):
	if len(x) != len(y):
		return np.NaN
	else:
		return [x[i] + y[i] for i in range(0, len(x))]

def sublist(x, y):
	if len(x) != len(y):
		return np.NaN
	else:
		return [x[i] - y[i] for i in range(0, len(x))]


def bollinger(x, y):
	std2 = addlist(movingstd(x, y), movingstd(x, y))
	upline = addlist(movingmean(x, y), std2)
	dnline = sublist(movingmean(x, y), std2)
	return {"upline":upline, "dnline":dnline}

def collector():
	pass

def plotter():
	pass

if __name__ == '__main__':

	# show usage
	if len(sys.argv) == 1:
		print('Usage: ./algotrader.py amd aapl msft nvda')
		exit()

	if len(sys.argv) == 2:
		stock = sys.argv[-1]

		# create the plot
		fig = plt.figure()

		# collect the data we want to plot
		data = yfinance.Ticker(stock).history(period=longtime)['Close']
		bollingerbands = bollinger(data, shorttime)

		# plot the data
		plt.plot(data.index, data.values, label=stock, color='black')
		plt.plot(data.index, bollingerbands["upline"], label='', color='gray')
		plt.plot(data.index, bollingerbands["dnline"], label='', color='gray')

		plt.grid(True)
		plt.legend()

	else:
		# create the plots
		fig, axs = plt.subplots(len(sys.argv[1:]), 1, figsize=(10,4), sharex='col')
		for ax, stock in zip(axs, sys.argv[1:]):
			ax.set_title(stock)

			# collect the data we want to plot
			data = yfinance.Ticker(stock).history(period=longtime)['Close']
			bollingerbands = bollinger(data, shorttime)

			# plot the data
			ax.plot(data.index, data.values, color='black', label=stock)
			ax.plot(data.index, bollingerbands["upline"], color='gray', label='')
			ax.plot(data.index, bollingerbands["dnline"], color='gray', label='')
			ax.legend()
			ax.grid(True)

	# draw plot
	plt.show()
