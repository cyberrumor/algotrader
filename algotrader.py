#!/usr/bin/python3
import numpy as np
import yfinance
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
import sys

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

def psar(x, iaf = 0.02, maxaf = 0.2):
	psar = list(x)
	psarbull = [None] * len(x)
	psarbear = [None] * len(x)
	bull = True
	af = iaf
	ep = hp = lp = x[0]
	for i in range(2, len(x)):
		if bull:
			psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
		else:
			psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
		reverse = False

		# this if/else triggers the actual stop and reverse, resetting af on the way
		if bull:
			if x[i] < psar[i]:
				bull = False
				reverse = True
				psar[i] = hp
				lp = x[i]
				af = iaf
		else:
			if x[i] > psar[i]:
				bull = True
				reverse = True
				psar[i] = lp
				hp = x[i]
				af = iaf
		# do this if we didn't just switch directions above
		if not reverse:
			if bull:
				# if we have a new highest high point, increase ratio
				if x[i] > hp:
					hp = x[i]
					af = min(af + iaf, maxaf)
				# set psar to lowest value between today and yesterday
				if x[i - 1] < psar[i]:
					psar[i] = x[i - 1]

				if x[i - 2] < psar[i]:
					psar[i] = x[i - 2]
			else:
				# if we have a new lowest low, increase ratio
				if x[i] < lp:
					lp = x[i]
					af = min(af + iaf, maxaf)
				# set psar to highest value between today and yesterday
				if x[i - 1] > psar[i]:
					psar[i] = x[i - 1]
				if x[i - 2] > psar[i]:
					psar[i] = x[i - 2]

		if bull:
			psarbull[i] = psar[i]
		else:
			psarbear[i] = psar[i]

	return {"psar":psar, "psarbear":psarbear, "psarbull":psarbull}

# list sums. NaN isn't graphed by matplotlib, this hides graphs using bad sums. expects lists.
def addlist(x, y):
	if len(x) != len(y):
		return [NaN]
	else:
		return [x[i] + y[i] for i in range(0, len(x))]
def sublist(x, y):
	if len(x) != len(y):
		return [NaN]
	else:
		return [x[i] - y[i] for i in range(0, len(x))]

def collector(stock, y):
	x = yfinance.Ticker(stock).history(period=longtime)['Close']

	std2 = addlist(movingstd(x, y), movingstd(x, y))
	upline = addlist(movingmean(x, y), std2)
	dnline = sublist(movingmean(x, y), std2)
	psardata = psar(x)
	H, c, data = compute_Hc(x, kind='price', simplified=True)
	printableH = str(H)
	print("Hurst of " + stock + " = " + printableH)

	return {'upline': upline, 'dnline': dnline, 'close': x, 'index': x.index, 'psarbear':psardata['psarbear'], 'psarbull': psardata['psarbull']}

def plotter(plotobject, data, stock):
	plotobject.plot(data['index'], data['close'], label=stock, color='black')
	plotobject.plot(data['index'], data['upline'], label='bollinger', color='gray')
	plotobject.plot(data['index'], data['dnline'], label='', color='gray')
	plotobject.plot(data['index'], data['psarbear'], label='psarbear', color='green')
	plotobject.plot(data['index'], data['psarbull'], label='psarbull', color='red')
	plotobject.legend()
	plotobject.grid(True)

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

