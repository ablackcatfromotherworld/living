import json
import time
import asyncio
import schedule
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Text, inspect, DateTime

from sqlalchemy.orm import sessionmaker, declarative_base
import logging
from fetch_m3u8_urls import M3U8Fetcher

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
    update_time = Column(DateTime)

def create_table_if_not_exists():
    """
    检查GloboSeries表是否存在，如果不存在则创建
    """
    try:
        # 使用inspect检查表是否存在
        inspector = inspect(engine)
        if not inspector.has_table('globo_series'):
            logging.info("GloboSeries表不存在，正在创建...")
            Base.metadata.create_all(bind=engine)
            logging.info("GloboSeries表创建成功")
        else:
            logging.info("GloboSeries表已存在")
    except Exception as e:
        logging.error(f"创建表时出错: {e}")
        # 如果检查失败，尝试直接创建（SQLAlchemy会忽略已存在的表）
        Base.metadata.create_all(bind=engine)

# 创建表（如果不存在）
create_table_if_not_exists()

async def fetch_and_upload_m3u8_data():
    """
    获取m3u8数据并上传到数据库
    """
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"开始获取m3u8数据 - {current_time}")
        
        # 创建M3U8Fetcher实例
        fetcher = M3U8Fetcher()
        
        # 获取所有m3u8链接
        results = await fetcher.fetch_all_m3u8_urls()
        
        if not results:
            logging.warning("没有获取到任何m3u8数据")
            return False
        
        # 加载graphql.json数据以获取完整的媒体信息
        graphql_data = fetcher.load_graphql_data()
        
        # 创建媒体ID到完整信息的映射
        media_info_map = {}
        for item in graphql_data:
            without_dvr_id = item.get('withoutDVRMediaId')
            if without_dvr_id:
                media_info_map[without_dvr_id] = item
        
        success_count = 0
        total_count = len(results)
        
        # 处理每个结果
        for result in results:
            try:
                # 从结果中提取媒体ID和m3u8链接
                name = result.get('name', 'Unknown')
                m3u8_url = None
                without_dvr_media_id = None
                
                for key, value in result.items():
                    if key != 'name':
                        without_dvr_media_id = key
                        m3u8_url = value
                        break
                
                if not without_dvr_media_id or not m3u8_url:
                    logging.warning(f"跳过无效数据: {result}")
                    continue
                
                # 从graphql数据中获取完整信息
                media_info = media_info_map.get(without_dvr_media_id, {})
                
                # 构建数据库记录
                db_data = {
                    'mediaId': media_info.get('mediaId', without_dvr_media_id),
                    'name': name,
                    'description': media_info.get('description', ''),
                    'img_cover': media_info.get('img_cover', ''),
                    'withoutDVRMediaId': without_dvr_media_id,
                    'slug': media_info.get('slug', ''),
                    'channel_ref': media_info.get('channel_ref', ''),
                    'categories': media_info.get('categories', ''),
                    'subscriptionServices_id': media_info.get('subscriptionServices_id', ''),
                    'm3u8_url': m3u8_url,
                    'update_time': datetime.now()
                }
                
                # 上传到数据库
                if upload_data_with_retry(db_data):
                    success_count += 1
                    logging.info(f"成功上传: {name} ({without_dvr_media_id})")
                else:
                    logging.error(f"上传失败: {name} ({without_dvr_media_id})")
                    
            except Exception as e:
                logging.error(f"处理数据时出错: {e}, 数据: {result}")
                continue
        
        logging.info(f"数据上传完成 - 成功: {success_count}/{total_count}")
        return success_count > 0
        
    except Exception as e:
        logging.error(f"获取和上传m3u8数据时出错: {e}")
        return False

def run_daily_update():
    """
    运行每日更新任务的包装函数
    """
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"开始执行每日更新任务 - {current_time}")
        
        # 运行异步任务
        success = asyncio.run(fetch_and_upload_m3u8_data())
        
        if success:
            logging.info(f"每日更新任务完成 - {current_time}")
        else:
            logging.error(f"每日更新任务失败 - {current_time}")
            
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"每日更新任务执行异常 - {current_time}: {e}")

def start_daily_scheduler():
    """
    启动每日定时任务
    """
    logging.info("启动每日更新定时任务")
    logging.info("定时任务设置: 每天0点和12点自动执行")
    
    # 设置定时任务
    schedule.every().day.at("00:00").do(run_daily_update)
    schedule.every().day.at("12:00").do(run_daily_update)
    
    # 首次执行
    logging.info("执行首次更新任务...")
    run_daily_update()
    
    logging.info("定时任务已启动，等待下次执行时间...")
    logging.info("下次执行时间: 每天 00:00 和 12:00")
    logging.info("按 Ctrl+C 退出程序")
    
    # 持续运行定时任务
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logging.info("程序已停止")
        print("程序已停止")

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
    # 启动每日定时任务
    start_daily_scheduler()