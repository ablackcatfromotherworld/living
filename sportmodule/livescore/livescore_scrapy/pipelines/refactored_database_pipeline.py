# -*- coding: utf-8 -*-
"""
Livescore重构后的数据库管道
用于将爬取的数据保存到重构后的MySQL数据库
"""

import logging
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from items import LivescoreItem, TeamItem

# 定义数据库模型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, ForeignKey

Base = declarative_base()

class Country(Base):
    """国家模型"""
    __tablename__ = 'countries'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    language = Column(String(10), nullable=False, comment='语言类型')
    name = Column(String(100), nullable=False, comment='国家名称')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

class League(Base):
    """联赛模型"""
    __tablename__ = 'leagues'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    language = Column(String(10), nullable=False, comment='语言类型')
    name = Column(String(200), nullable=False, comment='联赛名称')
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False, comment='国家ID')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

class Team(Base):
    """队伍模型"""
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    team_id = Column(String(100), nullable=False, comment='队伍ID')
    team_name = Column(String(200), nullable=False, comment='队伍名称')
    team_img = Column(Text, comment='队伍图片URL')
    sport = Column(String(50), nullable=False, comment='运动类型')
    language = Column(String(10), nullable=False, comment='语言类型')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

class Match(Base):
    """比赛模型"""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    match_id = Column(String(100), nullable=False, comment='比赛ID')
    sport = Column(String(50), nullable=False, comment='运动类型')
    date = Column(String(20), nullable=False, comment='比赛日期')
    time_full = Column(BigInteger, comment='比赛时间戳(Unix时间戳)')
    esd_timestamp = Column(String(20), comment='原始Esd时间戳')
    language = Column(String(10), nullable=False, comment='语言')
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False, comment='联赛ID')
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False, comment='国家ID')
    season_id = Column(String(50), comment='赛季ID')
    team1_id = Column(String(255), nullable=False, comment='主队ID')
    team2_id = Column(String(255), nullable=False, comment='客队ID')
    score1 = Column(String(10), comment='主队得分')
    score2 = Column(String(10), comment='客队得分')
    status = Column(Integer, comment='比赛状态ID')
    round_info = Column(String(100), comment='轮次信息')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class RefactoredDatabasePipeline:
    """重构后的数据库管道类"""
    
    def __init__(self, database_url=None):
        self.database_url = database_url
        self.engine = None
        self.Session = None
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # 缓存字典，避免重复查询
        self.country_cache = {}  # {(language, name): id}
        self.league_cache = {}   # {(language, name, country_id): id}
        
        # 统计信息
        self.teams_processed = 0
        self.teams_inserted = 0
        self.teams_updated = 0
        self.matches_processed = 0
        self.matches_inserted = 0
        self.matches_updated = 0
        self.countries_inserted = 0
        self.leagues_inserted = 0
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
            
            # 预加载缓存
            self._load_cache()
            
            self.logger.info("重构后数据库连接成功")
            
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            raise
    
    def _load_cache(self):
        """预加载国家和联赛缓存"""
        try:
            # 加载国家缓存
            countries = self.session.query(Country).all()
            for country in countries:
                key = (country.language, country.name)
                self.country_cache[key] = country.id
            
            # 加载联赛缓存
            leagues = self.session.query(League).all()
            for league in leagues:
                key = (league.language, league.name, league.country_id)
                self.league_cache[key] = league.id
            
            self.logger.info(f"缓存加载完成: {len(self.country_cache)} 个国家, {len(self.league_cache)} 个联赛")
            
        except Exception as e:
            self.logger.error(f"加载缓存失败: {e}")
    
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
        self.logger.info("=== 重构后数据处理统计 ===")
        self.logger.info(f"国家插入: {self.countries_inserted} 条")
        self.logger.info(f"联赛插入: {self.leagues_inserted} 条")
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
    
    def _get_or_create_country(self, country_name, language):
        """获取或创建国家记录"""
        if not country_name:
            return None
        
        cache_key = (language, country_name)
        
        # 先从缓存查找
        if cache_key in self.country_cache:
            return self.country_cache[cache_key]
        
        # 从数据库查找
        country = self.session.query(Country).filter_by(
            language=language,
            name=country_name
        ).first()
        
        if country:
            self.country_cache[cache_key] = country.id
            return country.id
        
        # 创建新国家
        new_country = Country(
            language=language,
            name=country_name
        )
        self.session.add(new_country)
        self.session.flush()  # 获取ID
        
        self.country_cache[cache_key] = new_country.id
        self.countries_inserted += 1
        self.logger.debug(f"创建新国家: {country_name} (语言: {language})")
        
        return new_country.id
    
    def _get_or_create_league(self, league_name, country_id, language):
        """获取或创建联赛记录"""
        if not league_name or not country_id:
            return None
        
        cache_key = (language, league_name, country_id)
        
        # 先从缓存查找
        if cache_key in self.league_cache:
            return self.league_cache[cache_key]
        
        # 从数据库查找
        league = self.session.query(League).filter_by(
            language=language,
            name=league_name,
            country_id=country_id
        ).first()
        
        if league:
            self.league_cache[cache_key] = league.id
            return league.id
        
        # 创建新联赛
        new_league = League(
            language=language,
            name=league_name,
            country_id=country_id
        )
        self.session.add(new_league)
        self.session.flush()  # 获取ID
        
        self.league_cache[cache_key] = new_league.id
        self.leagues_inserted += 1
        self.logger.debug(f"创建新联赛: {league_name} (国家ID: {country_id}, 语言: {language})")
        
        return new_league.id
    
    def _process_team_item(self, item, spider):
        """处理队伍item"""
        try:
            self.teams_processed += 1
            
            # 验证必填字段
            if not item.get('team_id') or not item.get('team_name'):
                self.logger.warning(f"队伍item缺少必填字段: {dict(item)}")
                return item
            
            language = item.get('language', 'en')
            
            # 检查队伍是否已存在
            existing_team = self.session.query(Team).filter_by(
                team_id=item['team_id'],
                language=language
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
                    sport=item.get('sport', ''),
                    language=language
                )
                self.session.add(new_team)
                self.teams_inserted += 1
                self.logger.debug(f"插入新队伍: {item['team_name']} (ID: {item['team_id']})")
            
            # 每10条记录提交一次
            if self.teams_processed % 10 == 0:
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
            
            language = item.get('language', 'en')
            
            # 获取或创建国家和联赛ID
            country_id = self._get_or_create_country(item.get('country'), language)
            league_id = self._get_or_create_league(item.get('league'), country_id, language)
            
            # 检查比赛是否已存在
            existing_match = self.session.query(Match).filter_by(
                match_id=item['match_id'],
                language=language
            ).first()
            
            if existing_match:
                # 更新现有比赛
                self._update_match(existing_match, item, country_id, league_id)
                self.matches_updated += 1
                self.logger.debug(f"更新比赛: {item.get('team1', '')} vs {item.get('team2', '')} (ID: {item['match_id']})")
            else:
                # 插入新比赛
                new_match = self._create_match(item, country_id, league_id)
                self.session.add(new_match)
                self.matches_inserted += 1
                self.logger.debug(f"插入新比赛: {item.get('team1', '')} vs {item.get('team2', '')} (ID: {item['match_id']})")
            
            # 每10条记录提交一次
            if self.matches_processed % 10 == 0:
                self.session.commit()
                self.logger.info(f"已处理 {self.matches_processed} 个比赛")
            
            return item
        
        except IntegrityError as e:
            self.session.rollback()
            self.logger.warning(f"比赛数据完整性错误: {e}")
            return item
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"处理比赛item时出错: {e}")
            raise
    
    def _create_match(self, item, country_id, league_id):
        """创建新的比赛记录"""
        return Match(
            match_id=item['match_id'],
            sport=item.get('sport', ''),
            date=item.get('date', ''),
            time_full=item.get('time_full'),  # Unix时间戳
            esd_timestamp=item.get('esd_timestamp', ''),
            language=item.get('language', ''),
            league_id=league_id,
            country_id=country_id,
            season_id=item.get('season_id', ''),
            team1_id=item.get('team1_id', ''),
            team2_id=item.get('team2_id', ''),
            score1=item.get('score1', ''),
            score2=item.get('score2', ''),
            status=item.get('status'),  # 状态ID
            round_info=item.get('round_info', '')
        )
    
    def _update_match(self, match, item, country_id, league_id):
        """更新现有的比赛记录"""
        match.sport = item.get('sport', match.sport)
        match.date = item.get('date', match.date)
        match.time_full = item.get('time_full', match.time_full)
        match.esd_timestamp = item.get('esd_timestamp', match.esd_timestamp)
        match.league_id = league_id or match.league_id
        match.country_id = country_id or match.country_id
        match.season_id = item.get('season_id', match.season_id)
        match.team1_id = item.get('team1_id', match.team1_id)
        match.team2_id = item.get('team2_id', match.team2_id)
        match.score1 = item.get('score1', match.score1)
        match.score2 = item.get('score2', match.score2)
        match.status = item.get('status', match.status)
        match.round_info = item.get('round_info', match.round_info)
        match.updated_at = datetime.now()