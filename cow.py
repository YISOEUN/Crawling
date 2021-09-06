from time import sleep
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.keys import Keys


def changeDate(driver, url):
    # Read url
    driver.get(url)

    # Find date input box
    select_date = driver.find_element_by_css_selector('input#searchStartDate')
    select_date.click()
    sleep(1)  # Using 'sleep' to run in sequence

    # Set variable for 1-year data collection
    yearAgo = datetime.now() - relativedelta(years=1)
    yearAgo = yearAgo.strftime('%Y-%m-%d')

    for i in range(1, 9):  # Clear previously entered dates
        select_date.send_keys(Keys.BACKSPACE)
        select_date.send_keys(Keys.DELETE)
    select_date.send_keys(yearAgo)  # Enter start date
    sleep(1)

    # Click enter button
    select_date.find_element_by_xpath('//*[@id="ipt_search"]').send_keys((Keys.ENTER))
    sleep(5)


def cow(driver, url, collection):
    item = '소'
    catalog = ['품목', '날짜','암송아지 경매가격', '숫송아지 경매가격', '농가수취가격',
               '도매 평균 지육가격', '도매 1등급 지육가격', '도매 1등급 부분육가격', '소비자 1등급 가격']

    # Get url set to 1 year data
    changeDate(driver, url)

    # Convert web pages to html
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # Crawling data to enter in collection
    data1 = soup.find('tbody')

    one_day = data1.find_all('tr')

    for i in range(len(one_day)):
        date = one_day[i].find('th', {'scope': 'row'}).text
        content = [item, date]

        find_content = one_day[i].find_all('span', {'class': 'mr5'})
        for j in range(len(find_content)):
            price = find_content[j].text
            price = price.replace('\t', '').replace('\n', '').replace(' ', '')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)  # Enter data into collection


def pork(driver, url, collection):
    item = '돼지'
    catalog = ['품목', '날짜', '산지 농가수취가격', '도매 평균가격', '도매 1등급가격', '삼겹살 소비자가격']

    # Get url set to 1 year data
    changeDate(driver, url)

    # Convert web pages to html
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # Crawling data to enter in collection
    data1 = soup.find('tbody')
    one_day = data1.find_all('tr')
    for i in range(len(one_day)):
        date = one_day[i].find('th', {'scope': 'row'}).text
        content = [item, date]

        find_content = one_day[i].find_all('span', {'class': 'mr5'})
        for j in range(len(find_content)):
            price = find_content[j].text
            price = price.replace('\t','').replace('\n','').replace(' ','')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)  # Enter data into collection


def poultry(driver, url, collection):
    item = "육계"
    catalog = ['품목', '날짜', '산지 생계유통가격', '산지 위탁생계가격', '도매 10호 가격', '도매 전체 가격', '소매 가격']

    # Get url set to 1 year data
    changeDate(driver, url)

    # Convert web pages to html
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # Crawling data to enter in collection
    data1 = soup.find('tbody')

    one_day = data1.find_all('tr')

    for i in range(len(one_day)):
        date = one_day[i].find('th', {'class': 'first'}).text
        content = [item, date]

        find_content = one_day[i].find_all('td', {'class': 'align_right'})
        for j in range(len(find_content)):
            price = find_content[j].text
            price = price.replace('\t', '').replace('\n', '').replace(' ', '')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)  # Enter data into collection


def egg(driver, url, collection):
    item = '계란'
    catalog = ['품목', '날짜', '산지 30개 가격', '산지 10개 가격', '도매 10개 가격', '소비자 30개 가격']

    # Get url set to 1 year data
    changeDate(driver, url)

    # Convert web pages to html
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # Crawling data to enter in collection
    data1 = soup.find('tbody')

    one_day = data1.find_all('tr')

    for i in range(len(one_day)):
        date = one_day[i].find('th', {'scope': 'row'}).text
        date = date.replace('\t', '').replace('\n', '').replace(' ', '')
        content = [item, date]

        find_content = one_day[i].find_all('span', {'class': 'mr5'})
        for j in range(len(find_content)):
            price = find_content[j].text
            price = price.replace('\t','').replace('\n','').replace(' ', '')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)  # Enter data into collection


def duck(driver, url, collection):
    item = '오리'
    catalog = ['품목', '날짜', '산지가격', '도매가격']

    # Get url set to 1 year data
    changeDate(driver, url)

    # Convert web pages to html
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # Crawling data to enter in collection
    data1 = soup.find('tbody')

    one_day = data1.find_all('tr')

    for i in range(len(one_day)):
        date = one_day[i].find('th', {'class': 'first'}).text
        content = [item, date]

        find_content = one_day[i].find_all('td', {'class': 'align_right'})
        delete = one_day[i].find_all('span')

        for j in range(len(find_content)):
            price = find_content[j].text
            if len(delete) != 0:
                up = delete[j].text
                price = price.replace(up, '', -1)
            price = price.replace('\t', '').replace('\n', '').replace(' ', '')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)  #Enter data into collection


def main():
    # Associate with the MongoDB instance with 27017 ports on localhost
    client = MongoClient('localhost', 27017)

    # Create a database called livestock_information
    db = client.livestock_information
    database = [db.cow, db.pork, db.poultry, db.egg, db.duck]

    # get selenium
    path = 'C:/Users/YISOEUN/PycharmProjects\chromedriver_win32./chromedriver.exe'
    driver = webdriver.Chrome(path)

    page = ['https://www.ekapepia.com/priceStat/distrPriceBeef.do?menuId=menu100033&boardInfoNo=',
            'https://www.ekapepia.com/priceStat/distrPricePork.do?menuId=menu100034&boardInfoNo=',
            'https://www.ekapepia.com/priceStat/poultry/periodMarketPrice.do?menuId=menu100039&boardInfoNo=',
            'https://www.ekapepia.com/priceStat/distrPriceEgg.do?menuId=menu100155&boardInfoNo=',
            'https://www.ekapepia.com/priceStat/distrPriceDuck.do?menuId=menu100151&boardInfoNo=']

    for i in range(5):
        url = page[i]
        collection = database[i]
        if i == 0:
            cow(driver, url, collection)
        elif i == 1:
            pork(driver, url, collection)
        elif i == 2:
            poultry(driver, url, collection)
        elif i == 3:
            egg(driver, url, collection)
        elif i == 4:
            duck(driver, url, collection)


main()
