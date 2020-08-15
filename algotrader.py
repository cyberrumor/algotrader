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

# close values psar
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

# this is necessary because max() does not handle empty lists the way we want.
def biggest(x):
	if x == []:
		return 0
	if x != []:
		return max(x)

# followerstoplossA, current price - (standard deviation * risk). Only moves up.
def resistanceA(x, y, risk):
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

if __name__ == "__main__":

	# crunch
	movingstdbaseshort = movingstd(somenumbers, scope)
	twostandarddeviation = addlist(movingstdbaseshort, movingstdbaseshort)
	movingmeanshort = movingmean(somenumbers, scope)

	# bollinger high
	bollingerhigh = pandas.Series(addlist(movingmeanshort, twostandarddeviation))
	hist.insert(loc=0, column='bollingerhigh', value=bollingerhigh.values)
	hist['bollingerhigh'].plot(label='bollingerhigh', color='gray')
	# bollinger low
	bollingerlow = pandas.Series(sublist(movingmeanshort, twostandarddeviation))
	hist.insert(loc=0, column='bollingerlow', value=bollingerlow.values)
	hist['bollingerlow'].plot(label='bollingerlow', color='gray')

	# resistance level
	# resistance = pandas.Series(resistanceA(somenumbers, scope, 1))
	# hist.insert(loc=0, column='resistance', value=resistance.values)
	# hist['resistance'].plot(label='resistance', color='blue')

	# parabolic stop and reverse
	sar = psar(somenumbers)

	# psarsar = pandas.Series(sar['psar'])
	# hist.insert(loc=0, column='psar', value=psarsar.values)
	# hist['psar'].plot(label='psar', color='blue')

	psarbull = pandas.Series(sar['psarbull'])
	hist.insert(loc=0, column='psarbull', value=psarbull.values)
	hist['psarbull'].plot(label='psarbull', color='red')

	psarbear = pandas.Series(sar['psarbear'])
	hist.insert(loc=0, column='psarbear', value=psarbear.values)
	hist['psarbear'].plot(label='psarbear', color='pink')

	# base price
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
