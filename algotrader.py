#!/usr/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas

amd = yf.Ticker("AMD")
hist = amd.history(period="365d")
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
			# result.append('{:0.2f}'.format(x[i] + y[i]))
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
			# result.append('{:0.2f}'.format(x[i] - y[i]))
			result.append(x[i] - y[i])
		else:
			result.append(0)
		i += 1
	return result

movingstdbaselong = movingstd(somenumbers, 200)
print(movingstdbaselong)

movingstdbaseshort = movingstd(somenumbers, 50)
print(movingstdbaseshort)

movingstdlonghi = pandas.Series(addlist(somenumbers, movingstdbaselong))
print(movingstdlonghi.values)

movingstdlonglo = pandas.Series(sublist(somenumbers, movingstdbaselong))
print(movingstdlonglo.values)

movingstdshorthi = pandas.Series(addlist(somenumbers, movingstdbaseshort))
print(movingstdshorthi.values)

movingstdshortlo = pandas.Series(sublist(somenumbers, movingstdbaseshort))
print(movingstdshortlo.values)

movingmeanlong = pandas.Series(movingmean(somenumbers, 200))
print(movingmeanlong.values)

movingmeanshort = pandas.Series(movingmean(somenumbers, 50))
print(movingmeanshort.values)



hist.insert(loc=0, column='STDLongHi', value=movingstdlonghi.values)
hist.insert(loc=0, column='STDLongLo', value=movingstdlonglo.values)
hist.insert(loc=0, column='STDShortHi', value=movingstdshorthi.values)
hist.insert(loc=0, column='STDShortLo', value=movingstdshortlo.values)
hist.insert(loc=0, column='ShortMean', value=movingmeanshort.values)
hist.insert(loc=0, column='LongMean', value=movingmeanlong.values)





# draw the plots
# AMD close prices
hist['Close'].plot(label='AMD', color='black')
plt.xlabel('date')
plt.ylabel('price')
plt.title('AMD stock data')

hist['STDLongHi'].plot(label='STDLongHi', color='red')
hist['STDLongLo'].plot(label='STDLongLo', color='red')
hist['STDShortHi'].plot(label='STDShortHi', color='green')
hist['STDShortLo'].plot(label='STDShortLo', color='green')
hist['ShortMean'].plot(label='ShortMean', color='blue')
hist['LongMean'].plot(label='LongMean', color='blue')


print(hist)


# show the legend
plt.legend()

# show grid
plt.grid(True)

# this will draw the plot
plt.show()

