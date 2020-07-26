#!/usr/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

amd = yf.Ticker("AMD")
hist = amd.history(period="365d")
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
		result.append("nan")
		i += 1
	for i in x[0 + e:y + e]:
		while e + y < len(x):
			result.append('{:0.2f}'.format(mean(x[0 + e:y + e])))
			e += 1
	return result

# moving standard deviation, x is the list, y is the number of data points at a time
def movingstd(x, y):
	e = 0
	i = 0
	result = []
	while i < y:
		result.append("nan")
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
			result.append('{:0.2f}'.format(x[i] + y[i]))
		else:
			result.append("nan")
		i += 1
	return result

# subtract list, can retain nan
def sublist(x, y):
	result = []
	i = 0
	while i < len(x):
		if type(x[i]) and type(y[i]) != str:
			result.append('{:0.2f}'.format(x[i] - y[i]))
		else:
			result.append("nan")
		i += 1
	return result

listmovingstd = movingstd(somenumbers, 200)
movingstdhi = addlist(somenumbers, listmovingstd)
movingstdlo = sublist(somenumbers, listmovingstd)
listmovingmean = movingmean(somenumbers, 200)
shortmovingmean = movingmean(somenumbers, 50)
fiftydaymovingstd = movingstd(somenumbers, 50)
movingstdhishort = addlist(somenumbers, fiftydaymovingstd)
movingstdloshort = sublist(somenumbers, fiftydaymovingstd)



print()
print('amd:')
print(somenumbers)
print()
print('moving mean 200 day:')
print(listmovingmean)
print()
print('moving high std dist 200 day:')
print(movingstdhi)
print()
print('moving low std dist 200 day:')
print(movingstdlo)
print()
print('moving mean 50 day:')
print(shortmovingmean)
print()
print('moving high std dist 50 day:')
print(movingstdhishort)
print()
print('moving low std dist 50 day:')
print(movingstdloshort)


# here we need to push these values into the AMD panda series


# draw the plots

# AMD close prices
hist['Close'].plot(label='AMD', color='red')
plt.xlabel('date')
plt.ylabel('price')
plt.title('AMD stock data')

# here we need to draw the AMD moving means and std deviations
# requires moving the data into the series first
# https://pythonexamples.org/pandas-dataframe-add-column/

# show the legend
plt.legend()

# show grid
plt.grid(True)

# this will draw the plot
plt.show()

