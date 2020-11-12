#!/usr/bin/python3
def mean_reversion(stock, data, alpha):
	# we should look into hurst exponent here
	capital = alpha
	holding = False
	prices = data[stock]
	buy = []
	sell = []
	# we should get this from currently held positions in broker api
	last_buy = 0
	day = 0
	for price in prices:
		# define all sell signal conditions.
		if holding:
			buy.append(None)
			if price > data['bollingerhigh'][day]:
				# don't sell if it's lower than purchase price
				if price < last_buy:
					sell.append(None)

				# profitable sale
				else:
					sell.append(price)
					capital += price
					holding = False
			# hold
			else:
				sell.append(None)

		# define all buy signal conditions and check affordability.
		else:
			sell.append(None)
			if price < data['bollingerlow'][day] and price < capital:
				buy.append(price)
				last_buy = price
				capital -= price
				holding = True
			# hold
			else:
				buy.append(None)
		day += 1

	return {'capital': capital, 'buy': buy, 'sell': sell, 'holding': holding}

def momentum(stock, data, alpha):
	capital = alpha
	holding = False
	prices = data[stock]
	buy = []
	sell = []
	# we should get this from currently held positions from broker api.
	last_buy = 0
	day = 0
	for price in prices:
		# define all sell signal conditions.
		if holding:
			buy.append(None)
			if data['psarbear'][day]:
				sell.append(price)
				capital += price
				holding = False
			# hold
			else:
				sell.append(None)

		# define all buy signal conditions.
		else:
			# can't sell what we don't have
			sell.append(None)

			# detect bull run
			if data['psarbull'][day] and price < capital:
				buy.append(price)
				last_buy = price
				capital -= price
				holding = True
			# hold
			else:
				buy.append(None)

		day += 1

	return {'capital': capital, 'buy': buy, 'sell': sell, 'holding': holding}

