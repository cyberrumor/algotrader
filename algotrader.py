#!/usr/bin/python3
import numpy as np
import yfinance
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
import sys
import psar

shorttime = 20
longtime = '3y'

def movingstd(x, y):
	return [0] * y + [np.std(x[e:y + e]) for e in range(0, len(x) - y)]

def movingmean(x, y):
	return [0] * y + [np.mean(x[e:y + e]) for e in range(0, len(x) - y)]

def addlist(x, y):
	return [x[i] + y[i] for i in range(0, len(x))]

def sublist(x, y):
	return [x[i] - y[i] for i in range(0, len(x))]

def collector(stock, z):
	y = yfinance.Ticker(stock).history(period=longtime)['Close']
	std2 = addlist(movingstd(y, z), movingstd(y, z))
	mean = movingmean(y, z)
	bollingerhigh = addlist(mean, std2)
	bollingerlow = sublist(mean, std2)
	psardata = psar.getpsar(y)
	return {stock: y,
		'bollingerhigh': bollingerhigh,
		'bollingerlow': bollingerlow,
		'psarbear': psardata['psarbear'],
		'psarbull': psardata['psarbull']
		}

def plotter(plotobject, data, stock):
	fig.set_tight_layout(True)
	x = data[stock].index
	colors = ['red', 'grey', 'grey', 'black', 'black']
	for y, c in zip(data, colors):
		plotobject.plot(x, data[y], label=str(y), color=c)
	plotobject.legend()
	plotobject.grid(True)

if __name__ == '__main__':
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
