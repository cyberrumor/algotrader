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

def collector(stock, y):
	x = yfinance.Ticker(stock).history(period=longtime)['Close']
	std2 = addlist(movingstd(x, y), movingstd(x, y))
	upline = addlist(movingmean(x, y), std2)
	dnline = sublist(movingmean(x, y), std2)
	return {'upline': upline, 'dnline': dnline, 'close': x, 'index': x.index}

def plotter(plot, data, stock):
	plot.plot(data['index'], data['close'], label=stock, color='black')
	plot.plot(data['index'], data['upline'], label='bollinger', color='gray')
	plot.plot(data['index'], data['dnline'], label='', color='gray')
	plot.legend()
	plot.grid(True)

if __name__ == '__main__':

	# show usage
	if len(sys.argv) == 1:
		print('Usage: ./algotrader.py amd aapl msft nvda')
		exit()

	if len(sys.argv) == 2:
		stock = sys.argv[-1]
		fig = plt.figure()
		data = collector(stock, shorttime)
		plotter(plt, data, stock)

	else:
		fig, axs = plt.subplots(len(sys.argv[1:]), 1, figsize=(12,6), sharex='col')
		for ax, stock in zip(axs, sys.argv[1:]):
			data = collector(stock, shorttime)
			plotter(ax, data, stock)


	plt.show()
