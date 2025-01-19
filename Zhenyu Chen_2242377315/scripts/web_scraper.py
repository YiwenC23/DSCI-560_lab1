'''
Name: Zhenyu Chen
SID: 2242377315
Email: zhenyuch@usc.edu
'''

import os
import requests
from bs4 import BeautifulSoup

def get_html(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		print("Successfully fetched web data!\n")
		return response.content
	except requests.RequestException as e:
		print(f"Failed to fetch web data. Reason: {e}")
		return None

def parse_html(data):
	if not data:
		return None
	try:
		soup = BeautifulSoup(data, "html.parser")
		print("Successfully parsed HTML!\n")
		return soup
	except Exception as e:
		print(f"Failed to parse HTML. Reason: {e}")
		return None

def save_html(soup):
	if not soup:
		return False
	try:
		with open(output_path, "w", encoding = "utf-8") as f:
			f.write(soup.prettify())
		return True
	except Exception as e:
		print(f"Failed to write HTML to file. Reason: {e}")
		return False

if __name__ == "__main__":
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	output_path = os.path.join(CURRENT_DIR, "../data/raw_data/web_data.html")
	url = "https://www.cnbc.com/world/?region=world"
	
	print("Gathering web data...")
	web_data = get_html(url)
	
	print("Parsing HTML...")
	soup = parse_html(web_data)
	
	print("Writing HTML to file...")
	if save_html(soup):
		print("Successfully completed web scraping!")
	else:
		print("Web scraping failed!")
