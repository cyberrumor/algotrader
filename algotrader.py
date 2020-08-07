#!/usr/bin/python3

# the data source
import yfinance as yf
# the plotter
import matplotlib.pyplot as plt
# convert list to plottable array
import pandas

# Set size for averages
scope = 20

# pick a stock
amd = yf.Ticker("AMD")
hist = amd.history(period="730d")
somenumbers = hist['Close'].values

# mean formula, x is list
def mean(x):
	return sum(x) / len(x)

# moving mean y is chunk size
def movingmean(x, y):
	return [0] * y + [mean(x[e:y + e]) for e in range(0, len(x) - y)]

# standard deviation, x is list
def std(x):
	return (sum([(i - sum(x) / len(x)) ** 2 for i in x]) / len(x)) ** 0.5

# moving standard deviation, y is chunk size
def movingstd(x, y):
	return [0] * y + [std(x[e:y + e]) for e in range(0, len(x) - y)]

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

# this is necessary because max() does not handle empty lists the way we want.
def biggest(x):
	if x == []:
		return 0
	if x != []:
		return max(x)

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

# crunch
movingstdbaseshort = movingstd(somenumbers, scope)
twostandarddeviation = addlist(movingstdbaseshort, movingstdbaseshort)
movingmeanshort = movingmean(somenumbers, scope)

# bollinger high
bollingerhigh = pandas.Series(addlist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerhigh', value=bollingerhigh.values)
hist['bollingerhigh'].plot(label='bollingerhigh', color='green')
# bollinger low
bollingerlow = pandas.Series(sublist(movingmeanshort, twostandarddeviation))
hist.insert(loc=0, column='bollingerlow', value=bollingerlow.values)
hist['bollingerlow'].plot(label='bollingerlow', color='green')

# stoploss
stoploss = pandas.Series(followerstoplossA(somenumbers, scope, 1))
hist.insert(loc=0, column='stoploss', value=stoploss.values)
hist['stoploss'].plot(label='stoploss', color='blue')

# base price
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
