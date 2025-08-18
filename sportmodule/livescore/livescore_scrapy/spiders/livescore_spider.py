import scrapy
import json
import os
import requests
from datetime import datetime, timedelta
from items import LivescoreItem, TeamItem


class LivescoreSpider(scrapy.Spider):
    """Livescore数据爬虫 - 直接从API获取数据"""
    
    name = 'livescore'
    allowed_domains = ['prod-cdn-mev-api.livescore.com']
    
    def __init__(self, sports=None, languages=None, days_back=10, days_forward=30, *args, **kwargs):
        super(LivescoreSpider, self).__init__(*args, **kwargs)
        
        # 支持的运动类型和语言
        self.supported_sports = ['soccer', 'basketball', 'tennis', 'cricket', 'hockey']
        self.supported_languages = ['pt', 'es', 'en']
        
        # 解析参数
        self.sports = self._parse_list_param(sports, self.supported_sports)
        self.languages = self._parse_list_param(languages, self.supported_languages)
        self.days_back = int(days_back) if days_back else 10
        self.days_forward = int(days_forward) if days_forward else 30
        
        self.logger.info(f"运动类型: {self.sports}")
        self.logger.info(f"语言: {self.languages}")
        self.logger.info(f"获取数据范围: 过去{self.days_back}天到未来{self.days_forward}天")
    
    def _parse_list_param(self, param, default_list):
        """解析逗号分隔的参数"""
        if param:
            return [item.strip() for item in param.split(',') if item.strip()]
        return default_list[:3]  # 默认取前3个
    
    def start_requests(self):
        """开始请求 - 直接从API获取数据"""
        try:
            # 生成日期范围
            dates = self._generate_date_range()
            self.logger.info(f"生成了 {len(dates)} 个日期: {dates[0]} 到 {dates[-1]}")
            
            # 为每个运动类型、语言和日期生成API请求
            for sport in self.sports:
                for language in self.languages:
                    for date_str in dates:
                        url = f"https://prod-cdn-mev-api.livescore.com/v1/api/app/date/{sport}/{date_str}/8"
                        
                        yield scrapy.Request(
                            url=url,
                            callback=self.parse_api_response,
                            meta={
                                'sport': sport,
                                'language': language,
                                'date': date_str
                            },
                            headers={
                                'Accept': 'application/json',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            },
                            dont_filter=True
                        )
        
        except Exception as e:
            self.logger.error(f"生成API请求失败: {e}")
    
    def _generate_date_range(self):
        """生成日期范围"""
        dates = []
        today = datetime.now().date()
        
        # 过去的日期
        for i in range(self.days_back, 0, -1):
            date = today - timedelta(days=i)
            dates.append(date.strftime('%Y%m%d'))
        
        # 今天
        dates.append(today.strftime('%Y%m%d'))
        
        # 未来的日期
        for i in range(1, self.days_forward + 1):
            date = today + timedelta(days=i)
            dates.append(date.strftime('%Y%m%d'))
        
        return dates
    
    def parse_api_response(self, response):
        """解析API响应"""
        try:
            sport = response.meta['sport']
            language = response.meta['language']
            date_str = response.meta['date']
            
            # 解析JSON响应
            data = json.loads(response.text)
            
            if not data or 'Stages' not in data:
                self.logger.warning(f"API响应为空或格式不正确: {sport}/{date_str}")
                return
            
            stages = data.get('Stages', [])
            total_matches = 0
            
            for stage in stages:
                events = stage.get('Events', [])
                total_matches += len(events)
                
                for event in events:
                    # 提取比赛信息（传入stage信息）
                    match_info = self._extract_match_info(event, stage, sport, language, date_str)
                    
                    if match_info:
                        # 创建队伍Items
                        team1_item = self._create_team_item(
                            match_info['team1_id'],
                            match_info['team1_name'],
                            match_info['team1_img'],
                            sport
                        )
                        
                        team2_item = self._create_team_item(
                            match_info['team2_id'],
                            match_info['team2_name'],
                            match_info['team2_img'],
                            sport
                        )
                        
                        # 创建比赛Item
                        match_item = self._create_match_item(match_info, sport, language)
                        
                        # 返回数据
                        yield team1_item
                        yield team2_item
                        yield match_item
            
            self.logger.info(f"处理完成 {sport}/{date_str}: {total_matches} 场比赛")
        
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败 {sport}/{date_str}: {e}")
        except Exception as e:
            self.logger.error(f"解析API响应失败 {sport}/{date_str}: {e}")
    
    def _extract_match_info(self, event, stage, sport, language, date_str):
        """从事件数据中提取比赛信息"""
        try:
            # 基本信息
            match_id = str(event.get('Eid', ''))
            if not match_id:
                return None
            
            # 队伍信息
            t1 = event.get('T1', [{}])[0] if event.get('T1') else {}
            t2 = event.get('T2', [{}])[0] if event.get('T2') else {}
            
            team1_id = str(t1.get('ID', ''))
            team1_name = t1.get('Nm', '').strip()
            team1_img = t1.get('Img', '').strip()
            
            team2_id = str(t2.get('ID', ''))
            team2_name = t2.get('Nm', '').strip()
            team2_img = t2.get('Img', '').strip()
            
            if not team1_name or not team2_name:
                return None
            
            # 比赛时间和状态
            timestamp = event.get('Esd', 0)
            time_full = self._parse_timestamp_full(timestamp) if timestamp else ''
            
            # 比分
            tr1 = event.get('Tr1', '')
            tr2 = event.get('Tr2', '')
            
            # 比赛状态 - 优先使用EpsL字段，如果为空则使用Eps字段并映射
            status = event.get('EpsL', '').strip()  # 比赛状态（如Finished, Not started等）
            if not status:
                # 如果EpsL为空，尝试使用Eps字段并映射
                status_code = event.get('Eps', '').strip()
                if status_code:
                    status = self._map_status(status_code)
                else:
                    status = 'Unknown'  # 默认状态
            
            # 比赛进度信息
            round_info = event.get('ErnInf', '')  # 轮次/阶段信息（如Match 18）
            
            # 从stage中获取联赛和国家信息（修复空字段问题）
            stage_info = stage.get('Snm', '')  # 从stage获取联赛名称
            country = stage.get('Cnm', '')     # 从stage获取国家名称
            
            return {
                'match_id': match_id,
                'team1_id': team1_id,
                'team1_name': team1_name,
                'team1_img': team1_img,
                'team2_id': team2_id,
                'team2_name': team2_name,
                'team2_img': team2_img,
                'timestamp': timestamp,
                'time_full': time_full,
                'score1': str(tr1) if tr1 is not None else '',
                'score2': str(tr2) if tr2 is not None else '',
                'status': status,
                'round_info': round_info,
                'league': stage_info,
                'country': country,
                'date': date_str
            }
        
        except Exception as e:
            self.logger.error(f"提取比赛信息失败: {e}")
            return None
    
    def _create_team_item(self, team_id, team_name, team_img, sport):
        """创建队伍Item"""
        team_item = TeamItem()
        team_item['team_id'] = team_id
        team_item['team_name'] = team_name
        team_item['team_img'] = team_img
        team_item['sport'] = sport
        return team_item
    
    def _create_match_item(self, match_info, sport, language):
        """创建比赛Item"""
        match_item = LivescoreItem()
        match_item['match_id'] = match_info['match_id']
        match_item['sport'] = sport
        match_item['date'] = match_info['date']
        match_item['time_full'] = match_info['time_full']
        match_item['timestamp'] = match_info['timestamp']
        match_item['language'] = language
        match_item['league'] = match_info['league']
        match_item['country'] = match_info['country']
        match_item['team1_id'] = match_info['team1_id']
        match_item['team2_id'] = match_info['team2_id']
        match_item['score1'] = match_info['score1']
        match_item['score2'] = match_info['score2']
        match_item['status'] = match_info['status']
        match_item['round_info'] = match_info['round_info']
        
        # 队伍信息（保持向后兼容）
        match_item['team1'] = match_info['team1_name']
        match_item['team2'] = match_info['team2_name']
        match_item['team1_img'] = match_info['team1_img']
        match_item['team2_img'] = match_info['team2_img']
        
        return match_item
    
    def _parse_timestamp_full(self, timestamp):
        """解析时间戳为完整时间格式（巴西时间）"""
        try:
            if len(timestamp) == 14:
                year = timestamp[:4]
                month = timestamp[4:6]
                day = timestamp[6:8]
                hour = timestamp[8:10]
                minute = timestamp[10:12]
                second = timestamp[12:14]
                
                # 创建UTC时间
                dt_utc = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), tzinfo=timezone.utc)
                
                # 转换为巴西首都时间（UTC-3）
                brazil_tz = timezone(timedelta(hours=-3))
                dt_brazil = dt_utc.astimezone(brazil_tz)
                
                return dt_brazil.strftime('%Y-%m-%d')
        except Exception as e:
            self.logger.warning(f"时间转换失败 (timestamp: {timestamp}): {e}")
        return ''
    
    def _map_status(self, status_code):
        """映射状态码到状态描述"""
        status_mapping = {
            'NS': 'Not Started',
            'L': 'Live',
            'FT': 'Full Time',
            'HT': 'Half Time',
            'P': 'Postponed',
            'C': 'Cancelled',
            'A': 'Abandoned'
        }
        return status_mapping.get(status_code, status_code)
    
    def closed(self, reason):
        """爬虫关闭时的回调"""
        self.logger.info(f"爬虫关闭，原因: {reason}")


class LivescoreFileSpider(scrapy.Spider):
    """从文件系统读取多个JSON文件的爬虫"""
    
    name = 'livescore_files'
    allowed_domains = []
    
    def __init__(self, data_dir=None, file_pattern='*.json', *args, **kwargs):
        super(LivescoreFileSpider, self).__init__(*args, **kwargs)
        
        # 默认数据目录
        if data_dir is None:
            data_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        self.data_dir = data_dir
        self.file_pattern = file_pattern
        self.logger.info(f"数据目录: {self.data_dir}")
        self.logger.info(f"文件模式: {self.file_pattern}")
    
    def start_requests(self):
        """开始请求 - 扫描目录中的JSON文件"""
        try:
            import glob
            
            # 查找匹配的JSON文件
            pattern = os.path.join(self.data_dir, self.file_pattern)
            json_files = glob.glob(pattern)
            
            if not json_files:
                self.logger.warning(f"在 {self.data_dir} 中未找到匹配 {self.file_pattern} 的文件")
                return
            
            self.logger.info(f"找到 {len(json_files)} 个JSON文件")
            
            for json_file in json_files:
                self.logger.info(f"处理文件: {json_file}")
                
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if not isinstance(data, list):
                        self.logger.warning(f"文件 {json_file} 不包含列表数据，跳过")
                        continue
                    
                    self.logger.info(f"文件 {json_file} 包含 {len(data)} 条记录")
                    
                    # 为每条记录创建请求
                    for index, record in enumerate(data):
                        yield scrapy.Request(
                            url=f'data://livescore/{os.path.basename(json_file)}/{index}',
                            callback=self.parse_record,
                            meta={
                                'record': record,
                                'index': index,
                                'file': json_file
                            },
                            dont_filter=True
                        )
                
                except Exception as e:
                    self.logger.error(f"读取文件 {json_file} 失败: {e}")
        
        except Exception as e:
            self.logger.error(f"扫描目录失败: {e}")
    
    def parse_record(self, response):
        """解析单条记录"""
        try:
            record = response.meta['record']
            index = response.meta['index']
            file_path = response.meta['file']
            
            # 提取基本信息
            sport = record.get('sport', '').strip()
            team1_name = record.get('team1', '').strip()
            team2_name = record.get('team2', '').strip()
            team1_img = record.get('team1_img', '').strip()
            team2_img = record.get('team2_img', '').strip()
            match_date = record.get('date', '').strip()
            match_time = record.get('time_full', '').strip()
            language = record.get('language', '').strip()
            
            # 验证必填字段
            if not sport:
                self.logger.warning(f"文件 {file_path} 记录 {index} 缺少sport字段，跳过")
                return
            
            if not team1_name or not team2_name:
                self.logger.warning(f"文件 {file_path} 记录 {index} 缺少队伍信息，跳过")
                return
            
            if not language:
                self.logger.warning(f"文件 {file_path} 记录 {index} 缺少language字段，跳过")
                return
            
            # 生成唯一ID
            team1_id = f"{sport}_{team1_name}".replace(' ', '_')
            team2_id = f"{sport}_{team2_name}".replace(' ', '_')
            match_id = f"{sport}_{team1_name}_{team2_name}_{match_date}_{match_time}".replace(' ', '_')
            
            # 创建队伍Item（主队）
            team1_item = TeamItem()
            team1_item['team_id'] = team1_id
            team1_item['team_name'] = team1_name
            team1_item['team_img'] = team1_img
            team1_item['sport'] = sport
            
            # 创建队伍Item（客队）
            team2_item = TeamItem()
            team2_item['team_id'] = team2_id
            team2_item['team_name'] = team2_name
            team2_item['team_img'] = team2_img
            team2_item['sport'] = sport
            
            # 创建比赛Item
            match_item = LivescoreItem()
            match_item['match_id'] = match_id
            match_item['sport'] = sport
            match_item['date'] = match_date
            match_item['time_full'] = match_time
            match_item['timestamp'] = record.get('timestamp', '').strip()
            match_item['language'] = language
            match_item['league'] = record.get('league', '').strip()
            match_item['country'] = record.get('country', '').strip()
            match_item['team1_id'] = team1_id
            match_item['team2_id'] = team2_id
            match_item['score1'] = str(record.get('score1', '')).strip() if record.get('score1') is not None else ''
            match_item['score2'] = str(record.get('score2', '')).strip() if record.get('score2') is not None else ''
            match_item['status'] = record.get('status', '').strip()
            
            # 先返回队伍数据，再返回比赛数据
            yield team1_item
            yield team2_item
            yield match_item
        
        except Exception as e:
            self.logger.error(f"解析记录时出错: {e}")
    
    def closed(self, reason):
        """爬虫关闭时的回调"""
        self.logger.info(f"爬虫关闭，原因: {reason}")


class LivescoreWebSpider(LivescoreSpider):
    """Web API爬虫（继承主爬虫功能）"""
    
    name = 'livescore_web'
    
    def __init__(self, *args, **kwargs):
        super(LivescoreWebSpider, self).__init__(*args, **kwargs)
        self.logger.info("Web API爬虫已启动，使用与主爬虫相同的功能")
    
    # 继承父类的所有方法，无需重写