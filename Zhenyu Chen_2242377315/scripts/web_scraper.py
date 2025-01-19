'''
Name: Zhenyu Chen
SID: 2242377315
Email: zhenyuch@usc.edu
'''

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def get_static_data():
	try:
		response = requests.get(url)
		response.raise_for_status()
		
		static_soup = BeautifulSoup(response.text, "html.parser")
		print("Successfully fetched static data!\n")
		return static_soup
	
	except requests.RequestException as e:
		print(f"Failed to fetch static data. Reason: {e}")
		sys.exit()

def get_dynamic_data():
	try:
		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")
		
		driver = webdriver.Chrome(options = options, service = ChromeService(ChromeDriverManager().install()))
		driver.get(url)
		time.sleep(10)
		html_handle = driver.page_source
		driver.quit()
		
		dynamic_soup = BeautifulSoup(html_handle, "html.parser")
		print("Successfully fetched dynamic market data!\n")
		return dynamic_soup
	
	except Exception as e:
		print(f"Getting dynamic data failed. Reason: {e}")
		sys.exit()


def generate_web_data():
	try:
		print("Gathering static data...")
		static_soup = get_static_data()
		
		print("Gathering dynamic data...")
		dynamic_soup = get_dynamic_data()
		
		print("Getting complete web data by replacing the section tag in static data with the one in dynamic data...")
		static_soup.section.replace_with(dynamic_soup.section)
		
		print("Successfully generated complete web data!\n")
		return static_soup
	
	except Exception as e:
		print(f"Generating web data failed. Reason: {e}")
		sys.exit()


def save_web_data(web_data):
	try:
		with open(output_path, "w", encoding = "utf-8") as f:
			f.write(web_data.prettify())
		print("Successfully stored web data in an HTML file!\n")
	except Exception as e:
		print(f"Storing web data in an HTML file failed. Reason: {e}")


if __name__ == "__main__":
	url = "https://www.cnbc.com/world/?region=world"
	
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	output_path = os.path.join(CURRENT_DIR, "../data/raw_data/web_data.html")
	
	web_data = generate_web_data()
	
	print("Storing web data in an HTML file...")
	save_web_data(web_data)

	print("Web Scraping Completed!")
