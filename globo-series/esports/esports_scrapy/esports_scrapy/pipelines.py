# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import GloboSports
from .database_config import Config

logger = logging.getLogger(__name__)

class GloboSportsPipeline:
    """
    Scrapy Pipeline for Globo Sports data
    实现数据插入、更新和去重功能
    """
    
    def __init__(self):
        self.engine = None
        self.session = None
        self.Session = None
        
    def open_spider(self, spider):
        """
        Spider启动时初始化数据库连接
        """
        try:
            # 使用MySQL配置
            database_url = Config.get_database_url('mysql')
            self.engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # 设置为True可以看到SQL语句
            )
            
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            
            logger.info(f"数据库连接成功: {Config.MYSQL['host']}:{Config.MYSQL['port']}/{Config.MYSQL['db']}")
            
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
            
    def close_spider(self, spider):
        """
        Spider结束时关闭数据库连接
        """
        if self.session:
            self.session.close()
            logger.info("数据库连接已关闭")
    
    def process_item(self, item, spider):
        """
        处理爬取到的数据项
        实现插入或更新逻辑
        """
        try:
            # 添加爬取时间
            if 'created_at' not in item or not item['created_at']:
                item['created_at'] = datetime.now()
                
            # 查询是否已存在该记录
            existing_record = self.session.query(GloboSports).filter_by(
                episode_id=item.get('episode_id')
            ).first()
            
            if existing_record:
                # 更新已存在的记录
                # for key, value in item.items():
                #     if value is not None:  # 只更新非空值
                #         setattr(existing_record, key, value)
                # item['updated_at'] = datetime.now()
                # self.session.merge(existing_record)
                # logger.info(f"更新记录: {item.get('episode_id')} - {item.get('episode_headline')}")
                logger.info(f'跳过已经有的记录: {item.get('episode_id')} - {item.get('episode_headline')}')
            else:
                # 创建新记录
                new_record = GloboSports(**item)
                self.session.add(new_record)
                logger.info(f"新增记录: {item.get('episode_id')} - {item.get('episode_headline')}")
            
            # 提交事务
            self.session.commit()
            
        except SQLAlchemyError as e:
            # 回滚事务
            self.session.rollback()
            logger.error(f"数据库错误: {e}")
            
        except Exception as e:
            logger.error(f"处理数据项时出错: {e}")
            
        return item

