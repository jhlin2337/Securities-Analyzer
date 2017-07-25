import requests
import re

reports_path = './Annual_Reports/'
crawler_path = './Annual_Reports/Crawler_Files/'

crawler1 = crawler_path + 'Crawler_15Q1.idx'
crawler2 = crawler_path + 'Crawler_15Q2.idx'
crawler3 = crawler_path + 'Crawler_15Q3.idx'
crawler4 = crawler_path + 'Crawler_15Q4.idx'
report = reports_path + 'Annual_Reports_15.txt'
reportxml = reports_path + 'Annual_Reports_15_Ticker_XML.txt'

# Open necessary files
crawler_q1 = open(crawler1, 'r')
crawler_q2 = open(crawler2, 'r')
crawler_q3 = open(crawler3, 'r')
crawler_q4 = open(crawler4, 'r')

annual_report = open(report, 'w')

# Dump annual reports data into Annual_Reports.txt
for line in crawler_q1:
	if '10-K' in line and 'NT 10-K' not in line and '10-K/A' not in line and '10-KT' not in line:
		annual_report.write(line)

for line in crawler_q2:
	if '10-K' in line and 'NT 10-K' not in line and '10-K/A' not in line and '10-KT' not in line:
		annual_report.write(line)

for line in crawler_q3:
	if '10-K' in line and 'NT 10-K' not in line and '10-K/A' not in line and '10-KT' not in line:
		annual_report.write(line)

for line in crawler_q4:
	if '10-K' in line and 'NT 10-K' not in line and '10-K/A' not in line and '10-KT' not in line:
		annual_report.write(line)

# Close all files
crawler_q1.close()
crawler_q2.close()
crawler_q3.close()
crawler_q4.close()
annual_report.close()

# Open annual reports files for reading and writing
annual_reports = open(report, 'r')
annual_reports_ticker_xml = open(reportxml, 'w')

for line in annual_reports:
	# Request annual report index webpage
	fields = line.strip().split('  ')
	report_index_page = fields[len(fields)-1]
	index_page_request = requests.get(report_index_page)
	index_page_text = index_page_request.text
	try:
		# Find xml link
		xml_file_link_regexp = r'<a href="/Archives/edgar/data/.*\d\.xml">'
		xml_report_link = re.findall(xml_file_link_regexp, index_page_text)
		xml_report_link = re.findall(r'".*"', xml_report_link[0])
		xml_report_link = xml_report_link[0]
		xml_report_link = xml_report_link[1:len(xml_report_link)-1]

		# Find ticker symbol
		ticker_symbol = re.findall(r'\d+/.*-', xml_report_link)
		ticker_symbol = re.findall(r'\w+', ticker_symbol[0])
		ticker_symbol = ticker_symbol[len(ticker_symbol)-1]

		# Write data into file
		annual_reports_ticker_xml.write(ticker_symbol + '     ')
		annual_reports_ticker_xml.write(xml_report_link + '\n')
	except Exception as e:
		print(e)

# Close files and finish
annual_report.close()
annual_reports_ticker_xml.close()