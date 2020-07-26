#!/usr/bin/python3

# for rounding correctly, this currently truncates instead of rounds
# from decimal import Decimal

somenumbers = [54.51, 54.2,  54.59, 55.47, 56.39, 54.65, 55.17, 53.19, 52.74, 51.74, 53.8,  53.63,
 53.54, 52.73, 52.63, 53.1,  52.97, 56.39, 57.44, 52.83, 53.5,  54.68, 54.46, 54.55,
 54.04, 54.23, 54.76, 53.99, 52.39, 51.93, 50.1,  50.28, 52.61, 52.58, 52.34, 53.4,
 52.93, 53.43, 57.26, 55.88, 53.59, 54.72, 55.34, 54.92, 55.04, 57.46, 57.,   61.79,
 59.57, 69.4]

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

listmovingstd = movingstd(somenumbers, 10)
movingstdhi = addlist(somenumbers, listmovingstd)
movingstdlo = sublist(somenumbers, listmovingstd)
listmovingmean = movingmean(somenumbers, 10)

print()
print('amd:')
print(somenumbers)
print()
print('mean:')
print(listmovingmean)
print()
print('high std dist:')
print(movingstdhi)
print()
print('low std dist:')
print(movingstdlo)
print()
