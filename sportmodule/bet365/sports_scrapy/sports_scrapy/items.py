# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field
from datetime import datetime


class SportItem(scrapy.Item):
    """体育项目数据项"""
    sport_id = Field()  # 体育项目ID
    sport_name = Field()  # 体育项目名称
    sport_sid = Field()  # 体育项目SID
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间


class CountryItem(scrapy.Item):
    """国家/地区数据项"""
    country_id = Field()  # 国家ID
    country_name = Field()  # 国家名称
    country_code = Field()  # 国家代码
    country_code_3 = Field()  # 国家代码3
    ioc_code = Field()  # IOC代码
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间


class LeagueItem(scrapy.Item):
    """联赛数据项"""
    league_id = Field()  # 联赛ID
    league_name = Field()  # 联赛名称
    country_id = Field()  # 国家ID
    sport_id = Field()  # 体育项目ID
    unique_tournament_id = Field()  # 唯一锦标赛ID
    current_season_id = Field()  # 当前赛季ID
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间


class TeamItem(scrapy.Item):
    """队伍数据项"""
    team_id = Field()  # 队伍ID
    team_name = Field()  # 队伍名称
    # team_sid = Field()  # 队伍SID
    # team_uid = Field()  # 队伍UID
    country_id = Field()  # 国家ID
    sport_id = Field()  # 体育项目ID
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间


class SeasonItem(scrapy.Item):
    """赛季数据项"""
    season_id = Field()  # 赛季ID
    season_name = Field()  # 赛季名称
    league_id = Field()  # 联赛ID
    sport_id = Field()  # 体育项目ID
    start_date = Field()  # 开始日期
    end_date = Field()  # 结束日期
    is_current = Field()  # 是否当前赛季
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间


class MatchItem(scrapy.Item):
    """比赛数据项"""
    match_id = Field()  # 比赛ID
    sport_id = Field()  # 体育项目ID
    country_id = Field()  # 国家ID
    league_id = Field()  # 联赛ID
    unique_tournament_id = Field()  # 唯一锦标赛ID
    season_id = Field()  # 赛季ID
    round_number = Field()  # 轮次号
    home_team_id = Field()  # 主队ID
    away_team_id = Field()  # 客队ID
    match_time = Field()  # 比赛时间
    home_score = Field()  # 主队得分
    away_score = Field()  # 客队得分
    match_status = Field()  # 比赛状态
    language_code = Field()  # 语言代码
    created_at = Field()  # 创建时间
    updated_at = Field()  # 更新时间
