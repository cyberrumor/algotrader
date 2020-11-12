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
			# only one security at a time
			buy.append(None)
			# if all sell conditions are met, sell.
			if  all([
				price > last_buy,
				price > data['bollingerhigh'][day]
			]):
				sell.append(price)
				capital += price
				holding = False
				last_buy = 0

			# everything else is a hold
			else:
				sell.append(None)

		# define all buy signal conditions and check affordability.
		else:
			# can't sell what we don't have
			sell.append(None)

			# detect sale and trigger buy
			if all([
				price < data['bollingerlow'][day],
				price < capital
			]):
				buy.append(price)
				last_buy = price
				capital -= price
				holding = True

			# wait for better discount
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
			# only one security at a time
			buy.append(None)

			# sell if all criteria are met
			if all([
				data['psarbear'][day],
				price > last_buy
			]):
				# profitable sell
				sell.append(price)
				capital += price
				holding = False
				last_buy = 0

			# everything else is a hold
			else:
				sell.append(None)

		# define all buy signal conditions.
		else:
			# can't sell what we don't have
			sell.append(None)
			# find buy signal and check affordability.
			if all([
				data['psarbull'][day],
				price < capital
			]):
				buy.append(price)
				last_buy = price
				capital -= price
				holding = True

			# wait for a better discount
			else:
				buy.append(None)
		day += 1
	return {'capital': capital, 'buy': buy, 'sell': sell, 'holding': holding}

