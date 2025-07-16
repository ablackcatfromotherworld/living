import requests
import time
import datetime
from pathlib import Path
import parsel
import html
import ujson
import logging
import schedule
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TVProgram(Base):
    __tablename__ = 'tvmap_jmd'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    img_cover = Column(String(255))
    programs = Column(JSON)
    updatetime = Column(DateTime, default=datetime.datetime.now)

class TVMapCrawler:
    def __init__(self):
        # 数据库连接
        self.engine = create_engine('mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        self.headers = {
            'x-requested-with': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://tvmap.com.br/Programacao/'
        self.time_slots = ['2.30', '5.30', '8.00', '10.30', '13.00', '15.30', '18.00', '20.30', '23.00']
        logging.basicConfig(level=logging.INFO)

    def get_formatted_date(self, days_ahead=0):
        target_date = datetime.datetime.now() + datetime.timedelta(days=days_ahead)
        # 将月份转换为巴西葡萄牙语简写
        month_map = {
            1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr', 5: 'mai', 6: 'jun',
            7: 'jul', 8: 'ago', 9: 'set', 10: 'out', 11: 'nov', 12: 'dez'
        }
        day = target_date.strftime("%d")
        month = month_map[target_date.month]
        year = target_date.strftime("%Y")
        return f"{day}-{month}-{year}"

    def crawl_schedule(self, date, time_slot):
        url = f"{self.base_url}{date}/{time_slot}hs"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                selector = parsel.Selector(response.text)
                channels_data = []

                tables = selector.xpath('//div[@id="zc-grid"]/table')
                for table in tables:
                    channel_info = {}
                    
                    # 获取频道名称
                    channel_name = table.xpath('.//tbody//div/span/a/text()').get()
                    if not channel_name:
                        continue
                        
                    # 获取频道台标
                    logo_url = table.xpath('.//tbody//div/a/img/@src').get()
                    
                    # 获取节目信息
                    programs = []
                    program_rows = table.xpath('.//tbody/tr//table//tr/td')
                    
                    for row in program_rows:
                        title = row.xpath('./a/text()').get().strip()
                        program_time = row.xpath('./span/text()').get()
                        
                        if title and program_time:
                            programs.append({
                                "title": html.unescape(title.strip()),
                                "time": program_time.strip()
                            })
                    
                    if programs:  # 只添加有节目的频道
                        channel_info["name"] = channel_name.strip()
                        channel_info["logo"] = 'https://tvmap.com.br' + logo_url
                        channel_info["programs"] = programs
                        channels_data.append(channel_info)
                
                return channels_data
            else:
                logging.error(f"Failed to fetch data from {url}, status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"Error crawling {url}: {str(e)}")
            return None

    def save_data(self, data, date):
        output_dir = Path("tvmap_data")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"tvmap_{date}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            ujson.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"Data saved to {output_file}")
        
    def cleanup_old_files(self):
        """清理7天前的数据文件"""
        output_dir = Path("tvmap_data")
        if not output_dir.exists():
            return
            
        current_date = datetime.datetime.now()
        for file in output_dir.glob("tvmap_*.json"):
            try:
                # 从文件名中提取日期
                date_str = file.stem.replace('tvmap_', '')
                file_date = datetime.datetime.strptime(date_str, '%d-%b-%Y')
                
                # 如果文件超过7天，则删除
                if (current_date - file_date).days > 7:
                    file.unlink()
                    logging.info(f"Deleted old file: {file}")
            except Exception as e:
                logging.error(f"Error processing file {file}: {str(e)}")


    def merge_channel_data(self, channels_data_list):
        merged_data = {}
        for channel_data in channels_data_list:
            channel_name = channel_data['name']
            if channel_name not in merged_data:
                merged_data[channel_name] = {
                    'name': channel_name,
                    'logo': channel_data['logo'],
                    'programs': []
                }
            merged_data[channel_name]['programs'].extend(channel_data['programs'])
        return list(merged_data.values())

    def run_crawler(self):
        # 获取明天和后天的日期
        tomorrow = self.get_formatted_date(1)
        day_after = self.get_formatted_date(2)
        
        # 存储两天的数据
        all_data = {}
        
        for date in [tomorrow, day_after]:
            daily_data = []
            all_channels_data = []
            
            for time_slot in self.time_slots:
                logging.info(f"Crawling data for {date} {time_slot}hs")
                channels_data = self.crawl_schedule(date, time_slot)
                
                if channels_data:
                    all_channels_data.extend(channels_data)
                time.sleep(2)  # 添加延迟避免请求过快
            
            # 合并同一频道的节目数据
            merged_channels = self.merge_channel_data(all_channels_data)
            daily_data.extend(merged_channels)
            all_data[date] = daily_data
        
        # 保存合并后的数据
        self.save_data(all_data, tomorrow)
        # 上传到数据库
        self.upload_to_db(all_data)
    
    def upload_to_db(self, all_data):
        try:
            # 获取所有频道的名称集合
            channel_names = set()
            for date_data in all_data.values():
                for channel in date_data:
                    channel_names.add(channel['name'])
            
            # 处理每个频道
            for channel_name in channel_names:
                channel_programs = {}
                channel_logo = None
                
                # 收集该频道在两天中的节目数据
                for date, date_data in all_data.items():
                    channel_programs[date] = []
                    for channel in date_data:
                        if channel['name'] == channel_name:
                            channel_programs[date].append({"programs": channel['programs']})
                            channel_logo = channel['logo']
                
                # 检查是否已存在该频道
                existing_program = self.session.query(TVProgram).filter_by(title=channel_name).first()
                
                if existing_program:
                    # 更新现有记录
                    existing_program.img_cover = channel_logo
                    existing_program.programs = channel_programs
                    existing_program.updatetime = datetime.datetime.now()
                else:
                    # 创建新记录
                    new_program = TVProgram(
                        title=channel_name,
                        img_cover=channel_logo,
                        programs=channel_programs
                    )
                    self.session.add(new_program)
            
            self.session.commit()
            logging.info("Successfully uploaded data to database")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error uploading to database: {str(e)}")

def schedule_tasks():
    crawler = TVMapCrawler()
    
    def job():
        crawler.run_crawler()
        # 每周日执行清理
        if datetime.datetime.now().weekday() == 6:
            crawler.cleanup_old_files()
    
    # 设置定时任务：启动时运行一次，然后每天0点运行
    job()  # 立即运行一次
    schedule.every().day.at("00:00").do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_tasks()
