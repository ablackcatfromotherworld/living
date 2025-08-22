from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Sports(Base):
    __tablename__ = 'sports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sport_id = Column(Integer, nullable=False)
    sport_name = Column(String(255), nullable=False)
    sport_sid = Column(String(100))
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Countries(Base):
    __tablename__ = 'countries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, nullable=False)
    country_name = Column(String(255), nullable=False)
    country_code = Column(String(10))
    country_code_3 = Column(String(10))
    ioc_code = Column(String(10))
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Leagues(Base):
    __tablename__ = 'leagues'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    league_id = Column(Integer, nullable=False)
    league_name = Column(String(255), nullable=False)
    country_id = Column(Integer)
    sport_id = Column(Integer)
    unique_tournament_id = Column(Integer)
    current_season_id = Column(Integer)
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Teams(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, nullable=False)
    team_name = Column(String(255), nullable=False)
    # team_sid = Column(String(100))
    # team_uid = Column(String(100))
    country_id = Column(Integer)
    sport_id = Column(Integer)
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Seasons(Base):
    __tablename__ = 'seasons_sport'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    season_id = Column(Integer, nullable=False)
    season_name = Column(String(255), nullable=False)
    league_id = Column(Integer)
    sport_id = Column(Integer)
    start_date = Column(String(50))
    end_date = Column(String(50))
    is_current = Column(Boolean, default=False)
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Matches(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, nullable=False)
    sport_id = Column(Integer)
    country_id = Column(Integer)
    league_id = Column(Integer)
    unique_tournament_id = Column(Integer)
    season_id = Column(Integer)
    round_number = Column(Integer)
    home_team_id = Column(Integer)
    away_team_id = Column(Integer)
    match_time = Column(DateTime)
    home_score = Column(Integer)
    away_score = Column(Integer)
    match_status = Column(TINYINT(unsigned=True))
    language_code = Column(String(10), nullable=False, default='pt')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

def create_tables(connection_string):
    """创建所有数据库表"""
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine

if __name__ == '__main__':
    # 示例用法
    connection_string = 'mysql+pymysql://user:password@host:port/database'
    engine = create_tables(connection_string)
    print("数据库表创建完成")