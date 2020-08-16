#!/usr/bin/python3

# the data source
import yfinance as yf
# the plotter
import matplotlib.pyplot as plt
# convert list to plottable array
import pandas
# for benchmarking
import time

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


# Hurst exponent


# Sharpe filter





# timer supervisor, run any function with "mytimer(): \n\t function()" to time it
class MyTimer():
	def __init__(self):
		self.start = time.time()
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		end = time.time()
		runtime = end - self.start
		msg = 'The function took {time} seconds to complete'
		print(msg.format(time=runtime))

if __name__ == "__main__":

	with MyTimer():

		# required by twostandardeviation
		movingstdbaseshort = movingstd(somenumbers, scope)
		# required by bollinger
		twostandarddeviation = addlist(movingstdbaseshort, movingstdbaseshort)
		# required by bollinger
		movingmeanshort = movingmean(somenumbers, scope)
		# required by psar{bear, bull, sar}
		sar = psar(somenumbers)

		# Convert the data into pandas.Series type for plotting.

		# bollinger high, requires twostandarddeviation and movingmeanshort
		bollingerhigh = pandas.Series(addlist(movingmeanshort, twostandarddeviation))
		# bollinger low, requires twostandarddeviation and movingmeanshort
		bollingerlow = pandas.Series(sublist(movingmeanshort, twostandarddeviation))

		# psar, requires sar
		# psarsar = pandas.Series(sar['psar'])
		psarbull = pandas.Series(sar['psarbull'])
		psarbear = pandas.Series(sar['psarbear'])

		# insert the data into the main dataframe.
		hist['Close'].plot(label='AMD', color='black')
		hist.insert(loc=0, column='bollingerhigh', value=bollingerhigh.values)
		hist['bollingerhigh'].plot(label='bollingerhigh', color='gray')
		hist.insert(loc=0, column='bollingerlow', value=bollingerlow.values)
		hist['bollingerlow'].plot(label='bollingerlow', color='gray')
		hist.insert(loc=0, column='psarbull', value=psarbull.values)
		hist['psarbull'].plot(label='psarbull', color='red')
		hist.insert(loc=0, column='psarbear', value=psarbear.values)
		hist['psarbear'].plot(label='psarbear', color='pink')
		# hist.insert(loc=0, column='psar', value=psarsar.values)
		# hist['psar'].plot(label='psar', color='blue')

		# set up some labels
		plt.xlabel('date')
		plt.ylabel('price')
		plt.title('AMD stock data')

		# show the legend
		plt.legend()

		# show grid
		plt.grid(True)

	# this will draw the plot, we don't want to benchmark how long you look at it, esc MyTimer.
	plt.show()
