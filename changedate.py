from time import sleep

from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
from selenium.webdriver.common.keys import Keys


def cow(url, collection):

    yearAgo = datetime.now() - relativedelta(years=1)
    yearAgo = yearAgo.strftime('%Y-%m-%d')
    print(yearAgo)

    # t셀리니움 설치
    path = 'C:/Users/YISOEUN/PycharmProjects\chromedriver_win32./chromedriver.exe'
    driver = webdriver.Chrome(path)

    driver.get(url)

    select_date = driver.find_element_by_css_selector('input#searchStartDate')
    select_date.click()
    sleep(2)  # 컴퓨터속도가 너무 빨라서 사이사이에 sleep으로 2초정도식 쉬어줘야 원하는 대로 구동된다.

    for i in range(1, 9):
        select_date.send_keys(Keys.BACKSPACE)  # 기존에 입력된 날짜 지워주기.
        select_date.send_keys(Keys.DELETE)
    select_date.send_keys(yearAgo)  # 시작날짜 내맘대로 세팅하기
    sleep(2)

    select_date.find_element_by_xpath('//*[@id="ipt_search"]').send_keys((Keys.ENTER))

    item = '소'
    catalog = ['품목', '날짜', '암송아지 경매가격', '숫송아지 경매가격', '농가수취가격',
               '도매 평균 지육가격', '도매 1등급 지육가격', '도매 1등급 부분육가격', '소비자 1등급 가격']

    source = requests.get(url, verify=False)
    soup = BeautifulSoup(source.text, "html.parser")
    data1 = soup.find('tbody')

    find_day = data1.find_all('tr')

    for i in range(len(find_day)):
        date = find_day[i].find('th', {'scope': 'row'}).text
        content = [item, date]

        find_content = find_day[i].find_all('span', {'class': 'mr5'})
        for j in range(len(find_content)):
            price = find_content[j].text
            price = price.replace('\t', '').replace('\n', '').replace(' ', '')
            content.append(price)

        information = dict(zip(catalog, content))
        collection.insert_one(information)


def main():
    # localgost의 27017포트로 mongodb 인스턴스와 연결
    client = MongoClient('localhost', 27017)

    # cow_information이라는 데이터베이스 만듦
    db = client.livestock_information
    collection = db.collection

    page = ['https://www.ekapepia.com/priceStat/distrPriceBeef.do?menuId=menu100033&boardInfoNo=']

    for i in range(5):
        url = page[i]
        if i == 0:
            cow(url, collection)


main()
