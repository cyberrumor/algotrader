#!/usr/bin/python3
import math

# get some data, preferably from somewhere free like yahoo finance
# the below is the 50 day closing prices of AMD taken on July 25th

somenumbers = [54.51, 54.2,  54.59, 55.47, 56.39, 54.65, 55.17, 53.19, 52.74, 51.74, 53.8,  53.63,
 53.54, 52.73, 52.63, 53.1,  52.97, 56.39, 57.44, 52.83, 53.5,  54.68, 54.46, 54.55,
 54.04, 54.23, 54.76, 53.99, 52.39, 51.93, 50.1,  50.28, 52.61, 52.58, 52.34, 53.4,
 52.93, 53.43, 57.26, 55.88, 53.59, 54.72, 55.34, 54.92, 55.04, 57.46, 57.,   61.79,
 59.57, 69.4]

# mean formulat
def average(x):
	u = 0
	for i in x:
		u += i
	return u / len(x)

# standard deviation formula
def volatility(x):
	u = 0
	n = 0
	z = 0
	for i in x:
		u += i
	u = u / len(x)
	for i in x:
		i = (i - u) ** 2
		z += i
	return math.sqrt(z / len(x))

mean = average(somenumbers)
standard_deviation = volatility(somenumbers)
buy = mean - standard_deviation
sell = mean + standard_deviation

print()
print("data set:")
print(somenumbers)
print()
print("mean:")
print(mean)
print()
print("standard deviation:")
print(standard_deviation)
print()
print("buy below:")
print(buy)
print()
print("sell above:")
print(sell)
print()
