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

# square root formula, so we don't need to import math
def sqrt(x):
	if x < 0:
		return
	else:
		return x ** 0.5

# mean formula, so we don't need to import numpy
def mean(x):
	e = 0
	for i in x:
		e += i
	return e / len(x)

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
	result = []
	i = 0
	e = 0
	while i < y:
		result.append(0)
		i += 1
	for i in x[0 + e:y + e]:
		while e + y < len(x):
			result.append(mean(x[0 + e:y + e]))
			e += 1
	return result

# return the biggest value from a list
def biggest(list):
	if list == []:
		return 0
	if list != []:
		return max(list)

# followerstoplossA, current price - (standard deviation * risk). Only moves up.
# consider using https://en.wikipedia.org/wiki/Parabolic_SAR instead
def followerstoplossA(x, y, risk):
	result = []
	i = 0
	e = movingstd(x, y)
	while i < len(x):
		if type(x[i]) and type(e[i]) != str:
			if x[i] - (e[i] * risk) > biggest(result):
				result.append(x[i] - (e[i] * risk))
			else:
				result.append(biggest(result))
		else:
			result.append(0)
		i += 1
	return result

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
	return result


# moving standard deviation, x is the list, y is the number of data points at a time
def movingstd(x, y):
	result = []
	i = 0
	e = 0
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

sar(somenumbers, 20)


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

