from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os
import random
import time

keywords = ["restaurants", "cafes", "cinemas"]

browser = None
city = None
customer_hotel = None
customer_location = None

temp_browser = None


def google_search(browser, search):
    browser.get("https://google.com/")
    search_box = browser.find_element_by_xpath('//input[@name="q"]')
    search_box.send_keys(search)
    search_form = browser.find_element_by_xpath('//form[@role="search"]')
    search_form.submit()


def initialize_browser():
    global browser
    opts = Options()
    # opts.add_argument('--headless')
    browser = webdriver.Firefox()


def close_browsers():
    global browser
    global temp_browser
    # browser.close()
    browser.quit()
    temp_browser.quit()


def pause(_time):
    time.sleep(_time)


def crawl_page(keyword):
    # /html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/div[2]/div
    # /html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[1]/span[2]
    # /html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[1]/span[1]
    # /html/body/div[6]/div/div[8]/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div[4]/div[6]/div/div[2]/div/a/div/span/div[2]/span/span
    global browser
    all_a_links = browser.find_elements_by_xpath('//a')
    at_least_one = False  # ovim Bool-om proveravamo da li je strana poslednja ili ne to jest da li postoji bar jedan restoran na strani
    total = 0
    niz = []
    for a_link in all_a_links:
        try:
            object_name = a_link.find_element_by_xpath('./div/div[2]/div').text
            object_number_of_ratings = a_link.find_element_by_xpath('./div/span/div[1]/span[2]').text
            object_rating = a_link.find_element_by_xpath('./div/span/div[1]/span[1]').text
            object_address = a_link.find_element_by_xpath('./div/span/div[2]/span/span').text
            object_number_of_ratings = int(object_number_of_ratings[1:-1].replace('.', '')) # brisanje zagrada
            a_link.click()
            pause(1.0)
            object_address = WebDriverWait(browser, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/span[2]"))).text#browser.find_element_by_xpath('/html/body/div[6]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/span[2]').text
            #pause(2.0)
            #/html/body/div[6]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/span[2]
            #/html/body/div[6]/div/div[8]/div[2]/div/div[2]/async-local-kp/div/div/div[1]/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[3]/div/div/span[2]
            print(object_name, object_rating, object_number_of_ratings, object_address)
            niz.append((object_name, object_rating, object_number_of_ratings, object_address))
            at_least_one = True
            total += 1
            #time.sleep(8.0)
        except Exception as e:
            continue
    file_path = os.path.realpath(__file__)
    last_index = file_path.rindex('/')
    file_path = file_path[:last_index]
    file_path = file_path + "/" + keyword + ".txt"
    print(file_path)
    with open(file_path,"w+") as file:
        for tuple_of_informations in niz:
            file.write('/0'.join( [str(x) for x in tuple_of_informations] )+"\n")
    return at_least_one, total


def crawl(keyword):
    global city
    global browser
    """
    browser.get("https://google.com/")
    search_box = browser.find_element_by_xpath('//input[@name="q"]')
    search = city + " " + keyword
    search_box.send_keys(search)
    search_form = browser.find_element_by_xpath('//form[@role="search"]')
    search_form.submit()
    """
    google_search(browser, city + " " + keyword)
    all_a_links = browser.find_elements_by_xpath('//a')
    right_a_link = None
    pause(5.0)
    right_a_link = browser.find_element_by_xpath('//a[@class="Q2MMlc"]')
    """
    for a_object in all_a_links:
        if "search" in a_object.get_attribute("href"):
            right_a_link = a_object
            break
    """
    right_a_link.click()
    total = 0
    while (True):
        pause(5.0)
        at_least_one, new_total = crawl_page(keyword)
        total += new_total
        if total >= 10:
            break
        if not at_least_one:
            print("ALL", keyword, "FOUND")
            break
        pause(2.0)
        try:
            next_page = browser.find_element_by_xpath('//a[@id="pnnext"]')
            next_page.click()
        except Exception as e:
            print("ALL", keyword, "FOUND")
            break


def crawl_hotels():
    # /html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div/g-more-link/a
    global city
    global browser
    search = city + " hotels"
    google_search(browser,search)
    pause(12.0)
    view_more_button = browser.find_element_by_xpath('/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div/g-more-link/a')
    view_more_button.click()
    # /html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div[1]/div[2]/main/div/div[2]/c-wiz/div[6]/c-wiz[1]/div/a
    # /html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div[1]/div[2]/main/div/div[2]/c-wiz/div[6]/c-wiz[2]/div/a
    # /html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div[1]/div[2]/main/div/div[2]/c-wiz/div[6]/c-wiz[16]/div/a
    all_hotels = browser.find_elements_by_xpath('//c-wiz')
    pause(10.0)
    for hotel in all_hotels:
        #print("HERE")
        try:
            # /html/body/c-wiz[2]/div/div[2]/div/c-wiz/div/div[1]/div[2]/main/div/div[2]/c-wiz/div[6]/c-wiz[1]/div/div/div/div[1]/div/div[1]/div[2]/a/div/div/div/span[1]/span/span[1]
            hotel_root_element = hotel.find_element_by_xpath('./div/a') # ovo je <a> koji sadrzi sve podatke o konkretnom hotelu
            hotel_name = hotel_root_element.get_attribute("aria-label") # text
            hotel_rating = hotel.find_element_by_xpath('./div/div/div/div[1]/div/div[1]/div[1]/div[1]/a/div/span/span/span/span[1]/span/span[1]').text
            hotel_reviews = hotel.find_element_by_xpath('./div/div/div/div[1]/div/div[1]/div[1]/div[1]/a/div/span/span/span/span[1]/span/span[3]').text
            hotel_reviews = hotel_reviews[:-10]
            hotel_reviews = hotel_reviews.replace('.', '')
            hotel_price = hotel.find_element_by_xpath('./div/div/div/div[1]/div/div[1]/div[2]/a/div/div/div/span[1]/span/span[1]').text
            hotel_price = hotel_price[:-4]
            hotel_price = hotel_price.replace(',', '')
            hotel_price = hotel_price.replace('.', '')
            hotel_location = get_hotel_location2(hotel_name)
            print(hotel_name,hotel_rating,hotel_reviews,hotel_price,hotel_location)
        except:
            continue
    browser.quit()


def get_hotel_location(hotel_name):
    # /html/body/div[7]/div/div[9]/div[3]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    # /html/body/div[7]/div/div[9]/div[3]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    global customer_location
    global city
    global temp_browser
    if city not in hotel_name:
        hotel_name = hotel_name + " " + city
    if temp_browser == None:
        temp_browser = webdriver.Firefox()
    google_search(temp_browser, hotel_name)
    pause(13.0)
    # /html/body/div[7]/div/div[9]/div[2]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    try:
        customer_location = temp_browser.find_element_by_xpath(
            '/html/body/div[7]/div/div[9]/div[2]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]').text
        print(customer_location)
    except:
        return -1
    return 1

def get_hotel_location2(hotel_name):
    # /html/body/div[7]/div/div[9]/div[3]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    # /html/body/div[7]/div/div[9]/div[3]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    global city
    global temp_browser
    if city not in hotel_name:
        hotel_name = hotel_name + " " + city
    if temp_browser == None:
        temp_browser = webdriver.Firefox()
    google_search(temp_browser, hotel_name)
    pause(5.0)
    # /html/body/div[7]/div/div[9]/div[2]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]
    location = None
    try:
        """
        location = temp_browser.find_element_by_xpath(
            '/html/body/div[7]/div/div[9]/div[2]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]').text
        """
        location = WebDriverWait(temp_browser, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div/div[9]/div[2]/div/div[1]/div/div[1]/div/div[4]/div/div[2]/div/div/span[2]"))).text
        #print(location,"ZZ")
    except:
        return -1
    return location


def main():
    global city
    global customer_hotel
    global customer_location
    global browser
    initialize_browser()
    if browser == None:
        print("ERROR WHILE BROWSER INITIALIZATION")
        close_browser()
        exit()
    city = input("Please enter city name: ")
    customer_hotel = input("Please enter name of your hotel(alternatively enter -1 to input address of your location): ")
    hotel_location_success = None
    if customer_hotel != "-1":
        hotel_location_success = get_hotel_location(customer_hotel)
    if customer_hotel == "-1" or hotel_location_success == -1:
        customer_location = input("Please enter your location: ")
    if city == None:
        print("ERROR WHILE CITY NAME INPUT")
        close_browser()
        exit()
    for keyword in keywords:
        crawl(keyword)
    time.sleep(10)
    crawl_hotels()
    close_browsers()
    time.sleep(10)


if __name__ == "__main__":
    main()


# python3 /Users/mbp/Downloads/gdsc_web_scraping.py
