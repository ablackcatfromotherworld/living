import redis
import json
import logging
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Float, ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
base = declarative_base()
engine = create_engine('mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider')
Session = sessionmaker(bind=engine)

redis_client = redis.from_url('redis://:wnhmsy@43.157.146.240:6379/15')
pipe = redis_client.pipeline()

class CXTV_live_streaming(base):

    __tablename__ = 'cxtv_live_streaming'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    areas = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    profile = Column(Text, nullable=False)
    country_img = Column(Text, nullable=False)
    img_cover = Column(Text, nullable=False)
    m3u8_url = Column(Text, nullable=False)
    codec_name = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    variant_bitrate = Column(BigInteger, nullable=False)

class CXTV_img(base):

    __tablename__ = 'cxtv_img'

    img_id = Column(Integer, primary_key=True, autoincrement=True)
    cxtv_id = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    storage = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)


with Session() as db:
    cxtv_imgs = db.query(CXTV_img.img_id, CXTV_img.cxtv_id, CXTV_img.url, CXTV_img.storage).where(CXTV_img.status == 0)
    index = 0
    for cxtv_img in cxtv_imgs:
        pipe.lpush('cxtv_img', json.dumps({
            'img_id':cxtv_img.img_id,
            'cxtv_id': cxtv_img.cxtv_id,
            'url': cxtv_img.url,
            'storage': cxtv_img.storage,
        }))
        index += 1
        logging.info(f"正在处理第{index}个")
        if index % 100 == 0:
            index = 0
            pipe.execute()
    pipe.execute()