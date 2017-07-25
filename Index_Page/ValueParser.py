import requests
import re

annual_reports = open('test.txt', 'r')
value_stocks_list = open('Value_List.txt', 'w')

for line in annual_reports:
	fields = line.strip().split('  ')
	report_index_page = fields[len(fields)-1]
	index_page_request = requests.get(report_index_page)
	index_page_text = index_page_request.text
	try:
		xml_file_link_regexp = r'<a href="/Archives/edgar/data/.*\d\.xml">'
		xml_report_link = re.findall(xml_file_link_regexp, index_page_text)
		xml_report_link = re.findall(r'".*"', xml_report_link[0])
		xml_report_link = xml_report_link[0]
		xml_report_link = xml_report_link[1:len(xml_report_link)-1]

		ticker_symbol = re.findall(r'\d+/.*-', xml_report_link)
		ticker_symbol = re.findall(r'\w+', ticker_symbol[0])
		ticker_symbol = ticker_symbol[len(ticker_symbol)-1]
		value_stocks_list.write(ticker_symbol)
		value_stocks_list.write('     ')
		value_stocks_list.write(xml_report_link + '\n')
	except Exception as e:
		print(e)