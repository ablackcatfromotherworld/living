# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 创建Base类，用于声明模型
Base = declarative_base()

class GloboSports(Base):
    """Globo Sports数据库模型"""
    __tablename__ = 'globo_sports'
    
    # 主键ID，自动递增
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 从esports.py获取的字段
    titleId = Column(String(50), nullable=False, comment='标题ID')
    headline = Column(String(255), nullable=False, comment='节目标题')
    originProgramId = Column(String(50), nullable=False, comment='原始节目ID')
    slug = Column(String(255), nullable=False, comment='URL slug')
    type = Column(String(50), nullable=False, comment='类型')
    
    # 从get_headline获取的字段
    episode_id = Column(String(50), nullable=True, comment='剧集ID')
    episode_headline = Column(Text, nullable=True, comment='剧集标题')
    
    # 时间戳字段
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def __repr__(self):
        return f"<GloboSports(id={self.id}, titleId='{self.titleId}', headline='{self.headline}')>"
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'titleId': self.titleId,
            'headline': self.headline,
            'originProgramId': self.originProgramId,
            'slug': self.slug,
            'type': self.type,
            'episode_id': self.episode_id,
            'episode_headline': self.episode_headline,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # 'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }