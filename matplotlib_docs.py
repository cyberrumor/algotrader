#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import statistics
import pandas


# set variable for the yahoo finance stock data object
amd = yf.Ticker("AMD")

# get historical market data
hist = amd.history(period="50d")

print(type(hist['Close'].values))
print(hist['Close'].values)


# the yahoo finance data gives us access to the following data:
# Date, Open, High, Low, Close, Adj Close, Volume
hist['Close'].plot(label='AMD', color='red')

# you can assign labels like so:
plt.xlabel('date')
plt.ylabel('value')
plt.title('Simple Plot')

# show the legend
plt.legend()

# show grid
plt.grid(True)

# this will draw the plot once ready
plt.show()
