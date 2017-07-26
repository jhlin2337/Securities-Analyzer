from Stock import Stock

class Value:
	
	THRESHOLD = 6	# Number of requirements that need to be met in order to not be filtered out

	# Initializes the list of high BM stocks that the code will run through
	def __init__(self):
		self.value_stocks = open('./Data/Stocks_List/Value_Stocks.txt', 'r')
		
	# Returns a list of value stocks that have an F_Score greater than THRESHOLD
	def get_value_stocks(self):
		for line in self.value_stocks:
			ticker = line[:len(line)-1]
			requirements_satisfied = self.get_number_requirements_satisfied(ticker)
			if len(requirements_satisfied) > self.THRESHOLD:
				print('--------------------------------------------------------------')
				print(ticker + ': ' + str(len(requirements_satisfied)))
				print(requirements_satisfied)
				#self.print_data(ticker)

	# Appends each F_Score requirement that <ticker> meets onto an array and returns
	# the array
	def get_number_requirements_satisfied(self, ticker):
		stock = Stock(ticker)
		requirements_satisfied = []

		if self.satisfies_roa_requirement(stock):
			requirements_satisfied.append('ROA')
		if self.satisfies_cfo_requirement(stock):
			requirements_satisfied.append('CFO')
		if self.satisfies_delta_roa_requirement(stock):
			requirements_satisfied.append('Delta_ROA')
		if self.satisfies_accrual_requirement(stock):
			requirements_satisfied.append('Accrual')
		if self.satisfies_delta_leverage_requirement(stock):
			requirements_satisfied.append('Delta_Leverage')
		if self.satisfies_delta_liquidity_requirement(stock):
			requirements_satisfied.append('Delta_Liquidity')
		if self.satisfies_delta_margin_requirement(stock):
			requirements_satisfied.append('Delta_Margin')
		if self.satisfies_delta_turnover_requirement(stock):
			requirements_satisfied.append('Delta_Turnover')

		return requirements_satisfied

	# Returns True if the company's return on assets is positive; returns False otherwise
	def satisfies_roa_requirement(self, stock):
		try:
			net_income = int(stock.get_net_income(0))
			if net_income > 0:
				return True
		except:
			pass

		return False

	# Returns True if the company's cash flow from operations is positive; returns False otherwise
	def satisfies_cfo_requirement(self, stock):
		try:
			cfo = int(stock.get_operations_cash_flow(0))
			if cfo > 0:
				return True
		except:
			pass

		return False

	# Returns True if the company's return on assets this year is greater than its return on assets
	# for the previous year. Returns False otherwise
	def satisfies_delta_roa_requirement(self, stock):
		try:
			current_roa = int(stock.get_net_income(0))/int(stock.get_total_assets(1))
			prev_roa = int(stock.get_net_income(1))/int(stock.get_total_assets(2))
			if current_roa > prev_roa:
				return True
		except:
			pass

		return False

	# Returns True if the company's accrual has decreased; returns False otherwise
	def satisfies_accrual_requirement(self, stock):
		try: 
			net_income = int(stock.get_net_income(0))
			cfo = int(stock.get_operations_cash_flow(0))
			if cfo > net_income:
				return True
		except:
			pass

		return False

	# Returns True if the company's leverage has decreased over the past year; returns False otherwise
	def satisfies_delta_leverage_requirement(self, stock):
		try:
			average_total_assets = (int(stock.get_total_assets(0)) + int(stock.get_total_assets(1)))/2
			prev_average_total_assets = (int(stock.get_total_assets(1)) + int(stock.get_total_assets(2)))/2
			current_leverage = int(stock.get_long_term_liabilities(0))/average_total_assets
			previous_leverage = int(stock.get_long_term_liabilities(1))/prev_average_total_assets
			if current_leverage < previous_leverage:
				return True
		except:
			pass

		return False

	# Returns True if the company's liquidity has increased over the past year; returns False otherwise
	def satisfies_delta_liquidity_requirement(self, stock):
		try:
			current_liquidity = int(stock.get_current_assets(0))/int(stock.get_current_liabilities(0))
			previous_liquidity = int(stock.get_current_assets(1))/int(stock.get_current_liabilities(1))
			if current_liquidity > previous_liquidity:
				return True
		except:
			pass

		return False

	# Returns True if the company's margins have improved over the past year; returns False otherwise
	def satisfies_delta_margin_requirement(self, stock):
		try:
			current_revenue = int(stock.get_revenue(0))
			current_cogs = int(stock.get_cost_of_goods_sold(0))
			current_margin = (current_revenue-current_cogs)/current_revenue

			previous_revenue = int(stock.get_revenue(1))
			previous_cogs = int(stock.get_cost_of_goods_sold(1))
			previous_margin = (previous_revenue-previous_cogs)/previous_revenue

			if current_margin > previous_margin:
				return True
		except:
			pass

		return False

	# Returns True if the company's asset turnover ratio has increased over the past year; return False otherwise
	def satisfies_delta_turnover_requirement(self, stock):
		try:
			current_turnover = int(stock.get_revenue(0))/int(stock.get_total_assets(1))
			previous_turnover = int(stock.get_revenue(1))/int(stock.get_total_assets(2))

			if current_turnover > previous_turnover:
				return True
		except:
			pass

		False

	def print_data(self, ticker):
		stock = Stock(ticker)

		# Retrieve the company's financial data for the most recent year
		total_assets = stock.get_total_assets(0)
		current_assets = stock.get_current_assets(0)
		total_liabilities = stock.get_total_liabilities(0)
		current_liabilities = stock.get_current_liabilities(0)
		long_term_liabilities = stock.get_long_term_liabilities(0)
		net_income = stock.get_net_income(0)
		revenue = stock.get_revenue(0)
		cost_of_goods_sold = stock.get_cost_of_goods_sold(0)
		cash_flow_from_operations = stock.get_operations_cash_flow(0)

		# Retrieve the company's financial data for last year
		previous_total_assets = stock.get_total_assets(1)
		previous_current_assets = stock.get_current_assets(1)
		previous_total_liabilities = stock.get_total_liabilities(1)
		previous_current_liabilities = stock.get_current_liabilities(1)
		previous_long_term_liabilities = stock.get_long_term_liabilities(1)
		previous_net_income = stock.get_net_income(1)
		previous_revenue = stock.get_revenue(1)
		previous_cost_of_goods_sold = stock.get_cost_of_goods_sold(1)
		previous_cash_flow_from_operations = stock.get_operations_cash_flow(1)

		# Retrieve the company's financial data for two years ago
		prev_prev_total_assets = stock.get_total_assets(2)


		# Calculate F Score ratios
		try: 
			roa = int(net_income)/int(previous_total_assets)
		except:
			roa = 'error'
		try:
			cfo = int(cash_flow_from_operations)/int(previous_total_assets)
		except:
			cfo = 'error'
		try:
			delta_roa = int(roa) - (int(previous_net_income)/int(prev_prev_total_assets))
		except:
			delta_roa = 'error'
		try:
			accrual = roa - cfo
		except:
			accrual = 'error'
		try:
			average_total_assets = (int(total_assets) + int(previous_total_assets))/2
			previous_average_total_assets = (int(previous_total_assets) + int(prev_prev_total_assets))/2
			delta_leverage = (int(long_term_liabilities)/average_total_assets - (int(previous_long_term_liabilities)/previous_average_total_assets))
		except:
			delta_leverage = 'error'
		try:
			delta_liquidity = (int(current_assets)/int(current_liabilities)) - (int(previous_current_assets)/int(previous_current_liabilities))
		except:
			delta_liquidity = 'error'
		try:
			delta_margin = ((int(revenue) - int(cost_of_goods_sold))/int(revenue)) - ((int(previous_revenue) - int(previous_cost_of_goods_sold))/int(previous_revenue))
		except:
			delta_margin = 'error'
		try:
			delta_turnover = (int(revenue)/int(previous_total_assets)) - (int(previous_revenue)/int(prev_prev_total_assets))
		except:
			delta_turnover = 'error'

		# Print F Score ratios
		print('Return on Assets:      ' + str(roa))
		print('Operations Cash Flow:  ' + str(cfo))
		print('Change in ROA:         ' + str(delta_roa))
		print('Accrual:               ' + str(accrual))
		print('Change in Leverage:    ' + str(delta_leverage))
		print('Change in Liquidity:   ' + str(delta_liquidity))
		print('Change in Margin:      ' + str(delta_margin))
		print('Change in Turnover:    ' + str(delta_turnover))
		print('')

		# Print financial data
		N = 0
		print('Total Assets:          ' + stock.get_total_assets(N))
		print('Current Assets:        ' + stock.get_current_assets(N))
		print('Total Liabilities:     ' + stock.get_total_liabilities(N))
		print('Current Liabilities:   ' + stock.get_current_liabilities(N))
		print('Long Term Liabilities: ' + stock.get_long_term_liabilities(N))
		print('Net Income:            ' + stock.get_net_income(N))
		print('Revenue:               ' + stock.get_revenue(N))
		print('Cost of Goods Sold:    ' + stock.get_cost_of_goods_sold(N))
		print('Operations Cash Flow:  ' + stock.get_operations_cash_flow(N))


value = Value()
value.get_value_stocks()