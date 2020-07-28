#!/usr/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas

amd = yf.Ticker("AMD")
hist = amd.history(period="730d")
print(type(hist))
somenumbers = hist['Close'].values

# square root formula, so we don't need to import math
def sqrt(x):
	if x < 0:
		return
	else:
		return x ** 0.5

# mean formula, so we don't need to import numpy
def mean(x):
	u = 0
	for i in x:
		u += i
	return u / len(x)

# standard deviation formula, so we don't have to import numpy
def std(x):
	u = 0
	n = 0
	z = 0
	for i in x:
		u += i
	u = u / len(x)
	for i in x:
		i = (i - u) ** 2
		z += i
	return sqrt(z / len(x))

# moving mean, x is the list, y is the number of data points at a time
def movingmean(x, y):
	e = 0
	i = 0
	result = []
	while i < y:
		result.append(0)
		i += 1
	for i in x[0 + e:y + e]:
		while e + y < len(x):
			# result.append('{:0.2f}'.format(mean(x[0 + e:y + e])))
			result.append(mean(x[0 + e:y + e]))
			e += 1
	return result


def biggest(list):
	if list == []:
		return 0
	if list != []:
		return max(list)


# follower stop loss, sell on cross from above
def followerstoploss(x, y, risk):
	result = []
	i = 0
	z = movingstd(x, y)
	while i < len(x):
		if type(x[i]) and type(z[i]) != str:
			if x[i] - (z[i] * risk) > biggest(result):
				result.append(x[i] - (z[i] * risk))
			else:
				result.append(biggest(result))
		else:
			result.append(0)
		i += 1
	return result

# moving standard deviation, x is the list, y is the number of data points at a time
def movingstd(x, y):
	e = 0
	i = 0
	result = []
	while i < y:
		result.append(0)
		i += 1

	for i in x[0 + e:y + e]:
		while e + y < len(x):
			result.append(std(x[0 + e:y + e]))
			e += 1
	return result

# add list, can handle retain nan
def addlist(x, y):
	result = []
	i = 0
	while i < len(x):
		if type(x[i]) and type(y[i]) != str:
			result.append(x[i] + y[i])
		else:
			result.append(0)
		i += 1
	return result

# subtract list, can retain nan
def sublist(x, y):
	result = []
	i = 0
	while i < len(x):
		if type(x[i]) and type(y[i]) != str:
			result.append(x[i] - y[i])
		else:
			result.append(0)
		i += 1
	return result

movingstdbaseshort = movingstd(somenumbers, 20)
twostandarddeviation = addlist(movingstdbaseshort, movingstdbaseshort)
movingmeanshort = movingmean(somenumbers, 20)

# set up some charts
bollingerhigh = pandas.Series(addlist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerhigh', value=bollingerhigh.values)
hist['bollingerhigh'].plot(label='bollingerhigh', color='green')

bollingerlow = pandas.Series(sublist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerlow', value=bollingerlow.values)
hist['bollingerlow'].plot(label='bollingerlow', color='green')

stoploss = pandas.Series(followerstoploss(somenumbers, 20, 1))
hist.insert(loc=0, column='stoploss', value=stoploss.values)
hist['stoploss'].plot(label='stoploss', color='blue')

hist['Close'].plot(label='AMD', color='black')

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

