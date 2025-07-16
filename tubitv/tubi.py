import requests
import asyncio
import functools
import backoff
import aiohttp
import schedule
from pathlib import Path
import datetime
import time
import redis
from concurrent.futures import ThreadPoolExecutor
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, JSON, Integer, DateTime
import json

redis_client = redis.Redis.from_url('redis://:wnhmsy@43.157.146.240:6379/15')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# engine = create_engine('mysql+pymysql://root:123456@localhost:3306/movie')
engine = create_engine('mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider')
Session = sessionmaker(bind=engine)
base = declarative_base()

# 任务池配置
TASK_POOL_SIZE = 20
taks_pool = asyncio.Queue(maxsize=TASK_POOL_SIZE)

# 批量处理配置
WORKER_COUNT = 10
BATCH_SIZE = 5

processing_concurrency = 20
semaphore = asyncio.Semaphore(processing_concurrency)
executor = ThreadPoolExecutor()

def log_retry_error(details):
    logger = logging.getLogger('AsyncCosUploader')
    logger.error(f"Retrying {details['tries']}: \nexception={details['exception']} \nargs={details['args']}")

aio_retry = functools.partial(
    backoff.on_exception,
    backoff.expo,
    (Exception, ),
    max_tries=3,
    on_backoff=log_retry_error,
    logger=logging.getLogger('AsyncCosUploader')
)()

class TUBI(base):
    __tablename__ = 'tubitv_living'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    description_channel = Column(Text)
    m3u8_url = Column(Text)
    background_img = Column(String(255))
    hero_img = Column(String(255))
    landscape_img = Column(String(255))
    poster_img = Column(String(255))
    thumbnail_img = Column(String(255))
    programs = Column(JSON)
    updatetime = Column(DateTime)


class Tubi_project():
    def __init__(self):
        self.headers = {
            'authorization': 'Bearer eyJhbGciOiJFZERTQSIsImtpZCI6IjliNTMyOTg1LTE5ODgtNGQ4Mi04ZjA0LTIzYzVmYjE3YjZhOSIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJKb2tlbiIsImJkIjoxMDg4NzI2NDAwLCJkZXZpY2VfaWQiOiI3OTY1NDNlZS00MTY4LTQ3MGItODUzYy0yMmVkMDdmNjg1YzAiLCJleHAiOjE3NTI3MzczODEsImdkIjowLCJpYXQiOjE3NTE1Mjc3ODEsImlzX2d1ZXN0IjpmYWxzZSwiaXNzIjoiVHViaSBBY2NvdW50IFNlcnZpY2UiLCJqdGkiOiIzMTdhcWY2MmtsMjBjZTFtc2NhZm43ZzIiLCJuYmYiOjE3NTE1Mjc3ODEsInBsYXRmb3JtIjoid2ViIiwicmF0aW5nIjozLCJ0eXBlIjoxLCJ1c2VyX2lkIjo0NDMwMTk1NzcsInVzZXJfdXVpZCI6ImQ2OTgzZDFiLWNjYWEtNDk1MS1hZGY5LWNmZjRmZTk3ZWQ5NCJ9.wxYHVEB_yjJ9fTguOrjNVf55PTvQ8q0HhYnN_G-PKI5Q3t9EltaVzFu-nT70aBE4tSCESDDCQfrBC_VXIRBnDg',
            'x-capability': '{"program_title_differ_with_episode_title": true}',
        }

    @staticmethod
    def get_param(content_id):
        params = {
            'platform': 'web',
            'device_id': '796543ee-4168-470b-853c-22ed07f685c0',
            'limit_resolutions[]': [
                'h264_1080p',
                'h265_1080p',
            ],
            'lookahead': '1',
            'content_id': content_id,
            'user_id': '443019577',
        }
        return params

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    def get_obj(self, item: dict):
        category = item.get('category')
        content_id = item.get('content_id')
        response = requests.get('https://epg-cdn.production-public.tubi.io/content/epg/programming', params=self.get_param(content_id),
                                headers=self.headers)
        rows = response.json().get('rows')[0]
        description_channel = rows.get('description')
        title = rows.get('title')
        content_id = rows.get('content_id')
        m3u8_url = rows.get('video_resources')[0].get('manifest').get('url')
        background_img = rows.get('images').get('background')[0]
        hero_img = rows.get('images').get('hero')[0]
        landscape_img = rows.get('images').get('landscape')[0]
        poster_img = rows.get('images').get('poster')[0]
        thumbnail_img = rows.get('images').get('thumbnail')[0]
        programs = rows.get('programs')
        return {
            "content_id": content_id,
            "title": title,
            "category": category,
            "description_channel": description_channel,
            "m3u8_url": m3u8_url,
            "background_img": background_img,
            "hero_img": hero_img,
            "landscape_img": landscape_img,
            "poster_img": poster_img,
            "thumbnail_img": thumbnail_img,
            "programs": programs,
            "updatetime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        }

    
    def upload_sql(self, data):
        try:
            with Session() as db:
                exist_data = db.query(TUBI).filter_by(content_id=data.get('content_id')).first()
                if exist_data:
                    for key, value in data.items():
                        setattr(exist_data, key, value)
                else:
                    db.add(TUBI(**data))
                db.commit()
                logging.info(f"成功上传/更新 content_id: {data.get('content_id')}")
        except Exception as e:
            db.rollback()
            logging.error(f"Error: {e}, 上传失败content_id: {data.get('content_id')}")

    def get_redis_tasks(self, max_tasks=100):
        tasks = []
        for _ in range(max_tasks):
            task_json = redis_client.lpop('tubitv_ids')
            if not task_json:
                break
            tasks.append(json.loads(task_json))
        return tasks

    async def process_task(self, item, loop):
        try:
            obj = await loop.run_in_executor(executor, self.get_obj, item)
            await loop.run_in_executor(executor, self.upload_sql, obj)
        except Exception as e:
            logging.error(f"Error: {e}, 处理失败content_id: {item.get('content_id')}")

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = self.get_redis_tasks(200)
        if not tasks:
            logging.info("没有任务可处理")
            return
        coros = [self.process_task(item, loop) for item in tasks]
        loop.run_until_complete(asyncio.gather(*coros))

    def upload_mysql(self):
        self.run()


if __name__ == '__main__':
    tubi = Tubi_project()
    schedule.every(2).hours.do(tubi.upload_mysql)
    tubi.upload_mysql()  
    while True:
        schedule.run_pending()
        time.sleep(10)

# print(response.status_code)
# print(response.json().get('rows')[0].get('video_resources')[0]['manifest']['url'])
# with open(path / 'tubi.txt', 'w', encoding='utf-8') as f:
#     f.write(response.text)
