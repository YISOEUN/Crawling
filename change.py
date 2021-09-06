# 몽고DB에 넣기 시작
from pymongo import MongoClient
    # localgost의 27017포트로 mongodb 인스턴스와 연결
client = MongoClient('localhost', 27017)

    # cow_information이라는 데이터베이스 만듦
db = client['livestock_information']
collection = db.collection

db.collection.remove({})
