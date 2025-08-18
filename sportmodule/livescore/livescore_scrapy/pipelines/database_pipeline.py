# -*- coding: utf-8 -*-
"""
Livescore数据库管道
用于将爬取的数据保存到MySQL数据库
"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from items import LivescoreItem, TeamItem

# 定义数据库模型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text

Base = declarative_base()

class Team(Base):
    """队伍模型"""
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    team_id = Column(String(100), nullable=False, comment='队伍ID')
    team_name = Column(String(200), nullable=False, comment='队伍名称')
    team_img = Column(Text, comment='队伍图片URL')
    sport = Column(String(50), nullable=False, comment='运动类型')
    created_at = Column(DateTime, comment='创建时间')
    updated_at = Column(DateTime, comment='更新时间')

class Match(Base):
    """比赛模型"""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    match_id = Column(String(100), nullable=False, comment='比赛ID')
    sport = Column(String(50), nullable=False, comment='运动类型')
    date = Column(String(20), nullable=False, comment='比赛日期')
    time_full = Column(String(50), comment='比赛时间')
    timestamp = Column(String(20), comment='时间戳')
    language = Column(String(10), nullable=False, comment='语言')
    league = Column(String(200), comment='联赛名称')
    country = Column(String(100), comment='国家')
    team1_id = Column(String(255), nullable=False, comment='主队ID')
    team2_id = Column(String(255), nullable=False, comment='客队ID')
    score1 = Column(String(10), comment='主队得分')
    score2 = Column(String(10), comment='客队得分')
    status = Column(String(50), comment='比赛状态')
    created_at = Column(DateTime, comment='创建时间')
    updated_at = Column(DateTime, comment='更新时间')


class DatabasePipeline:
    """数据库管道类"""
    
    def __init__(self, database_url=None):
        self.database_url = database_url
        self.engine = None
        self.Session = None
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # 统计信息
        self.teams_processed = 0
        self.teams_inserted = 0
        self.teams_updated = 0
        self.matches_processed = 0
        self.matches_inserted = 0
        self.matches_updated = 0
        self.errors = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        database_url = crawler.settings.get('DATABASE_URL')
        return cls(database_url=database_url)
    
    def open_spider(self, spider):
        """爬虫开始时的初始化"""
        try:
            # 如果没有提供数据库URL，使用默认配置
            if not self.database_url:
                self.database_url = 'mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider'
            
            # 创建数据库引擎
            self.engine = create_engine(
                self.database_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={
                    'charset': 'utf8mb4',
                    'connect_timeout': 60,
                    'read_timeout': 60,
                    'write_timeout': 60
                }
            )
            
            # 测试连接
            with self.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            
            self.logger.info("数据库连接成功")
            
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            raise
    
    def close_spider(self, spider):
        """爬虫结束时的清理"""
        if self.session:
            try:
                self.session.commit()
                self.session.close()
                self.logger.info("数据库会话已关闭")
            except Exception as e:
                self.logger.error(f"关闭数据库会话时出错: {e}")
        
        # 打印统计信息
        self.logger.info("=== 数据处理统计 ===")
        self.logger.info(f"队伍处理: {self.teams_processed} 条")
        self.logger.info(f"队伍插入: {self.teams_inserted} 条")
        self.logger.info(f"队伍更新: {self.teams_updated} 条")
        self.logger.info(f"比赛处理: {self.matches_processed} 条")
        self.logger.info(f"比赛插入: {self.matches_inserted} 条")
        self.logger.info(f"比赛更新: {self.matches_updated} 条")
        self.logger.info(f"错误数量: {self.errors} 条")
    
    def process_item(self, item, spider):
        """处理单个item"""
        try:
            if isinstance(item, TeamItem):
                return self._process_team_item(item, spider)
            elif isinstance(item, LivescoreItem):
                return self._process_match_item(item, spider)
            else:
                self.logger.warning(f"未知的item类型: {type(item)}")
                return item
        
        except Exception as e:
            self.errors += 1
            self.logger.error(f"处理item时出错: {e}")
            return item
    
    def _process_team_item(self, item, spider):
        """处理队伍item"""
        try:
            self.teams_processed += 1
            
            # 验证必填字段
            if not item.get('team_id') or not item.get('team_name'):
                self.logger.warning(f"队伍item缺少必填字段: {dict(item)}")
                return item
            
            # 检查队伍是否已存在
            existing_team = self.session.query(Team).filter_by(
                team_id=item['team_id']
            ).first()
            
            if existing_team:
                # 更新现有队伍
                existing_team.team_name = item['team_name']
                existing_team.team_img = item.get('team_img', '')
                existing_team.sport = item.get('sport', '')
                existing_team.updated_at = datetime.now()
                self.teams_updated += 1
                self.logger.debug(f"更新队伍: {item['team_name']} (ID: {item['team_id']})")
            else:
                # 插入新队伍
                new_team = Team(
                    team_id=item['team_id'],
                    team_name=item['team_name'],
                    team_img=item.get('team_img', ''),
                    sport=item.get('sport', '')
                )
                self.session.add(new_team)
                self.teams_inserted += 1
                self.logger.debug(f"插入新队伍: {item['team_name']} (ID: {item['team_id']})")
            
            # 每100条记录提交一次
            if self.teams_processed % 100 == 0:
                self.session.commit()
                self.logger.info(f"已处理 {self.teams_processed} 个队伍")
            
            return item
        
        except IntegrityError as e:
            self.session.rollback()
            self.logger.warning(f"队伍数据完整性错误: {e}")
            return item
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"处理队伍item时出错: {e}")
            raise
    
    def _process_match_item(self, item, spider):
        """处理比赛item"""
        try:
            self.matches_processed += 1
            
            # 验证必填字段
            if not item.get('match_id'):
                self.logger.warning(f"比赛item缺少match_id: {dict(item)}")
                return item
            
            # 检查比赛是否已存在
            existing_match = self.session.query(Match).filter_by(
                match_id=item['match_id'],
                language=item.get('language', '')
            ).first()
            
            if existing_match:
                # 更新现有比赛
                self._update_match(existing_match, item)
                self.matches_updated += 1
                self.logger.debug(f"更新比赛: {item.get('team1', '')} vs {item.get('team2', '')} (ID: {item['match_id']})")
            else:
                # 插入新比赛
                new_match = self._create_match(item)
                self.session.add(new_match)
                self.matches_inserted += 1
                self.logger.debug(f"插入新比赛: {item.get('team1', '')} vs {item.get('team2', '')} (ID: {item['match_id']})")
            
            # 每100条记录提交一次
            if self.matches_processed % 100 == 0:
                self.session.commit()
                self.logger.info(f"已处理 {self.matches_processed} 场比赛")
            
            return item
        
        except IntegrityError as e:
            self.session.rollback()
            self.logger.warning(f"比赛数据完整性错误: {e}")
            return item
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"处理比赛item时出错: {e}")
            raise
    
    def _create_match(self, item):
        """创建新的比赛记录"""
        return Match(
            match_id=item['match_id'],
            sport=item.get('sport', ''),
            date=item.get('date', ''),
            time_full=item.get('time_full', ''),
            timestamp=item.get('timestamp', ''),
            language=item.get('language', ''),
            league=item.get('league', ''),
            country=item.get('country', ''),
            team1_id=item.get('team1_id', ''),
            team2_id=item.get('team2_id', ''),
            score1=item.get('score1', ''),
            score2=item.get('score2', ''),
            status=item.get('status', '')
        )
    
    def _update_match(self, match, item):
        """更新现有的比赛记录"""
        match.sport = item.get('sport', match.sport)
        match.date = item.get('date', match.date)
        match.time_full = item.get('time_full', match.time_full)
        match.timestamp = item.get('timestamp', match.timestamp)
        match.league = item.get('league', match.league)
        match.country = item.get('country', match.country)
        match.team1_id = item.get('team1_id', match.team1_id)
        match.team2_id = item.get('team2_id', match.team2_id)
        match.score1 = item.get('score1', match.score1)
        match.score2 = item.get('score2', match.score2)
        match.status = item.get('status', match.status)
        match.updated_at = datetime.now()


class JsonPipeline:
    """JSON文件输出管道"""
    
    def __init__(self):
        self.teams_file = None
        self.matches_file = None
        self.teams_data = []
        self.matches_data = []
    
    def open_spider(self, spider):
        """爬虫开始时打开文件"""
        import json
        self.teams_file = open('teams_output.json', 'w', encoding='utf-8')
        self.matches_file = open('matches_output.json', 'w', encoding='utf-8')
    
    def close_spider(self, spider):
        """爬虫结束时保存数据并关闭文件"""
        import json
        
        # 保存队伍数据
        json.dump(self.teams_data, self.teams_file, ensure_ascii=False, indent=2)
        self.teams_file.close()
        
        # 保存比赛数据
        json.dump(self.matches_data, self.matches_file, ensure_ascii=False, indent=2)
        self.matches_file.close()
        
        logging.info(f"已保存 {len(self.teams_data)} 个队伍和 {len(self.matches_data)} 场比赛到JSON文件")
    
    def process_item(self, item, spider):
        """处理item"""
        if isinstance(item, TeamItem):
            self.teams_data.append(dict(item))
        elif isinstance(item, LivescoreItem):
            self.matches_data.append(dict(item))
        
        return item