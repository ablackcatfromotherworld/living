# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from items import TeamItem, LivescoreItem
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
    round_info = Column(String(100), comment='轮次/阶段信息')
    created_at = Column(DateTime, comment='创建时间')
    updated_at = Column(DateTime, comment='更新时间')

# 配置日志
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'username': 'spiderman',
    'password': 'ew4%2598fRpe',  # URL编码后的密码
    'host': '43.157.134.155',
    'port': '33070',
    'database': 'spider'
}

# 创建数据库连接字符串
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


class DuplicateFilterPipeline:
    """去重管道"""
    
    def __init__(self):
        self.teams_seen = set()
        self.matches_seen = set()
    
    def process_item(self, item, spider):
        if isinstance(item, TeamItem):
            team_key = f"{item['team_id']}_{item['sport']}"
            if team_key in self.teams_seen:
                logger.debug(f"重复队伍已过滤: {item['team_name']}")
                return None
            else:
                self.teams_seen.add(team_key)
                return item
        
        elif isinstance(item, LivescoreItem):
            match_key = f"{item['match_id']}_{item['language']}"
            if match_key in self.matches_seen:
                logger.debug(f"重复比赛已过滤: {item['match_id']}")
                return None
            else:
                self.matches_seen.add(match_key)
                return item
        
        return item


class DatabasePipeline:
    """数据库存储管道"""
    
    def __init__(self, database_url=DATABASE_URL):
        self.database_url = database_url
        self.engine = None
        self.Session = None
        self.session = None
        
        # 统计计数器
        self.teams_inserted = 0
        self.teams_updated = 0
        self.matches_inserted = 0
        self.matches_updated = 0
        self.errors = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        """从crawler获取配置"""
        return cls(
            database_url=crawler.settings.get('DATABASE_URL', DATABASE_URL)
        )
    
    def open_spider(self, spider):
        """爬虫开始时的初始化"""
        try:
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
            
            logger.info("数据库连接成功")
            
        except SQLAlchemyError as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def close_spider(self, spider):
        """爬虫结束时的清理"""
        if self.session:
            self.session.close()
        
        # 输出统计信息
        logger.info(f"数据处理完成 - 队伍: 新增{self.teams_inserted}个, 更新{self.teams_updated}个")
        logger.info(f"数据处理完成 - 比赛: 新增{self.matches_inserted}场, 更新{self.matches_updated}场")
        if self.errors > 0:
            logger.warning(f"处理过程中发生 {self.errors} 个错误")
    
    def process_item(self, item, spider):
        """处理单个item"""
        if item is None:
            return None
        
        try:
            if isinstance(item, TeamItem):
                self._process_team_item(item)
            elif isinstance(item, LivescoreItem):
                self._process_match_item(item)
            
            return item
        
        except Exception as e:
            self.errors += 1
            logger.error(f"处理item时出错: {e}")
            return item
    
    def _process_team_item(self, item):
        """处理队伍item"""
        try:
            # 检查队伍是否已存在
            existing_team = self.session.query(Team).filter(
                Team.team_id == item['team_id'],
                Team.sport == item['sport']
            ).first()
            
            if existing_team:
                # 更新现有队伍信息
                existing_team.team_name = item['team_name']
                existing_team.team_img = item.get('team_img', '')
                existing_team.updated_at = datetime.now()
                self.teams_updated += 1
                logger.debug(f"更新队伍: {item['team_name']}")
            else:
                # 创建新队伍
                new_team = Team(
                    team_id=item['team_id'],
                    team_name=item['team_name'],
                    team_img=item.get('team_img', ''),
                    sport=item['sport']
                )
                self.session.add(new_team)
                self.teams_inserted += 1
                logger.debug(f"新增队伍: {item['team_name']}")
            
            self.session.commit()
        
        except IntegrityError as e:
            self.session.rollback()
            logger.warning(f"队伍数据完整性错误: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"队伍数据库操作失败: {e}")
            raise
    
    def _process_match_item(self, item):
        """处理比赛item"""
        try:
            # 检查比赛是否已存在
            existing_match = self.session.query(Match).filter(
                Match.match_id == item['match_id'],
                Match.language == item['language']
            ).first()
            
            if existing_match:
                # 更新现有比赛信息
                existing_match.score1 = item.get('score1', '')
                existing_match.score2 = item.get('score2', '')
                existing_match.status = item.get('status', '')
                existing_match.round_info = item.get('round_info', '')
                existing_match.updated_at = datetime.now()
                self.matches_updated += 1
                logger.debug(f"更新比赛: {item['match_id']}")
            else:
                # 创建新比赛
                new_match = Match(
                    match_id=item['match_id'],
                    sport=item['sport'],
                    date=item['date'],
                    time_full=item.get('time_full', ''),
                    timestamp=item.get('timestamp', ''),
                    language=item['language'],
                    league=item.get('league', ''),
                    country=item.get('country', ''),
                    team1_id=item['team1_id'],
                    team2_id=item['team2_id'],
                    score1=item.get('score1', ''),
                    score2=item.get('score2', ''),
                    status=item.get('status', ''),
                    round_info=item.get('round_info', '')
                )
                self.session.add(new_match)
                self.matches_inserted += 1
                logger.debug(f"新增比赛: {item['match_id']}")
            
            self.session.commit()
        
        except IntegrityError as e:
            self.session.rollback()
            logger.warning(f"比赛数据完整性错误: {e}")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"比赛数据库操作失败: {e}")
            raise


class ValidationPipeline:
    """数据验证管道"""
    
    def process_item(self, item, spider):
        """验证item数据"""
        if isinstance(item, TeamItem):
            # 验证队伍必填字段
            if not item.get('team_id'):
                logger.warning("队伍缺少team_id字段，跳过")
                return None
            
            if not item.get('team_name'):
                logger.warning(f"队伍 {item.get('team_id')} 缺少team_name字段，跳过")
                return None
            
            if not item.get('sport'):
                logger.warning(f"队伍 {item.get('team_id')} 缺少sport字段，跳过")
                return None
        
        elif isinstance(item, MatchItem):
            # 验证比赛必填字段
            if not item.get('match_id'):
                logger.warning("比赛缺少match_id字段，跳过")
                return None
            
            if not item.get('sport'):
                logger.warning(f"比赛 {item.get('match_id')} 缺少sport字段，跳过")
                return None
            
            if not item.get('team1_id') or not item.get('team2_id'):
                logger.warning(f"比赛 {item.get('match_id')} 缺少队伍ID字段，跳过")
                return None
            
            if not item.get('language'):
                logger.warning(f"比赛 {item.get('match_id')} 缺少language字段，跳过")
                return None
        
        return item


class LoggingPipeline:
    """日志记录管道"""
    
    def __init__(self):
        self.items_processed = 0
        self.teams_processed = 0
        self.matches_processed = 0
    
    def process_item(self, item, spider):
        """记录处理日志"""
        if item is None:
            return None
        
        self.items_processed += 1
        
        if isinstance(item, TeamItem):
            self.teams_processed += 1
            if self.teams_processed % 100 == 0:
                logger.info(f"已处理 {self.teams_processed} 个队伍")
        
        elif isinstance(item, MatchItem):
            self.matches_processed += 1
            if self.matches_processed % 100 == 0:
                logger.info(f"已处理 {self.matches_processed} 场比赛")
        
        return item
    
    def close_spider(self, spider):
        """爬虫结束时输出总计"""
        logger.info(f"处理完成 - 总计: {self.items_processed} 个items")
        logger.info(f"处理完成 - 队伍: {self.teams_processed} 个")
        logger.info(f"处理完成 - 比赛: {self.matches_processed} 场")