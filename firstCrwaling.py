import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint


url = 'https://www.ekapepia.com/priceStat/distrPriceBeef.do'

# 축산물품질평가원 사이트에 html소스들을 문자열로 바꿔서 source변수에 넣기
source = requests.get(url, verify=False)
# 일련의 문자열만 가지고는 원하는 데이터를 갖고 올 수 없어서 뷰티풀솝 사용
# 요청받은 source변수를 가지고 뷰티풀솝에 html소스로 파싱해야한다고 옵션을 정하고 그 옵션을
# 통해 파싱한 결과값을 soup변수에 집어넣는다.
# 파이썬에서 보기 좋게, 다루기 쉽게 파싱작업을 거쳐야 각 요소에 접근이 쉬워진다.
soup = BeautifulSoup(source.text, "html.parser")

# soup 모듈의 find 함수를 사용하여 data1에 값을 저장하낟.
# 매개변수에는 div의 태그명과 class라는 속성의 값이
data1 = soup.find('tbody')


find_day = data1.find_all('tr')

for i in range(len(find_day)):
    date = find_day[i].find('th', {'scope': 'row'}).text

    catalog = '소'
    find_content = find_day[i].find_all('span', {'class': 'mr5'})
    female = find_content[0].text
    male = find_content[1].text
    male = re.findall('\d+', male)
    male = male[0] + "," + male[1]
    six = find_content[2].text
    six = re.findall('\d+', six)
    six = six[0] + "," + six[1]
    all_avg = find_content[3].text
    all_1 = find_content[4].text
    several_1 = find_content[5].text
    client_1 = find_content[6].text

    content = [date, female, male, six, all_avg, all_1, several_1, client_1]

    cow = {'품목', '날짜',
           '암송아지 경매가격', '숫송아지 경매가격', '농가수취가격',
           '도매 평균 지육가격', '도매 1등급 지육가격', '도매 1등급 부분육가격',
           '소비자 1등급 가격'}
    information = dict(zip(cow, content))

    pprint(information)
    print("----------")

    # 몽고DB에 넣기 시작
    from pymongo import MongoClient

    # localgost의 27017포트로 mongodb 인스턴스와 연결
    client = MongoClient('localhost', 27017)

    # cow_information이라는 데이터베이스 만듦
    db = client['livestock_information']
    collection = db.collection

    x = collection.insert_one(information)

    db.collection.remove({})
