#!/usr/bin/python3

import tkinter
import matplotlib
import numpy
import statistics


# some possibly useful built-in functions:
# abs() - absolute value
# filter() - Use a filter to exclude items in an iterable object
# min(), max() - returns smallest, largest items in an iterable
# sum() - sums the items of an iterator
# range() - returns a sequence of numbers, starting from 0 and increments by 1 (by default)

somenumbers = [1, 4, 9, 4, 7, 14, 12]

mean = statistics.mean(somenumbers)
standard_deviation = numpy.std(somenumbers)
buy = mean - standard_deviation
sell = mean + standard_deviation


print("mean: " + str(mean))
print("standard deviation: " + str(standard_deviation))
print("buy below: " + str(buy))
print("sell above: " + str(sell))


