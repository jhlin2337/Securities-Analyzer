nasdaq_listed_file = open('nasdaqlisted.txt', 'r')
nasdaq_stocks = open('nasdaqstocks.txt', 'w')

for line in nasdaq_listed_file:
	index = line.index('|')
	nasdaq_stocks.write(line[:index] + "\n")


other_listed_file = open('otherlisted.txt', 'r')
other_stocks = open('otherstocks.txt', 'w')

for line in other_listed_file:
	index = line.index('|')
	other_stocks.write(line[:index] + "\n")