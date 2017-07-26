from Stock import Stock
import json
import time

class Growth:

	THRESHOLD = 5	# Number of requirements that need to be met in order to not be filtered out
	ROA_INDEX = 0	# Index of industry median return on assets
	CFO_INDEX = 1	# Index of industry median operations cash flow
	SOE_INDEX = 2	# Index of industry median stability of earnings
	SGV_INDEX = 3	# Index of industry median sales growth variability
	RDI_INDEX = 4	# Index of industry median research development intensity
	CEI_INDEX = 5	# Index of industry median capital expenditure intensity
	AEI_INDEX = 6	# Index of industry median advertising expense intensity

	# Initializes the industry median dictionary and the list of low BM stocks that 
	# the code will run through
	def __init__(self):
		fp = open('./Data/Industry_Medians.json', 'r')
		self.industry_medians = json.load(fp)
		self.growth_stocks = open('./Data/Stocks_List/Growth_Stocks.txt', 'r')

	# Returns a list of growth stocks that have an F_Score greater than THRESHOLD
	def get_growth_stocks(self):
		for line in self.growth_stocks:
			ticker = line[:len(line)-1]
			requirements_satisfied = self.get_number_requirements_satisfied(ticker)
			if len(requirements_satisfied) > self.THRESHOLD:
				print('--------------------------------------------------------------')
				print(ticker + ': ' + str(len(requirements_satisfied)))
				print(requirements_satisfied)

	# Appends each G_Score requirement that <ticker> meets onto an array and returns
	# the array
	def get_number_requirements_satisfied(self, ticker):
		stock = Stock(ticker)
		requirements_satisfied = []

		if self.satisfies_roa_requirement(stock):
			requirements_satisfied.append('Return_On_Assets')
		if self.satisfies_cfo_requirement(stock):
			requirements_satisfied.append('Operations_Cashflow')
		if self.satisfies_accrual_requirement(stock):
			requirements_satisfied.append('Accrual')
		if self.satisfies_earnings_stability_requirement(stock):
			requirements_satisfied.append('Earnings_Stability')
		if self.satisfies_sales_growth_requirement(stock):
			requirements_satisfied.append('Sales_Growth')
		if self.satisfies_research_development_requirement(stock):
			requirements_satisfied.append('Research_Development')
		if self.satisfies_capital_expenditure_requirement(stock):
			requirements_satisfied.append('Capital_Expenditure')
		if self.satisfies_advertising_expense_requirement(stock):
			requirements_satisfied.append('Advertising_Expense')

		return requirements_satisfied

	# Returns True if the company's roa is greater than the industry median. Returns False otherwise
	def satisfies_roa_requirement(self, stock):
		try:
			net_income = int(stock.get_net_income(0))
			total_assets = int(stock.get_total_assets(1))
			roa = net_income/total_assets
			sic = stock.get_sic_code()

			if roa > (self.industry_medians[sic])[self.ROA_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's cfo is greater than the industry median. Return False otherwise
	def satisfies_cfo_requirement(self, stock):
		try:
			cashflow = int(stock.get_operations_cash_flow(0))
			total_assets = int(stock.get_total_assets(1))
			cfo = cashflow/total_assets
			sic = stock.get_sic_code()

			if cfo > (self.industry_medians[sic])[self.CFO_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's accruals is negative. Returns False otherwise
	def satisfies_accrual_requirement(self, stock):
		try:
			net_income = int(stock.get_net_income(0))
			cashflow = int(stock.get_operations_cash_flow(0))

			if cashflow > net_income:
				return True
		except:
			pass

		return False

	# Returns True if the company's earnings roa variability is less than the 
	# industry median. Returns False otherwise
	def satisfies_earnings_stability_requirement(self, stock):
		try:
			roa0 = int(stock.get_net_income(0))/int(stock.get_total_assets(1))
			roa1 = int(stock.get_net_income(1))/int(stock.get_total_assets(2))
			roa2 = int(stock.get_net_income(2))/int(stock.get_total_assets(3))
			roa3 = int(stock.get_net_income(3))/int(stock.get_total_assets(4))
			roa_list = [roa0, roa1, roa2, roa3]
			variance = np.var(roa_list)
			sic = stock.get_sic_code()

			if variance < (self.industry_medians[sic])[self.SOE_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's sales growth variability is less than the
	# industry median. Returns False otherwise
	def satisfies_sales_growth_requirement(self, stock):
		try:
			growth0 = int(stock.get_net_income(0))-int(stock.get_net_income(1))
			growth1 = int(stock.get_net_income(1))-int(stock.get_net_income(2))
			growth2 = int(stock.get_net_income(2))-int(stock.get_net_income(3))
			growth_list = [growth0, growth1, growth2]
			variance = np.var(growth_list)
			sic = stock.get_sic_code()

			if variance < (self.industry_medians[sic])[self.SGV_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's research development intensity is greater 
	# than the industry median. Returns False otherwise
	def satisfies_research_development_requirement(self, stock):
		try:
			research_development = int(stock.get_research_development_expense(0))
			total_assets = int(stock.get_total_assets(1))
			rdi = research_development/total_assets
			sic = stock.get_sic_code()

			if rdi > (self.industry_medians[sic])[self.RDI_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's capital expenditure intensity is greater
	# than the industry median. Returns False otherwise
	def satisfies_capital_expenditure_requirement(self, stock):
		try:
			ce = int(stock.get_capital_expenditure(0))
			total_assets = int(stock.get_total_assets(1))
			cei = ce/total_assets
			sic = stock.get_sic_code()

			if cei > (self.industry_medians[sic])[self.CEI_INDEX]:
				return True
		except:
			pass

		return False

	# Returns True if the company's advertising expense intensity is greater
	# than the industry median. Returns False otherwise
	def satisfies_advertising_expense_requirement(self, stock):
		try:
			ae = int(stock.get_advertising_expense(0))
			total_assets = int(stock.get_total_assets(1))
			aei = ae/total_assets
			sic = stock.get_sic_code()

			if aei > (self.industry_medians[sic])[self.AEI_INDEX]:
				return True
		except:
			pass

		return False

stocks = Growth()
stocks.get_growth_stocks()