import atFuncs
from tickers import tickers
from time import sleep

for ticker in tickers:
	try:
		atFuncs.fetchStock10(ticker)
		sleep(5)
	except Exception as e:
		print(e)
