#!/usr/bin/python3

def mean_reversion(stock, data, alpha):
	capital = alpha
	holding = False
	prices = data[stock]
	buy = []
	sell = []
	day = 0
	for price in prices:
		# define all sell signal conditions.
		if holding:
			if price > data['bollingerhigh'][day]:
				buy.append(None)
				sell.append(price)
				capital += price
				holding = False
			# hold
			else:
				buy.append(None)
				sell.append(None)

		# define all buy signal conditions and check affordability.
		else:
			if price < data['bollingerlow'][day] and price < capital:
				buy.append(price)
				sell.append(None)
				capital -= price
				holding = True
			# hold
			else:
				buy.append(None)
				sell.append(None)
		day += 1

	return {'capital': capital, 'buy': buy, 'sell': sell, 'holding': holding}

def momentum(stock, data, alpha):
	capital = alpha
	holding = False
	prices = data[stock]
	buy = []
	sell = []
	day = 0
	for price in prices:
		# define all sell signal conditions.
		if holding:
			if data['psarbear'][day]:
				buy.append(None)
				print('selling at:', price)
				sell.append(price)
				capital += price
				holding = False
			# hold
			else:
				buy.append(None)
				sell.append(None)

		# define all buy signal conditions and check affordability.
		else:
			if data['psarbull'][day] and price < capital:
				print('buying at', price)
				buy.append(price)
				sell.append(None)
				capital -= price
				holding = True
			# hold
			else:
				buy.append(None)
				sell.append(None)

		day += 1

	return {'capital': capital, 'buy': buy, 'sell': sell, 'holding': holding}

