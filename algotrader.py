#!/usr/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas

# Set size for averages
scope = 20

amd = yf.Ticker("AMD")
hist = amd.history(period="730d")
somenumbers = hist['Close'].values

# mean formula, so we don't need to import numpy
def mean(x):
	return sum(x) / len(x)

# moving mean, x is list, y chunk size
def movingmean(x, y):
	return [0] * y + [mean(x[e:y + e]) for e in range(0, len(x) - y)]

# standard deviation, x is list
def std(x):
	return (sum([(i - sum(x) / len(x)) ** 2 for i in x]) / len(x)) ** 0.5

# moving standard deviation, x is list, y is chunk size
def movingstd(x, y):
	return [0] * y + [std(x[e:y + e]) for e in range(0, len(x) - y)]

# list sums. NaN isn't graphed by matplotlib, this hides graphs using bad sums.
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

# this is necessary because max() does not handle empty lists the way we want.
def biggest(list):
	if list == []:
		return 0
	if list != []:
		return max(list)

# followerstoplossA, current price - (standard deviation * risk). Only moves up.
def followerstoplossA(x, y, risk):
	result = []
	e = movingstd(x, y)
	i = 0
	while i < len(x):
		if x[i] - (e[i] * risk) > biggest(result):
			result.append(x[i] - (e[i] * risk))
		else:
			result.append(biggest(result))
		i += 1
	return result

# https://en.wikipedia.org/wiki/Parabolic_SAR
def sar(x, y):
	result = [0]
	# ep is extreme point, record kept of largest or smallest values
	ep = 1
	# maximum value of a should be capped at 0.20
	a = 0.01
	for value in x:
		result.append(result[-1] + a * (ep - result[-1]))
		if result[-1] >= ep:
			ep = result[-1]
			print("ep:")
			print(ep)
	result.pop(0)
	return result

movingstdbaseshort = movingstd(somenumbers, scope)
twostandarddeviation = addlist(movingstdbaseshort, movingstdbaseshort)
movingmeanshort = movingmean(somenumbers, scope)

# set up some charts
bollingerhigh = pandas.Series(addlist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerhigh', value=bollingerhigh.values)
hist['bollingerhigh'].plot(label='bollingerhigh', color='green')

bollingerlow = pandas.Series(sublist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerlow', value=bollingerlow.values)
hist['bollingerlow'].plot(label='bollingerlow', color='green')

stoploss = pandas.Series(followerstoplossA(somenumbers, 20, 1))
hist.insert(loc=0, column='stoploss', value=stoploss.values)
hist['stoploss'].plot(label='stoploss', color='blue')

#stoploss = pandas.Series(sar(somenumbers, 20))
#print()
#print(len(stoploss))
#print()
#hist.insert(loc=0, column='stoploss', value=stoploss.values)
#hist['stoploss'].plot(label='stoploss', color='blue')


hist['Close'].plot(label='AMD', color='black')


if __name__ == "__main__":
	# set up some labels
	plt.xlabel('date')
	plt.ylabel('price')
	plt.title('AMD stock data')

	# show the legend
	plt.legend()

	# show grid
	plt.grid(True)

	# this will draw the plot
	plt.show()
