nasdaq_listed_file = open('./Stocks_List/Listed_Files/nasdaqlisted.txt', 'r')
nasdaq_stocks = open('./Stocks_List/nasdaqstocks.txt', 'w')

for line in nasdaq_listed_file:
	index = line.index('|')
	nasdaq_stocks.write(line[:index] + "\n")


other_listed_file = open('./Stocks_List/Listed_Files/otherlisted.txt', 'r')
other_stocks = open('./Stocks_List/otherstocks.txt', 'w')

for line in other_listed_file:
	index = line.index('|')
	other_stocks.write(line[:index] + "\n")