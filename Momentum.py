from Stock import Stock
import operator
import time

class Momentum:

	LOOKBACK_PERIOD = 39
	INCLUDE_LAG_WEEK = True

	# Returns an array of tuples containing the top decile of momentum stocks
	def get_momentum_stocks(self):
		stocks_list = {}

		f = open('./Securities_List/nasdaqstocks.txt', 'r')
		for symbol in f:
			print(symbol)
			stock = Stock(symbol)
			percent_return = stock.get_percent_return(self.LOOKBACK_PERIOD, self.INCLUDE_LAG_WEEK)
			stocks_list[symbol] = percent_return

		sorted_stocks = sorted(stocks_list.items(), key=operator.itemgetter(1), reverse=True)
		top_decile_index = len(sorted_stocks)//10

		return sorted_stocks[:top_decile_index]


t0 = time.time()
momentum = Momentum()
print(momentum.get_momentum_stocks())
t1 = time.time()
print(t1-t0)

# stock = Stock('AAPL')
# print(stock.get_percent_return(39, True))