# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class GloboSportsItem(scrapy.Item):
    """
    Globo Sports数据项定义
    对应数据库中的globo_sports表结构
    """
    # 基础字段
    titleId = Field()
    headline = Field()
    originProgramId = Field()
    slug = Field()
    type = Field()
    
    # 剧集相关字段
    episode_id = Field()
    episode_headline = Field()

    # 元数据字段
    created_at = Field()
    # updated_at = Field()
    

    
