# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime


class TeamItem(scrapy.Item):
    """队伍数据项"""
    
    # 队伍标识
    team_id = scrapy.Field()        # 队伍唯一ID（来自原始数据源）
    team_name = scrapy.Field()      # 队伍名称
    team_img = scrapy.Field()       # 队伍图标URL
    sport = scrapy.Field()          # 运动类型
    
    def __repr__(self):
        return f"TeamItem({self.get('team_name', 'N/A')}, ID: {self.get('team_id', 'N/A')})"


class LivescoreItem(scrapy.Item):
    """Livescore比赛数据项"""
    
    # 比赛标识
    match_id = scrapy.Field()       # 比赛唯一ID（来自原始数据源）
    
    # 基本信息
    sport = scrapy.Field()          # 运动类型 (football, basketball, tennis等)
    date = scrapy.Field()           # 比赛日期
    time_full = scrapy.Field()      # 完整时间信息
    timestamp = scrapy.Field()      # 时间戳
    language = scrapy.Field()       # 语言
    
    # 联赛信息
    league = scrapy.Field()         # 联赛名称
    country = scrapy.Field()        # 国家
    
    # 队伍关联（外键）
    team1_id = scrapy.Field()       # 主队ID（关联teams表）
    team2_id = scrapy.Field()       # 客队ID（关联teams表）
    
    # 队伍信息（保持向后兼容）
    team1 = scrapy.Field()          # 主队名称
    team2 = scrapy.Field()          # 客队名称
    team1_img = scrapy.Field()      # 主队图标
    team2_img = scrapy.Field()      # 客队图标
    
    # 比分信息
    score1 = scrapy.Field()         # 主队比分
    score2 = scrapy.Field()         # 客队比分
    
    # 比赛状态
    status = scrapy.Field()         # 比赛状态（EpsL字段）
    
    # 比赛进度信息
    round_info = scrapy.Field()     # 轮次/阶段信息（ErnInf字段）
    
    def __repr__(self):
        return f"LivescoreItem({self.get('team1', 'N/A')} vs {self.get('team2', 'N/A')}, ID: {self.get('match_id', 'N/A')})"


# 保持向后兼容性的别名
MatchItem = LivescoreItem