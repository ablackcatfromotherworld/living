import json
import logging
from kafka import KafkaConsumer
from sqlalchemy import create_engine, Table, MetaData, update
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- 配置 ---
# Kafka 配置
KAFKA_BROKERS = ["43.157.156.145:9092"]
KAFKA_TOPIC = 'movies'
KAFKA_GROUP_ID = 'movie_updater_group' # 自定义消费者组ID

# 数据库配置 (请根据您的实际情况修改)
DATABASE_URL = 'mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider' 
DB_TABLE_NAME = 'movies'

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 初始化 ---
# 初始化数据库连接
engine = create_engine(DATABASE_URL)
metadata = MetaData()
movies_table = Table(DB_TABLE_NAME, metadata, autoload_with=engine)
Session = sessionmaker(bind=engine)

def process_messages_batch(messages, session):
    """批量处理Kafka消息并更新数据库"""
    updates = 0
    for message in messages:
        try:
            data = json.loads(message.value.decode('utf-8'))
            movie_id = data.get('id')
            belong_to_id = data.get('belong_to_id')
            belong_to_name = data.get('belong_to_name')

            if not movie_id:
                logging.warning(f"消息中缺少 'id' 字段: {data}")
                continue

            # 准备更新语句
            stmt = (
                update(movies_table)
                .where(movies_table.c.id == movie_id)
                .values(
                    belong_to_id=belong_to_id, 
                    belong_to_name=belong_to_name,
                    update_at=datetime.now() # 更新update_at字段
                )
            )
            session.execute(stmt)
            updates += 1

        except json.JSONDecodeError:
            logging.error(f"无法解析JSON消息: {message.value}")
        except Exception as e:
            logging.error(f"处理消息时发生错误: {e}")

    if updates > 0:
        try:
            session.commit()
            logging.info(f"成功批量更新 {updates} 条记录.")
        except Exception as e:
            logging.error(f"批量提交数据库时发生错误: {e}")
            session.rollback()

def consume_and_update():
    """消费Kafka消息并更新数据库"""
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset='earliest',
        enable_auto_commit=False,  # 关闭自动提交，手动控制
        fetch_max_bytes=1024 * 1024 * 5, # 增加每次拉取的最大字节数
        max_poll_interval_ms=600000  # 10 minutes
        # consumer_timeout_ms=10000 # 移除超时
    )

    logging.info(f"开始从 Kafka topic '{KAFKA_TOPIC}' 消费消息...")
    session = Session()
    try:
        while True:
            batch = []
            # 拉取一批消息
            message_partitions = consumer.poll(timeout_ms=5000, max_records=100) # 最多拉100条，等待5秒
            if not message_partitions:
                logging.info("当前没有新消息，继续等待...")
                continue # 继续循环而不是退出

            for tp, messages in message_partitions.items():
                for message in messages:
                    message_timestamp = message.timestamp
                    message_date = datetime.fromtimestamp(message_timestamp / 1000).date()
                    target_dates = [datetime(2025, 7, 17).date(), datetime(2025, 7, 18).date()]

                    if message_date in target_dates:
                        batch.append(message)

            if batch:
                logging.info(f"处理 {len(batch)} 条目标日期的消息...")
                process_messages_batch(batch, session)
                consumer.commit() # 处理完一批后手动提交offset

    except KeyboardInterrupt:
        logging.info("停止消费者...")
    finally:
        consumer.close()
        session.close()
        logging.info("消费者和数据库会话已关闭.")

if __name__ == "__main__":
    consume_and_update()