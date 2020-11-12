#!/usr/bin/python3
import numpy as np
import yfinance
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
import sys
import strategies
import psar

# starting funds = alpha
alpha = 50
shorttime = 20
longtime = '1y'

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


def print_stats(strategy, price):
	if strategy['holding']:
		print('liquid capital:', strategy['capital'])
		print('all assets:', strategy['capital'] + price)
	else:
		print('liquid capital:', strategy['capital'])
		print('all assets:', strategy['capital'])

def signals(stock, data):
	# current positions should go here and get fed to strategies.
	prices = data[stock]

	# mean reversion
	strat_mr = strategies.mean_reversion(stock, data, alpha)
	print()
	print('Mean Reversion on', stock + ':')
	print_stats(strat_mr, prices[-1])

	# momentum
	strat_mo = strategies.momentum(stock, data, alpha)
	print()
	print('Momentum on', stock + ':')
	print_stats(strat_mo, prices[-1])

	# buy and hold
	first_buy = 0
	for i in strat_mr['buy']:
		if i != None:
			first_buy = i
			break
	hodl = alpha - first_buy + prices[-1]
	print()
	if strat_mr['capital'] >= strat_mo['capital']:
		signals = {'buy': strat_mr['buy'], 'sell': strat_mr['sell']}
		if hodl >= strat_mr['capital']:
			print('recommending buy and hold:', hodl)


	elif strat_mo['capital'] > strat_mr['capital']:
		signals = {'buy': strat_mo['buy'], 'sell': strat_mo['sell']}
		if hodl >= strat_mo['capital']:
			print('recommending buy and hold:', hodl)
	# test momentum
	# signals = {'buy': strat_mo['buy'], 'sell': strat_mo['sell']}
	return signals

def plotter(plotobject, data, stock, exchanges):
	fig.set_tight_layout(True)
	x = data[stock].index
	colors = ['red', 'grey', 'grey', 'black', 'black']

	# price, indicators
	for y, c in zip(data, colors):
		plotobject.plot(x, data[y], label = str(y), color = c)

	# buys and sells
	plotobject.scatter(x, exchanges['buy'], c = 'g', s = 100, marker = '^', label = 'buy')
	plotobject.scatter(x, exchanges['sell'], c = 'b', s = 100, marker = 'v', label = 'sell')

	plotobject.legend()
	plotobject.grid(True)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('Usage: ./algotrader.py amd aapl msft nvda')
		exit()

	print('Starting with:', alpha)

	if len(sys.argv) == 2:
		stock = sys.argv[-1]
		fig = plt.figure()
		data = collector(stock, shorttime)
		exchanges = signals(stock, data)
		plotter(plt, data, stock, exchanges)
	else:
		fig, axs = plt.subplots(len(sys.argv[1:]), 1, figsize=(12,6), sharex='col')
		for ax, stock in zip(axs, sys.argv[1:]):
			data = collector(stock, shorttime)
			exchanges = signals(stock, data)
			plotter(ax, data, stock, exchanges)

	plt.show()
