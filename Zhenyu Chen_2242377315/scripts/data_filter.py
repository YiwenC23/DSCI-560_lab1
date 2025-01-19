'''
Name: Zhenyu Chen
SID: 2242377315
Email: zhenyuch@usc.edu
'''

import os
import sys
import csv
from bs4 import BeautifulSoup


def filter_market_data(soup):
	try:
		market_banner = soup.find("div", class_ = "MarketsBanner-marketData")
		market_cards = market_banner.find_all("a", class_ = "MarketCard-container")

		market_data = []
		for card in market_cards:
			symbol = card.find("span", class_ = "MarketCard-symbol")
			stock_position = card.find("span", class_ = "MarketCard-stockPosition")
			change_pct = card.find("span", class_ = "MarketCard-changesPct")

			market_data.append([symbol.text.strip(), stock_position.text.strip(), change_pct.text.strip()])
		
		return market_data

	except Exception as e:
		print(f"Filtering market data failed. Reason: {e}")
		sys.exit()


def save_market_data(market_data):
	try:
		with open(market_csv_path, "w") as f:
			writer = csv.writer(f)
			writer.writerow(["Symbol", "Stock Position", "Change Percentage"])
			writer.writerows(market_data)
	except Exception as e:
		print(f"Storing market data failed. Reason: {e}")
		sys.exit()


def filter_latest_news(soup):
	try:
		news_list = soup.find("ul", class_ = "LatestNews-list")
		news_items = news_list.find_all("li", class_ = "LatestNews-item")
		
		news_data = []
		for item in news_items:
			timestamp = item.find("time", class_ = "LatestNews-timestamp")
			
			headline = item.find("a", class_ = "LatestNews-headline")
			title = headline.get("title")
			link = headline.get("href")
			
			news_data.append([timestamp.text.strip(), title, link])
		
		return news_data

	except Exception as e:
		print(f"Filtering latest news failed. Reason: {e}")
		sys.exit()


def save_news_data(news_data):
	try:
		with open(news_csv_path, "w") as f:
			writer = csv.writer(f)
			writer.writerow(["Timestamp", "Title", "Link"])
			writer.writerows(news_data)
	except Exception as e:
		print(f"Storing news data failed. Reason: {e}")
		sys.exit()


def main():
	print("Reading web data...")
	try:
		soup = BeautifulSoup(open(input_filepath), "html.parser")
		print("Successfully loaded web data!\n")
	except Exception as e:
		print(f"Failed to load web data. Reason: {e}")
		sys.exit()
	
	print("Filtering market data...")
	market_data = filter_market_data(soup)
	print("Successfully filtered market data!\n")

	print("Storing market data...")
	save_market_data(market_data)
	print("Successfully stored market data!\n")

	print("Filtering latest news...")
	news_data = filter_latest_news(soup)
	print("Successfully filtered latest news data!\n")

	print("Storing latest news data...")
	save_news_data(news_data)
	print("Successfully stored latest news data!\n")


if __name__ == "__main__":
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	BASE_DIR = os.path.dirname(CURRENT_DIR)
	
	input_filepath = os.path.join(BASE_DIR, "data/raw_data/web_data.html")
	market_csv_path = os.path.join(BASE_DIR, "data/processed_data/market_data.csv")
	news_csv_path = os.path.join(BASE_DIR, "data/processed_data/news_data.csv")
	
	main()

	print("Data Filtering Completed!")