from Stock import Stock
import numpy as np
import json

def fill_dictionary(dictionary, data, sic_code):
	if sic_code in dictionary:
		dictionary[sic_code].append(data)
	else:
		dictionary[sic_code] = [data]

def fill_roa_dict(stock, sic_code):
	try:
		net_income = int(stock.get_net_income(0))
		total_assets = int(stock.get_total_assets(1))
		roa = net_income/total_assets
		fill_dictionary(return_on_assets, roa, sic_code)
	except Exception as e:
		fill_dictionary(return_on_assets, float("inf"), sic_code)

def fill_cfo_dict(stock, sic_code):
	try:
		cashflow = int(stock.get_operations_cash_flow(0))
		total_assets = int(stock.get_total_assets(1))
		cfo = cashflow/total_assets
		fill_dictionary(cashflow_from_operations, cfo, sic_code)
	except Exception as e:
		fill_dictionary(cashflow_from_operations, float("inf"), sic_code)

def fill_earnings_stability_dict(stock, sic_code):
	try:
		roa0 = int(stock.get_net_income(0))/int(stock.get_total_assets(1))
		roa1 = int(stock.get_net_income(1))/int(stock.get_total_assets(2))
		roa2 = int(stock.get_net_income(2))/int(stock.get_total_assets(3))
		roa3 = int(stock.get_net_income(3))/int(stock.get_total_assets(4))
		roa_list = [roa0, roa1, roa2, roa3]
		variance = np.var(roa_list)
		fill_dictionary(stability_of_earnings, variance, sic_code)
	except Exception as e:
		fill_dictionary(stability_of_earnings, float("-inf"), sic_code)
		
def fill_sales_growth_dict(stock, sic_code):
	try:
		growth0 = int(stock.get_net_income(0))-int(stock.get_net_income(1))
		growth1 = int(stock.get_net_income(1))-int(stock.get_net_income(2))
		growth2 = int(stock.get_net_income(2))-int(stock.get_net_income(3))
		growth_list = [growth0, growth1, growth2]
		variance = np.var(growth_list)
		fill_dictionary(sales_growth, variance, sic_code)
	except Exception as e:
		fill_dictionary(sales_growth, float("-inf"), sic_code)

def fill_rdi_dict(stock, sic_code):
	try:
		rd_expense = int(stock.get_research_development_expense(0))
		total_assets = int(stock.get_total_assets(1))
		rdi = rd_expense/total_assets
		fill_dictionary(research_development, rdi, sic_code)
	except Exception as e:
		fill_dictionary(research_development, float("inf"), sic_code)

def fill_cei_dict(stock, sic_code):
	try:
		ce = int(stock.get_capital_expenditure(0))
		total_assets = int(stock.get_total_assets(1))
		cei = ce/total_assets
		fill_dictionary(capital_expenditure, cei, sic_code)
	except Exception as e:
		fill_dictionary(capital_expenditure, float("inf"), sic_code)

def fill_aei_dict(stock, sic_code):
	try:
		ae = int(stock.get_advertising_expense(0))
		total_assets = int(stock.get_total_assets(1))
		aei = ae/total_assets
		fill_dictionary(advertising_expense, aei, sic_code)
	except Exception as e:
		fill_dictionary(advertising_expense, float("inf"), sic_code)


annual_report = open('./Data/Annual_Reports/Annual_Reports_17_Ticker_XML_SIC.txt', 'r')

# Dictionaries matching sic with financial data belonging to companies with corresponding sic
return_on_assets = dict()
cashflow_from_operations = dict()
stability_of_earnings = dict()
sales_growth = dict()
research_development = dict()
capital_expenditure = dict()
advertising_expense = dict()

count = 0
# Fill in the dictionaries with the financial data of every company we have data for
for line in annual_report:
	fields = line.strip().split('     ')
	sic_code = (fields[0])[:2]
	ticker = fields[1]
	stock = Stock(ticker)
	fill_roa_dict(stock, sic_code)
	fill_cfo_dict(stock, sic_code)
	fill_earnings_stability_dict(stock, sic_code)
	fill_sales_growth_dict(stock, sic_code)
	fill_rdi_dict(stock, sic_code)
	fill_cei_dict(stock, sic_code)
	fill_aei_dict(stock, sic_code)
	count += 1
	print(count)

# Find and delete any groups that have fewer than the threshold number of 
# companies that share its two-digit sic code
threshold = 3
delete_keys = []
for key in return_on_assets:
	if (len(return_on_assets[key]) < threshold):
		delete_keys.append(key)

for key in delete_keys:
	del return_on_assets[key]
	del cashflow_from_operations[key]
	del stability_of_earnings[key]
	del sales_growth[key]
	del research_development[key]
	del capital_expenditure[key]
	del advertising_expense[key]

# Find the median of each of the seven criterion
median_scores = {}
for key in return_on_assets:
	fill_dictionary(median_scores, np.median(return_on_assets[key]), key)
	fill_dictionary(median_scores, np.median(cashflow_from_operations[key]), key)
	fill_dictionary(median_scores, np.median(stability_of_earnings[key]), key)
	fill_dictionary(median_scores, np.median(sales_growth[key]), key)
	fill_dictionary(median_scores, np.median(research_development[key]), key)
	fill_dictionary(median_scores, np.median(capital_expenditure[key]), key)
	fill_dictionary(median_scores, np.median(advertising_expense[key]), key)

# Dump the data onto a json file
with open('data.json', 'w') as fp:
	json.dump(median_scores, fp, sort_keys=True, indent=4)