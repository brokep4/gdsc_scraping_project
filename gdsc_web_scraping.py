from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import random
import time

keywords = ["restaurants","gym", "cinema", "cafe"]
#hotele naknadno obraditi
#ne radi gym

browser = None
city = None

def initialize_browser():
	global browser
	opts = Options()
	#opts.add_argument('--headless')
	browser = webdriver.Firefox()

def close_browser():
	global browser
	#browser.close()
	browser.quit()

def pauza(_time):
	time.sleep(_time)

def crawl_page():
	#/html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/div[2]/div
	#/html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[1]/span[2]
	#/html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[1]/span[1]
	#/html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[2]/span/span
	all_a_links = browser.find_elements_by_xpath('//a')
	bar_jedan = False #ovim Bool-om proveravamo da li je strana poslednja ili ne to jest da li postoji bar jedan restoran na strani
	total = 0
	for a_link in all_a_links:
		try:
			object_name = a_link.find_element_by_xpath('./div/div[2]/div').text
			object_number_of_ratings = a_link.find_element_by_xpath('./div/span/div[1]/span[2]').text
			object_rating = a_link.find_element_by_xpath('./div/span/div[1]/span[1]').text
			object_address = a_link.find_element_by_xpath('./div/span/div[2]/span/span').text
			#brisanje zagrada
			object_number_of_ratings = int(object_number_of_ratings[1:-1].replace('.',''))
			#brisanje zagrada
			print(object_name,object_rating,object_number_of_ratings,object_address)
			bar_jedan = True
			total += 1
		except Exception as e:
			continue

	return bar_jedan, total


def crawl(keyword):
	global city
	browser.get("https://google.com/")
	search_box = browser.find_element_by_xpath('//input[@name="q"]')
	search = city + " " + keyword
	search_box.send_keys(search)
	search_form = browser.find_element_by_xpath('//form[@role="search"]')
	search_form.submit()
	all_a_links = browser.find_elements_by_xpath('//a')
	right_a_link = None
	pauza(5.0)
	right_a_link = browser.find_element_by_xpath('//a[@class="Q2MMlc"]')
	"""
	for a_object in all_a_links:
		if "search" in a_object.get_attribute("href"):
			right_a_link = a_object
			break
	"""
	right_a_link.click()
	total = 0
	while(True):
		pauza(5.0)
		bar_jedan, new_total = crawl_page()
		total += new_total
		if total >= 10:
			break
		if not bar_jedan:
			print("ALL",keyword,"FOUND")
			break
		pauza(2.0)
		try:
			next_page = browser.find_element_by_xpath('//a[@id="pnnext"]')
			next_page.click()
		except Exception as e:
			print("ALL",keyword,"FOUND")
			break
			


def main():
	global city
	initialize_browser()
	if initialize_browser == None:
		print("ERROR WHILE BROWSER INITIALIZATION")
		close_browser()
		exit()
	city = input("Please enter city name:")
	if city == None:
		print("ERROR WHILE CITY NAME INPUT")
		close_browser()
		exit()
	for keyword in keywords:
		crawl(keyword)

	time.sleep(10)
	close_browser()

if __name__ == "__main__":
	main()

#python3 /Users/mbp/Downloads/gdsc_web_scraping.py

