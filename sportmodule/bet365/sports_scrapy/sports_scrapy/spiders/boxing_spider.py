import scrapy
import json
import datetime 
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from ..items import (
    SportItem, CountryItem, LeagueItem, TeamItem, 
    SeasonItem, MatchItem
)


class BoxingSpider(scrapy.Spider):
    name = "boxing_spider"
    allowed_domains = ["stats.fn.sportradar.com", "s5.sir.sportradar.com"]
    
    # 拳击运动配置
    sport_id = 13
    sport_name = "拳击"
    
    # API配置
    base_url_template = "https://stats.fn.sportradar.com/bet365/{}/Asia:Shanghai/gismo"
    web_base_url_template = "https://s5.sir.sportradar.com/bet365/{}"
    timezone = "Asia/Shanghai"
    
    # 请求头配置
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    def start_requests(self):
        """开始请求 - 直接获取拳击的国家数据"""
        languages = ['pt', 'es', 'en']
        sync_group = f"boxing_countries_{int(time.time())}"
        
        # 直接为拳击运动获取国家数据
        for language in languages:
            base_url = self.base_url_template.format(language)
            countries_url = f"{base_url}/config_tree_mini/41/0/{self.sport_id}"
            yield scrapy.Request(
                url=countries_url,
                headers=self.custom_headers,
                callback=self.parse_countries,
                meta={'sport_id': self.sport_id, 'language': language, 'step': 'countries', 'sync_group': sync_group}
            )
    
    def parse_countries(self, response):
        """解析国家/地区数据"""
        try:
            sport_id = response.meta['sport_id']
            data = json.loads(response.text)
            
            # 正确解析数据结构：doc[0]['data'][0]['realcategories']
            countries_data = []
            if ('doc' in data and len(data['doc']) > 0 and 'data' in data['doc'][0] 
                and len(data['doc'][0]['data']) > 0 and 'realcategories' in data['doc'][0]['data'][0]):
                countries_data = data['doc'][0]['data'][0]['realcategories']
            
            self.logger.info(f"拳击运动获取到 {len(countries_data)} 个国家/地区")
            
            # 只获取指定的国家ID
            target_countries = [392, 4, 13]
            
            for country in countries_data:
                country_id = country.get('_id')  # 使用_id字段
                
                # 只处理指定的国家
                if country_id not in target_countries:
                    continue
                
                # 创建国家/地区Item
                country_item = CountryItem()
                country_item['country_id'] = country_id
                country_item['country_name'] = country.get('name', '')
                cc_info = country.get('cc', {})
                country_item['country_code'] = cc_info.get('a2', '') if cc_info else ''
                country_item['country_code_3'] = cc_info.get('a3', '') if cc_info else ''
                country_item['ioc_code'] = cc_info.get('ioc', '') if cc_info else ''
                country_item['language_code'] = response.meta.get('language', 'pt')
                country_item['created_at'] = datetime.now().isoformat()
                country_item['updated_at'] = datetime.now().isoformat()
                
                yield country_item
                
                # 只在第一种语言时为所有语言同时生成leagues请求
                current_language = response.meta.get('language', 'pt')
                if current_language == 'pt':  # 只在处理第一种语言时生成所有语言的请求
                    sync_group = f"boxing_leagues_{sport_id}_{country_id}_{int(time.time())}"
                    languages = ['pt', 'es', 'en']
                    for lang in languages:
                        base_url = self.base_url_template.format(lang)
                        leagues_url = f"{base_url}/config_tree_mini/41/0/{sport_id}/{country_id}"
                        yield scrapy.Request(
                            url=leagues_url,
                            headers=self.custom_headers,
                            callback=self.parse_leagues,
                            meta={'sport_id': sport_id, 'country_id': country_id, 'language': lang, 'step': 'leagues', 'sync_group': sync_group}
                        )
                
        except Exception as e:
            self.logger.error(f"解析拳击国家/地区数据失败: {e}")
    
    def parse_leagues(self, response):
        """解析联赛数据"""
        try:
            sport_id = response.meta['sport_id']
            country_id = response.meta['country_id']
            
            # 解析JSON响应
            data = json.loads(response.text)
            
            # 提取联赛数据
            leagues_data = []
            if 'doc' in data and isinstance(data['doc'], list):
                for doc in data['doc']:
                    if 'data' in doc and isinstance(doc['data'], list):
                        for sport_data in doc['data']:
                            if 'realcategories' in sport_data:
                                for category in sport_data['realcategories']:
                                    if 'tournaments' in category:
                                        leagues_data.extend(category['tournaments'])
            
            self.logger.info(f"拳击国家 {country_id} 获取到 {len(leagues_data)} 个联赛")
            
            for league in leagues_data:
                league_id = league.get('_tid')
                unique_tournament_id = league.get('_utid')
                season_id = league.get('seasonid')
                current_season = league.get('currentseason')
                
                # 创建联赛Item
                league_item = LeagueItem()
                league_item['league_id'] = league_id
                league_item['unique_tournament_id'] = unique_tournament_id
                league_item['sport_id'] = sport_id
                league_item['country_id'] = country_id
                league_item['league_name'] = league.get('name', '')
                league_item['current_season_id'] = current_season or season_id
                league_item['language_code'] = response.meta.get('language', 'pt')
                league_item['created_at'] = datetime.now().isoformat()
                league_item['updated_at'] = datetime.now().isoformat()
                
                yield league_item
                
                if season_id:
                    # 只在第一种语言时为所有语言同时生成matches请求
                    current_language = response.meta.get('language', 'pt')
                    if current_language == 'pt':  # 只在处理第一种语言时生成所有语言的请求
                        sync_group = f"boxing_matches_{season_id}_{int(time.time())}"
                        languages = ['pt', 'es', 'en']
                        for lang in languages:
                            base_url = self.base_url_template.format(lang)
                            matches_url = f"{base_url}/stats_season_fixtures2/{season_id}/1"
                            yield scrapy.Request(
                                url=matches_url,
                                headers=self.custom_headers,
                                callback=self.parse_matches,
                                meta={
                                    'sport_id': sport_id,
                                    'country_id': country_id,
                                    'league_id': league_id,
                                    'unique_tournament_id': unique_tournament_id,
                                    'season_id': season_id,
                                    'season_name': league.get('name', ''),
                                    'language': lang,
                                    'step': 'matches',
                                    'sync_group': sync_group
                                }
                            )
                
        except Exception as e:
            self.logger.error(f"解析拳击联赛数据失败: {e}")
    
    def parse_matches(self, response):
        """解析比赛数据"""
        try:
            sport_id = response.meta['sport_id']
            country_id = response.meta['country_id']
            league_id = response.meta['league_id']
            unique_tournament_id = response.meta['unique_tournament_id']
            season_id = response.meta['season_id']
            season_name = response.meta['season_name']
            
            data = json.loads(response.text)
            
            # 提取比赛数据
            matches_data = []
            if 'doc' in data and isinstance(data['doc'], list):
                season_data = data['doc'][0]['data']
                for item in data['doc']:
                    if 'data' in item and 'matches' in item['data']:
                        matches_data.extend(item['data']['matches'])
            
            # 创建赛季Item
            season_item = SeasonItem()
            season_item['season_id'] = season_data.get('_id')
            season_item['season_name'] = season_data.get('name')
            season_item['league_id'] = league_id
            season_item['sport_id'] = sport_id
            season_item['start_date'] = season_data.get('start').get('uts') if season_data.get('start') else ''
            season_item['end_date'] = season_data.get('end').get('uts') if season_data.get('end') else ''
            season_item['is_current'] = (season_id == season_data.get('currentseasonid'))
            season_item['language_code'] = response.meta.get('language', 'pt')
            season_item['created_at'] = datetime.now().isoformat()
            season_item['updated_at'] = datetime.now().isoformat()
            
            yield season_item
            self.logger.info(f"拳击赛季 {season_id} 获取到 {len(matches_data)} 场比赛")
            
            for match in matches_data:
                match_id = match.get('_id')
                
                # 处理队伍信息
                home_team = match.get('teams').get('home')
                away_team = match.get('teams').get('away')
                result = match.get('result')
                
                # 创建主队Item
                if home_team:
                    home_team_item = TeamItem()
                    home_team_item['team_id'] = home_team.get('_id')
                    home_team_item['team_name'] = home_team.get('name', '')
                    home_team_item['country_id'] = country_id
                    home_team_item['sport_id'] = sport_id
                    home_team_item['language_code'] = response.meta.get('language', 'pt')
                    home_team_item['created_at'] = datetime.now().isoformat()
                    home_team_item['updated_at'] = datetime.now().isoformat()
                    yield home_team_item
                
                # 创建客队Item
                if away_team:
                    away_team_item = TeamItem()
                    away_team_item['team_id'] = away_team.get('_id')
                    away_team_item['team_name'] = away_team.get('name', '')
                    away_team_item['country_id'] = country_id
                    away_team_item['sport_id'] = sport_id
                    away_team_item['language_code'] = response.meta.get('language', 'pt')
                    away_team_item['created_at'] = datetime.now().isoformat()
                    away_team_item['updated_at'] = datetime.now().isoformat()
                    yield away_team_item
                
                # 创建比赛Item
                match_item = MatchItem()
                match_item['match_id'] = match_id
                match_item['sport_id'] = sport_id
                match_item['country_id'] = country_id
                match_item['league_id'] = league_id
                match_item['unique_tournament_id'] = unique_tournament_id
                match_item['season_id'] = season_id

                # 比赛时间
                start_time = match.get('time').get('uts')
                match_item['match_time'] = start_time
                
                # 队伍信息
                match_item['home_team_id'] = home_team.get('_id')
                match_item['away_team_id'] = away_team.get('_id')
                
                # 比分信息
                match_item['home_score'] = result.get('home')
                match_item['away_score'] = result.get('away')
                
                # 比赛状态
                winner_status = result.get('winner')
                timestamp = int(time.time() - (time.time() % 60))
                if winner_status:
                    match_item['match_status'] = 2 # FT
                elif start_time < timestamp:
                    match_item['match_status'] = 1 # LIVE
                else:
                    match_item['match_status'] = 0 # NS
                
                # 其他信息
                match_item['round_number'] = match.get('round')
                match_item['language_code'] = response.meta.get('language', 'pt')
                match_item['created_at'] = datetime.now().isoformat()
                match_item['updated_at'] = datetime.now().isoformat()
                
                yield match_item
                
        except Exception as e:
            self.logger.error(f"解析拳击比赛数据失败: {e}")
    
    def parse(self, response):
        """默认解析方法（不使用）"""
        pass
