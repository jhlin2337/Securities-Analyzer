import requests
import re

# Open necessary files
crawler_q1 = open('Crawler_Q1.idx', 'r')
crawler_q2 = open('Crawler_Q2.idx', 'r')
crawler_q3 = open('Crawler_Q3.idx', 'r')

annual_report = open('Annual_Reports.txt', 'w')

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

# Close all files
crawler_q1.close()
crawler_q2.close()
crawler_q3.close()
annual_report.close()

# Open annual reports files for reading and writing
annual_reports = open('Annual_Reports.txt', 'r')
annual_reports_ticker_xml = open('Annual_Reports_Ticker_XML.txt', 'w')

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