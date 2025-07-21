import json
import time
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义数据库连接信息
DATABASE_URL = 'mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider'

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 定义数据模型
class GloboSeries(Base):
    __tablename__ = 'globo_series'
    mediaId = Column(String(255), primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    img_cover = Column(Text)
    withoutDVRMediaId = Column(String(255))
    slug = Column(String(255))
    channel_ref = Column(String(255))
    categories = Column(String(255))
    subscriptionServices_id = Column(String(255))
    m3u8_url = Column(Text)

# 创建表
Base.metadata.create_all(bind=engine)

def upload_data_with_retry(data, max_retries=3, delay=5):
    """
    上传数据到数据库，包含重试机制。
    """
    session = SessionLocal()
    for attempt in range(max_retries):
        try:
            # 检查数据是否存在
            existing_data = session.query(GloboSeries).filter_by(mediaId=data['mediaId']).first()
            if existing_data:
                # 更新数据
                for key, value in data.items():
                    setattr(existing_data, key, value)
                logging.info(f"Data with mediaId {data['mediaId']} updated.")
            else:
                # 插入新数据
                new_data = GloboSeries(**data)
                session.add(new_data)
                logging.info(f"Data with mediaId {data['mediaId']} inserted.")
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Upload failed.")
                return False
        finally:
            session.close()

if __name__ == "__main__":
    # 示例数据
    json_data = {
        "mediaId": "6120663",
        "name": "TV Globo",
        "description": "No Globoplay você assiste TV Globo AO VIVO! Acesse e confira todos os momentos.",
        "img_cover": "https://s2-globo-play.glbimg.com/nildGxwNq34FLeuTmpQRkuUSqJw=/0x1080/filters:quality(100)/https://s2-globo-play.glbimg.com/OF6daFOhVvEvHb7AdN-kH6p_p7U=/https://i.s3.glbimg.com/v1/AUTH_c3c606ff68e7478091d1ca496f9c5625/internal_photos/bs/2025/W/1/UcDY3aRai72ZeAw8Nyjw/2025-4786-tvg-60-anos-alternativa-on-air.jpg",
        "withoutDVRMediaId": "4452349",
        "slug": "tv-globo",
        "channel_ref": "196",
        "categories": "gratuitos",
        "subscriptionServices_id": "",
        "m3u8_url": "http://example.com/stream.m3u8"  # 示例 m3u8 地址
    }

    # 上传数据
    upload_data_with_retry(json_data)