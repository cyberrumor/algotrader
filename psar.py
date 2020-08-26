#!/usr/bin/python3

# https://virtualizedfrog.wordpress.com/2014/12/09/parabolic-sar-implementation-in-python/

def getpsar(x, iaf = 0.02, maxaf = 0.2):
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

	return {'psar':psar,
		'psarbear':psarbear,
		'psarbull':psarbull
		}
