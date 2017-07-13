import requests
from bs4 import BeautifulSoup
from pandas_datareader import data
import pandas as pd
from datetime import datetime, timedelta
import time

class Stock:
	DATA_SOURCE = 'google'

	# Initialize the instance variables in the class
	def __init__(self, ticker_symbol):
		self.ticker_symbol = ticker_symbol

	# If <include_lag_week> is true, get the percentage return of the stock between a week 
	# ago and <num_weeks> ago. Otherwise get the percentage return of the stock between  
	# yesterday and <num_weeks> ago.
	def get_percent_return(self, num_weeks, include_lag_week):
		# Incorporate either a lag day or a lag week into the dates we're using
		end_date = datetime.today()
		if include_lag_week:
			end_date -= timedelta(weeks=1)
		else:
			end_date -= timedelta(days=1)

		# Adjust date if it's on the weekend
		if end_date.weekday() == 6:
			end_date -= timedelta(days=2)
		elif end_date.weekday() == 5:
			end_date -= timedelta(days=1)

		# Create valid start and end dates
		start_date = end_date-timedelta(weeks=num_weeks)
		start_date = start_date.strftime("%Y-%m-%d")
		end_date = end_date.strftime("%Y-%m-%d")

		try:
			# Get the closing value of the stock on the start_date and the end_date
			start_date_data = data.DataReader(self.ticker_symbol, self.DATA_SOURCE, start_date, start_date)
			start_date_price = start_date_data['Close'][0]

			end_date_data = data.DataReader(self.ticker_symbol, self.DATA_SOURCE, end_date, end_date)
			end_date_price = end_date_data['Close'][0]

			# Calculate the percent difference between end_date closing price and start_date
			# closing price and return the value
			percent_return = (end_date_price-start_date_price)/start_date_price
			return percent_return
		except:
			return float("-inf")


# stock = Stock("amzn")
# t0 = time.time()
# print(stock.get_percent_return(39, 1))
# t1 = time.time()

# print(t1-t0)

# print(current_date)
# print(past_date)


# url = "https://www.sec.gov/Archives/edgar/data/1318605/000156459017009968/tsla-20170331.xml"
# r = requests.get(url)

# soup = BeautifulSoup(r.content, "lxml")
# tag = soup.period
# tag.name = "us-gaap:GrossProfit"
# print(tag)

