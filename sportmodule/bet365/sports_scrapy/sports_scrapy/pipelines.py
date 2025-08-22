# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

from typing import Dict, Any

from .items import (
    SportItem, CountryItem, LeagueItem, TeamItem, 
    SeasonItem, MatchItem
)

# 导入数据库表模型
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from create_tables_sqlalchemy import Sports, Countries, Leagues, Teams, Seasons, Matches


class ValidationPipeline:
    """数据验证管道"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # 验证必需字段
        if isinstance(item, SportItem):
            if not adapter.get('sport_id') or not adapter.get('sport_name'):
                raise ValueError(f"Sport item missing required fields: {dict(adapter)}")
        
        elif isinstance(item, CountryItem):
            if not adapter.get('country_id') or not adapter.get('country_name'):
                raise ValueError(f"Country item missing required fields: {dict(adapter)}")
        
        elif isinstance(item, LeagueItem):
            if not adapter.get('league_id') or not adapter.get('league_name'):
                raise ValueError(f"League item missing required fields: {dict(adapter)}")
        
        elif isinstance(item, TeamItem):
            if not adapter.get('team_id') or not adapter.get('team_name'):
                raise ValueError(f"Team item missing required fields: {dict(adapter)}")
        
        elif isinstance(item, SeasonItem):
            if not adapter.get('season_id') or not adapter.get('season_name'):
                raise ValueError(f"Season item missing required fields: {dict(adapter)}")
        
        elif isinstance(item, MatchItem):
            if not adapter.get('match_id'):
                raise ValueError(f"Match item missing required fields: {dict(adapter)}")
        
        # 添加时间戳
        current_time = datetime.now()
        if not adapter.get('created_at'):
            adapter['created_at'] = current_time
        if not adapter.get('updated_at'):
            adapter['updated_at'] = current_time
        
        # 设置默认语言代码
        if not adapter.get('language_code'):
            adapter['language_code'] = 'pt'
        
        return item


class DataCleaningPipeline:
    """数据清洗管道"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # 清洗字符串字段
        for field_name, field_value in adapter.items():
            if isinstance(field_value, str):
                # 去除首尾空格
                cleaned_value = field_value.strip()
                # 替换空字符串为None
                adapter[field_name] = cleaned_value if cleaned_value else None
        
        # 处理数值字段
        numeric_fields = ['sport_id', 'country_id', 'league_id', 'team_id', 'season_id', 
                         'match_id', 'home_team_id', 'away_team_id', 'home_score', 'away_score',
                         'round_number', 'week', 'timezone_offset', 'timestamp_utc']
        
        for field in numeric_fields:
            if field in adapter and adapter[field] is not None:
                try:
                    adapter[field] = int(adapter[field]) if adapter[field] != '' else None
                except (ValueError, TypeError):
                    adapter[field] = None
        
        # 处理布尔字段
        boolean_fields = ['friendly', 'is_current']
        for field in boolean_fields:
            if field in adapter and adapter[field] is not None:
                if isinstance(adapter[field], str):
                    adapter[field] = adapter[field].lower() in ('true', '1', 'yes')
                elif isinstance(adapter[field], int):
                    adapter[field] = bool(adapter[field])
        
        # 计算获胜方
        if isinstance(item, MatchItem):
            home_score = adapter.get('home_score')
            away_score = adapter.get('away_score')
            if home_score is not None and away_score is not None:
                if home_score > away_score:
                    adapter['winner'] = 'home'
                elif away_score > home_score:
                    adapter['winner'] = 'away'
                else:
                    adapter['winner'] = 'draw'
        
        return item


class MySQLPipeline:
    """MySQL数据库管道"""
    
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_db):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db
        self.engine = None
        self.Session = None
        self.logger = logging.getLogger(__name__)
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )
    
    def open_spider(self, spider):
        """爬虫开始时建立数据库连接"""
        try:
            connection_string = f'mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}'
            self.engine = create_engine(
                connection_string,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            self.Session = sessionmaker(bind=self.engine)
            self.logger.info(f"Connected to MySQL database: {self.mysql_db}")
        except Exception as e:
            self.logger.error(f"Failed to connect to MySQL: {e}")
            raise
    
    def close_spider(self, spider):
        """爬虫结束时关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("MySQL connection closed")
    
    def process_item(self, item, spider):
        """处理数据项"""
        session = self.Session()
        try:
            if isinstance(item, SportItem):
                self._save_sport(session, item)
            elif isinstance(item, CountryItem):
                self._save_country(session, item)
            elif isinstance(item, LeagueItem):
                self._save_league(session, item)
            elif isinstance(item, TeamItem):
                self._save_team(session, item)
            elif isinstance(item, SeasonItem):
                self._save_season(session, item)
            elif isinstance(item, MatchItem):
                self._save_match(session, item)

            
            session.commit()
            return item
        
        except IntegrityError as e:
            session.rollback()
            self.logger.warning(f"Duplicate entry ignored: {e}")
            return item
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving item: {e}")
            raise
        
        finally:
            session.close()
    
    def _save_sport(self, session, item):
        """保存体育项目数据"""
        adapter = ItemAdapter(item)
        
        # 检查是否已存在
        existing = session.query(Sports).filter_by(
            sport_id=adapter['sport_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            # 更新现有记录
            for key, value in adapter.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            # 创建新记录
            sport = Sports(
                sport_id=adapter['sport_id'],
                sport_name=adapter['sport_name'],
                sport_sid=adapter.get('sport_sid'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(sport)
    
    def _save_country(self, session, item):
        """保存国家数据"""
        adapter = ItemAdapter(item)
        
        existing = session.query(Countries).filter_by(
            country_id=adapter['country_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            # 过滤掉不存在的字段
            excluded_fields = {'continent', 'population'}
            for key, value in adapter.items():
                if key not in excluded_fields and hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            country = Countries(
                country_id=adapter['country_id'],
                country_name=adapter['country_name'],
                country_code=adapter.get('country_code'),
                country_code_3=adapter.get('country_code_3'),
                ioc_code=adapter.get('ioc_code'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(country)
    
    def _save_league(self, session, item):
        """保存联赛数据"""
        adapter = ItemAdapter(item)
        
        existing = session.query(Leagues).filter_by(
            league_id=adapter['league_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            # 过滤掉不存在的字段
            excluded_fields = {'friendly', 'league_order'}
            for key, value in adapter.items():
                if key not in excluded_fields and hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            league = Leagues(
                league_id=adapter['league_id'],
                league_name=adapter['league_name'],
                country_id=adapter.get('country_id'),
                sport_id=adapter.get('sport_id'),
                unique_tournament_id=adapter.get('unique_tournament_id'),
                current_season_id=adapter.get('current_season_id'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(league)
    
    def _save_team(self, session, item):
        """保存队伍数据"""
        adapter = ItemAdapter(item)
        
        existing = session.query(Teams).filter_by(
            team_id=adapter['team_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            for key, value in adapter.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            team = Teams(
                team_id=adapter['team_id'],
                team_name=adapter['team_name'],
                country_id=adapter.get('country_id'),
                sport_id=adapter.get('sport_id'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(team)
    
    def _save_season(self, session, item):
        """保存赛季数据"""
        adapter = ItemAdapter(item)
        
        existing = session.query(Seasons).filter_by(
            season_id=adapter['season_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            for key, value in adapter.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            season = Seasons(
                season_id=adapter['season_id'],
                season_name=adapter['season_name'],
                league_id=adapter.get('league_id'),
                sport_id=adapter.get('sport_id'),
                start_date=adapter.get('start_date'),
                end_date=adapter.get('end_date'),
                is_current=adapter.get('is_current'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(season)
    
    def _save_match(self, session, item):
        """保存比赛数据"""
        adapter = ItemAdapter(item)
        
        existing = session.query(Matches).filter_by(
            match_id=adapter['match_id'],
            language_code=adapter['language_code']
        ).first()
        
        if existing:
            for key, value in adapter.items():
                if hasattr(existing, key) and value is not None:
                    setattr(existing, key, value)
            existing.updated_at = datetime.now()
        else:
            match = Matches(
                match_id=adapter['match_id'],
                sport_id=adapter.get('sport_id'),
                country_id=adapter.get('country_id'),
                league_id=adapter.get('league_id'),
                unique_tournament_id=adapter.get('unique_tournament_id'),
                season_id=adapter.get('season_id'),
                round_number=adapter.get('round_number'),
                home_team_id=adapter.get('home_team_id'),
                away_team_id=adapter.get('away_team_id'),
                match_time=adapter.get('match_time'),
                home_score=adapter.get('home_score'),
                away_score=adapter.get('away_score'),
                match_status=adapter.get('match_status'),
                language_code=adapter['language_code'],
                created_at=adapter.get('created_at', datetime.now()),
                updated_at=adapter.get('updated_at', datetime.now())
            )
            session.add(match)
