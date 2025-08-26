# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
from datetime import datetime

# 导入Item
from esports_scrapy.items import GloboSportsItem

class GloboSportsSpider(scrapy.Spider):
    name = 'globo_sports'
    allowed_domains = ['globo.com', 'globoplay.globo.com', 'cloud-jarvis.globo.com']
   
    start_urls = [
        'https://globoplay.globo.com/categorias/esportes/',
        ]
    # 自定义设置
    custom_settings = {
        'ITEM_PIPELINES': {
            'esports_scrapy.pipelines.GloboSportsPipeline': 300,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(GloboSportsSpider, self).__init__(*args, **kwargs)

        self.headers = {
            'x-glb-exp-id': 'jra0VrIvHRqinAH_pXpN1yz0GMQpgp9DMK_FgRfdmNw=',
            'authorization': '139c8bca2815a1c71b11c874f68082c8d51556531524b56614d44416f52455374707246666f793873454e71674d64724c666a4a6f4a7a737375666b49734c706747445a6748473953413634314c636f56584b6559643344505f66794a427761643138504137673d3d3a303a75716f7a75346764773369397535317676656664',
            'x-platform-id': 'web',
            'x-user-id': '93cc4ec3-958b-41e7-8531-c1c1c320bf39',
            'x-device-id': 'desktop',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'Referer': 'https://globoplay.globo.com/',
            'sec-ch-ua-mobile': '?0',
            'x-hsid': '08fb7c2a-ccc7-4219-a2d8-9667fb3fb075',
            'sec-ch-ua-platform': '"Windows"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'accept': '*/*',
            'x-client-version': '2025.08-7',
            'content-type': 'application/json',
            'x-tenant-id': 'globo-play',
        }
        self.logger.info("初始化GloboSportsSpider")
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_with_existing_function)
    
    @staticmethod
    def get_params(page: int, title_id: str):
        params = {
        'operationName': 'getEpisodesPlaylist',
        'variables': f'{{"titleId":"{title_id}","page":{page},"perPage":40}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"77fbf2cae4a7a8f5a39e33c4d8b37a40b566d7dc3506d3ea876dd7a1dc1d74a4"}}',
        }
        return params 

    def parse_with_existing_function(self, response):
        """
        使用现有函数解析数据
        """
        self.logger.info(f"正在处理页面: {response.url}")
        
        try:
            # 提取页面中的apolloState数据
            apollo_state_pattern = re.compile(r'apolloState[:=]\s*(\{.*?\}),\s*preloadedState', re.DOTALL)
            match = apollo_state_pattern.search(response.text)
            
            if match:
                apollo_state_json = match.group(1)
                data = json.loads(apollo_state_json)
                
                # 处理数据
                for key, value in data.items():
                    if key.startswith('Title:') and isinstance(value, dict):
                        try:
                            item = GloboSportsItem()
                            
                            # 提取基本字段
                            item['titleId'] = value.get('titleId')
                            item['headline'] = value.get('headline')
                            item['originProgramId'] = value.get('originProgramId')
                            item['slug'] = value.get('slug')
                            item['type'] = value.get('type')
                            
                            
                            # 添加元数据
                            item['created_at'] = datetime.now()
                            
                            # 尝试获取该类别的详细数据
                            if item['titleId']:
                                page = 1
                                params = self.get_params(page=page, title_id=item['titleId'])
                                episode_url = f"https://cloud-jarvis.globo.com/graphql"
                                yield scrapy.FormRequest(
                                    method='GET',
                                    url=episode_url,
                                    callback=self.parse_episodes,
                                    meta={'item': item, 'page': page},
                                    priority=10,
                                    formdata=params,
                                    dont_filter=True,
                                    headers=self.headers
                                )
                
                        except Exception as e:
                            self.logger.error(f"处理数据项时出错: {e}")
                       
        except Exception as e:
            self.logger.error(f"解析页面时出错: {e}")
    
    def parse_episodes(self, response):
        """
        解析详细数据api
        """
        item = response.meta['item']
        page = response.meta['page']

        try:
            data = response.json()
            resources = data['data']['title']['structure']['episodes']['resources'] or None 
            if resources:
                for resource in resources:
                    item['episode_id'] = resource.get('video').get('id')
                    item['episode_headline'] = resource.get('video').get('headline') 
                    yield item
                    page += 1
                    yield scrapy.FormRequest(
                        method='GET',
                        url=response.url,
                        callback=self.parse_episodes,
                        meta={'item': item, 'page': page},
                        priority=10,
                        dont_filter=True,
                        formdata=self.get_params(page=page, title_id=item['titleId']),
                        headers=self.headers
                    )
            else:
                return None 
                
        except Exception as e:
            self.logger.error(f"解析剧集页面时出错: {e}")
            return None 
    
    def parse(self, response):
        pass
