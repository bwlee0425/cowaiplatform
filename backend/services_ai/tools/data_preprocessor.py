from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['cowai_db']
collection = db['cctv_logs']

def save_frame_metadata(frame_data):
    collection.insert_one(frame_data)

# 비정형 데이터 (CCTV 프레임 메타데이터, AI 모델 로그 등).