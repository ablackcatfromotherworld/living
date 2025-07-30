import subprocess
import tls_client
import parsel
from urllib.parse import urljoin
import time
import json
import schedule
import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Float, ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
base = declarative_base()
engine = create_engine('mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider')
Session = sessionmaker(bind=engine)

class CXTV_live_streaming(base):
    __tablename__ = 'cxtv_live_streaming'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    areas = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    profile = Column(Text, nullable=False)
    country_img = Column(Text, nullable=False)
    img_cover = Column(Text, nullable=False)
    m3u8_url = Column(Text, nullable=False)
    codec_name = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    variant_bitrate = Column(BigInteger, nullable=False)

    


class CXTVEtractor:
    def __init__(self):
        self.session = tls_client.Session(
            client_identifier="chrome_106",
            random_tls_extension_order=True
        )
        self.base_url = "https://www.cxtv.com.br"

    def get_category_links(self):
        print("--- 开始获取分类链接 ---")
        try:
            res = self.session.get(urljoin(self.base_url, "tv"), timeout_seconds=30)
            if res.status_code != 200:
                print(f"获取主页失败，状态码: {res.status_code}")
                return []
        except Exception as e:
            print(f"获取主页时发生错误: {e}")
            return []

        selector = parsel.Selector(res.text)
        category_links = selector.xpath('//a[@class="m-b-20 btn btn-white btn-block padding-20"]/@href').getall()
        print(f"成功获取到 {len(category_links)} 个分类链接")
        return [urljoin(self.base_url, link) for link in category_links]

    def get_all_detail_links(self):
        category_links = self.get_category_links()
        if not category_links:
            print("未能获取到分类链接，程序终止")
            return []

        all_detail_links = set()
        data_url = urljoin(self.base_url, "data/tv_cat_list_load.php")

        for cat_link in category_links:
            caturl = cat_link.strip("/").split("/")[-1]
            print(f"\n--- 开始处理分类: {caturl} ---")
            
            # First, get the initial page directly
            try:
                print(f"正在请求分类首页: {cat_link}")
                res = self.session.get(cat_link, timeout_seconds=30)
                if res.status_code != 200:
                    print(f"请求分类首页失败，状态码: {res.status_code}")
                    continue
                
                selector = parsel.Selector(res.text)
                initial_links = selector.xpath('//a[@class="m-b-20 btn btn-white btn-block"]/@href').getall()
                print(f"从分类首页获取到 {len(initial_links)} 个链接")
                for link in initial_links:
                    all_detail_links.add(urljoin(self.base_url, link))

            except Exception as e:
                print(f"请求分类首页时发生错误: {e}")
                continue

            # Then, start pagination from page 2 (page 1 is the category page itself)
            next_param = 2
            while True:
                params = {
                    'caturl': caturl,
                    'short': 'mo',
                    'next': str(next_param),
                }
                try:
                    print(f"正在请求分页数据: next={params['next']}")
                    res = self.session.get(data_url, params=params, timeout_seconds=30)
                    
                    if res.status_code != 200:
                        print(f"请求分页数据失败，状态码: {res.status_code}")
                        break
                    
                    if not res.text.strip():
                        print("返回内容为空，此分类处理完毕")
                        break

                    selector = parsel.Selector(res.text)
                    new_links = selector.xpath('//a[@class="m-b-20 btn btn-white btn-block"]/@href').getall()
                    
                    if not new_links:
                        print("未在此分页中找到新链接，此分类处理完毕")
                        break

                    print(f"获取到 {len(new_links)} 个新链接")
                    for link in new_links:
                        full_link = urljoin(self.base_url, link)
                        all_detail_links.add(full_link)
                    
                    next_param += 1
                    time.sleep(1)

                except Exception as e:
                    print(f"请求分页数据时发生错误: {e}")
                    break
        
        return list(all_detail_links)

    def process_detail_page(self, detail_link, index):
        """处理单个详情页"""
        try:
            # 为每个线程创建独立的session
            session = tls_client.Session(
                client_identifier="chrome106",
                random_tls_extension_order=True
            )
            
            logging.info(f"正在处理第{index+1}个详情页: {detail_link}")
            res = session.get(detail_link, timeout_seconds=30)
            if res.status_code != 200:
                logging.warning(f"请求详情页失败，状态码: {res.status_code}")
                return None
            
            selector = parsel.Selector(res.text)
            
            # 获取M3U8链接
            m3u8_element = selector.xpath('//section[@class="video bg-silver b-radius-5 padding-5"]//source/@src').get()
            if not m3u8_element:
                return None
            
            # 提取详情页信息，使用与cxtv.py相同的XPath
            name = selector.xpath('//h1/text()').get() or ""
            category = selector.xpath('//*[@id="page-stream"]/div/div/div[1]/div[1]/div[2]/div[2]/a[1]/text()').get() or ""
            profile = selector.xpath('//*[@id="page-stream"]/div/div/div[1]/span/text()').get() or ""
            country_img = selector.xpath('//*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]/a[1]/img/@src').get() or ""
            country = selector.xpath('//*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]/a[1]/text()').get() or ""
            areas = selector.xpath('//*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]/text()').get() or ""
            img_cover = selector.xpath('//img[@class="b-radius-5"]/@src').get() or ""
            
            return {
                'name': name.strip(),
                'category': category.strip(),
                'areas': areas.strip(),
                'country': country.strip(),
                'profile': profile.strip(),
                'country_img': country_img,
                'img_cover': img_cover,
                'm3u8_url': m3u8_element
            }
            
        except Exception as e:
            logging.error(f"处理详情页时发生错误: {e}")
            return None

    def get_m3u8_url(self, max_workers=10):
        """获取详情页的M3U8链接和相关信息（多线程版本）"""
        detail_links = self.get_all_detail_links()
        m3u8_urls = []
        m3u8_count = 0
        count_lock = Lock()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_link = {executor.submit(self.process_detail_page, link, i): (link, i) 
                             for i, link in enumerate(detail_links)}
            
            # 处理完成的任务
            for future in as_completed(future_to_link):
                link, index = future_to_link[future]
                try:
                    result = future.result()
                    if result:
                        with count_lock:
                            m3u8_count += 1
                            logging.info(f"获取到第{m3u8_count}个m3u8")
                        m3u8_urls.append(result)
                except Exception as e:
                    logging.error(f"处理详情页 {link} 时发生错误: {e}")
        
        return m3u8_urls

    @staticmethod
    def find_best_video_stream(data_json):
        """找到最佳视频流"""
        video_streams = [
            s for s in data_json.get('streams', [])
            if s.get('codec_type') == 'video' and s.get('codec_name') == 'h264'
        ]
        if not video_streams:
            logging.warning("在 JSON 数据中没有找到任何 H.264 视频流。")
            return None
        try:
            best_stream = max(
                video_streams,
                key=lambda s: (s.get('height', 0), int(s.get('tags', {}).get('variant_bitrate', 0)))
            )
            return best_stream
        except (ValueError, TypeError) as e:
            logging.error(f"在比较流时发生错误: {e}。可能是某个流的码率不是有效的数字。")
            return None

    def validate_m3u8_url(self, m3u8_data, index):
        """验证单个M3U8链接"""
        m3u8_url = m3u8_data['m3u8_url']
        logging.info(f'正在处理第{index+1}个m3u8链接：{m3u8_url}')
        
        try:
            data = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", f"{m3u8_url}"],
                capture_output=True, timeout=60
            ).stdout.decode()
        except subprocess.TimeoutExpired:
            logging.warning(f"ffprobe 检查超时，跳过：{m3u8_url}")
            return None
        except Exception as e:
            logging.warning(f"ffprobe 检查异常，跳过：{m3u8_url}，错误：{e}")
            return None

        try:
            data_json = json.loads(data)
        except json.JSONDecodeError:
            logging.warning(f"ffprobe 返回数据解析失败：{m3u8_url}")
            return None
            
        if not data_json:
            return None
            
        try:
            if len(data_json.get('streams', [])) > 1 and data_json['streams'][1].get('codec_name') == 'h264':
                codec_name = data_json['streams'][1]['codec_name']
                width = data_json['streams'][1].get('coded_width', 0) or data_json['streams'][1].get('width', 0)
                height = data_json['streams'][1].get('coded_height', 0) or data_json['streams'][1].get('height', 0)
                variant_bitrate = data_json['streams'][1].get('tags', {}).get('variant_bitrate', 0) or 0
            else:
                highest_quality_stream = self.find_best_video_stream(data_json)
                if not highest_quality_stream:
                    return None
                codec_name = highest_quality_stream.get('codec_name')
                height = highest_quality_stream.get('height')
                width = highest_quality_stream.get('width')
                variant_bitrate = highest_quality_stream.get('tags', {}).get('variant_bitrate', 0)
            
            logging.info(f"m3u8_url: {m3u8_url}, codec_name: {codec_name}, width: {width}, height: {height}, variant_bitrate: {variant_bitrate}")
            
            if codec_name == 'h264' and height >= 720 and int(variant_bitrate) >= 1000000 or int(variant_bitrate) == 0:
                m3u8_data.update({
                    'codec_name': codec_name,
                    'width': width,
                    'height': height,
                    'variant_bitrate': variant_bitrate
                })
                return m3u8_data
                
        except Exception as e:
            logging.info(f"m3u8_url: {m3u8_url}解析有误！！！！！")
            return None
        
        return None

    def get_useful_m3u8_urls(self, max_workers=5, detail_workers=10):
        """获取有效的M3U8链接（通过ffprobe验证，多线程版本）"""
        m3u8_urls = self.get_m3u8_url(max_workers=detail_workers)
        m3u8_useful_urls = []
        valid_count = 0
        count_lock = Lock()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有验证任务
            future_to_data = {executor.submit(self.validate_m3u8_url, m3u8_data, i): (m3u8_data, i) 
                             for i, m3u8_data in enumerate(m3u8_urls)}
            
            # 处理完成的任务
            for future in as_completed(future_to_data):
                m3u8_data, index = future_to_data[future]
                try:
                    result = future.result()
                    if result:
                        with count_lock:
                            valid_count += 1
                            logging.info(f"验证通过第{valid_count}个有效m3u8")
                        m3u8_useful_urls.append(result)
                except Exception as e:
                    logging.error(f"验证m3u8链接 {m3u8_data['m3u8_url']} 时发生错误: {e}")
        
        return m3u8_useful_urls

    def upload_mysql(self, batch_size=100, detail_workers=10, validate_workers=5):
        """上传数据到MySQL数据库"""
        logging.info(f"开始数据采集，详情页并发数: {detail_workers}, 验证并发数: {validate_workers}")
        m3u8_urls = self.get_useful_m3u8_urls(max_workers=validate_workers, detail_workers=detail_workers)
        with Session() as db:
            updated_count = 0
            inserted_count = 0
            
            for i in range(0, len(m3u8_urls), batch_size):
                batch = m3u8_urls[i:i+batch_size]
                try:
                    for data in batch:
                        # 根据name字段查找现有记录
                        existing = db.query(CXTV_live_streaming).filter_by(name=data['name']).first()
                        
                        if existing:
                            # 更新现有记录
                            for key, value in data.items():
                                setattr(existing, key, value)
                            updated_count += 1
                        else:
                            # 插入新记录
                            new_record = CXTV_live_streaming(**data)
                            db.add(new_record)
                            inserted_count += 1
                    
                    db.commit()
                    logging.info(f"成功处理第{i//batch_size+1}批，共{len(batch)}条数据")
                except Exception as e:
                    db.rollback()
                    logging.error(f"处理第{i//batch_size+1}批数据失败，错误：{e}")
            
            logging.info(f"数据库操作完成：更新{updated_count}条，新增{inserted_count}条")

    @staticmethod
    def my_task(detail_workers=10, validate_workers=5):
        """定时任务"""
        start_time = datetime.datetime.now()
        logging.info(f"开始执行任务，当前时间: {start_time}")
        extractor = CXTVEtractor()
        extractor.upload_mysql(detail_workers=detail_workers, validate_workers=validate_workers)
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        logging.info(f"任务执行完成，耗时: {duration}")

    def run_scheduler(self):
        """运行定时任务调度器"""
        # 程序启动时立即执行一次
        self.my_task()
        
        # 每天0点执行
        schedule.every().day.at("00:00").do(self.my_task)
        
        logging.info("定时任务已启动，每天0点执行")
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

    def run(self):
        """运行爬虫（仅获取链接）"""
        detail_links = self.get_all_detail_links()
        print(f"\n--- 总共获取到 {len(detail_links)} 个不重复的详情页链接 ---")
        
        with open("cxtv_detail_links.txt", "w", encoding="utf-8") as f:
            for link in sorted(list(detail_links)):
                f.write(link + "\n")
        print("所有链接已保存到 cxtv_detail_links.txt 文件")

if __name__ == '__main__':
    extractor = CXTVEtractor()
    # 运行定时任务调度器
    extractor.run_scheduler()

import requests

cookies = {
    'LOGIN_INFO': 'AFmmF2swRgIhAP0XAR0kiByNJ8mNO3_1d4uAP36K-F2EgfkKk6LIAfXoAiEAix_0D-lYR0PBa0UufgwFDytnBjYFNYGXHW5on0iRHZg:QUQ3MjNmekZfTVhYbk9IR2ZueG9sUk95R0JFNndiaWU2YlBsSDBPR1N4NUJ0VjZSTUZGUjM4d1dYRFBQZXZYTzNfaFl5TV9qVld3ZmNkT1JRdU11SmdMOU54QzNaTGp1azg5c1J0QnQ2T19VUXhpVlV6Rld4dzU2YzBEN2hXVzlvaHN6VzdkMnNLRmlURUwyMUtxdWNZSEZ1bmV6ekNfb0ln',
    '__Secure-3PSIDTS': 'sidts-CjIB5H03P_B3jkbwUs4qN8A_H2syLXplEYBwIuB2vfu-1MO3UvghMbyGEmHqkUtgTXd63hAA',
    '__Secure-3PAPISID': 'isFO5K2AVZNBV28n/AB6easbTAR0jTKGOo',
    '__Secure-3PSID': 'g.a000zQgxpS404yF8S67f6MkY7ES3D3VLomstRaNnmo2YJHfuBHxGQ9Zs_pflCIaqrxaoYskU7wACgYKAXUSARYSFQHGX2Miyn4OhQLdzspcCKps20w8TxoVAUF8yKqcz_fMdW_W8VzvySZeJP1D0076',
    'YSC': 'JjNahjvVYN8',
    'VISITOR_INFO1_LIVE': '4aGKzIZxGE4',
    'VISITOR_PRIVACY_METADATA': 'CgJCUhIEGgAgYw%3D%3D',
    '__Secure-ROLLOUT_TOKEN': 'CKjCjYS_ouy--gEQsLKfvabfjgMYsLKfvabfjgM%3D',
    '__Secure-3PSIDCC': 'AKEyXzXnzkKaYLXufTFQxhjcQ4PMvQP6EPqeWYlZnp_UAh2GzcWQt9B6ntSXpI8LL50ddHupp4k',
}

headers = {
    'accept': '*/*, application/vnd.t1c.pxr-626-1',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'authorization': 'SAPISIDHASH 1753697018_2c33e1e5b3410f440d0f10809b9898aebd7f9710_u SAPISID3PHASH 1753697018_2c33e1e5b3410f440d0f10809b9898aebd7f9710_u',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.youtube.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.youtube.com/embed/Cy0s_bxzqkw?autoplay=true',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-browser-channel': 'stable',
    'x-browser-copyright': 'Copyright 2025 Google LLC. All rights reserved.',
    'x-browser-validation': '6h3XF8YcD8syi2FF2BbuE2KllQo=',
    'x-browser-year': '2025',
    'x-client-data': 'CIS2yQEIo7bJAQipncoBCKmVywEIlqHLAQiko8sBCIWgzQEIif3OARjh4s4B',
    'x-goog-authuser': '0',
    'x-goog-visitor-id': 'Cgs0YUdLeklaeEdFNCj3lZ3EBjIKCgJCUhIEGgAgYw%3D%3D',
    'x-origin': 'https://www.youtube.com',
    'x-youtube-bootstrap-logged-in': 'true',
    'x-youtube-client-name': '56',
    'x-youtube-client-version': '1.20250722.00.00',
    # 'cookie': 'LOGIN_INFO=AFmmF2swRgIhAP0XAR0kiByNJ8mNO3_1d4uAP36K-F2EgfkKk6LIAfXoAiEAix_0D-lYR0PBa0UufgwFDytnBjYFNYGXHW5on0iRHZg:QUQ3MjNmekZfTVhYbk9IR2ZueG9sUk95R0JFNndiaWU2YlBsSDBPR1N4NUJ0VjZSTUZGUjM4d1dYRFBQZXZYTzNfaFl5TV9qVld3ZmNkT1JRdU11SmdMOU54QzNaTGp1azg5c1J0QnQ2T19VUXhpVlV6Rld4dzU2YzBEN2hXVzlvaHN6VzdkMnNLRmlURUwyMUtxdWNZSEZ1bmV6ekNfb0ln; __Secure-3PSIDTS=sidts-CjIB5H03P_B3jkbwUs4qN8A_H2syLXplEYBwIuB2vfu-1MO3UvghMbyGEmHqkUtgTXd63hAA; __Secure-3PAPISID=isFO5K2AVZNBV28n/AB6easbTAR0jTKGOo; __Secure-3PSID=g.a000zQgxpS404yF8S67f6MkY7ES3D3VLomstRaNnmo2YJHfuBHxGQ9Zs_pflCIaqrxaoYskU7wACgYKAXUSARYSFQHGX2Miyn4OhQLdzspcCKps20w8TxoVAUF8yKqcz_fMdW_W8VzvySZeJP1D0076; YSC=JjNahjvVYN8; VISITOR_INFO1_LIVE=4aGKzIZxGE4; VISITOR_PRIVACY_METADATA=CgJCUhIEGgAgYw%3D%3D; __Secure-ROLLOUT_TOKEN=CKjCjYS_ouy--gEQsLKfvabfjgMYsLKfvabfjgM%3D; __Secure-3PSIDCC=AKEyXzXnzkKaYLXufTFQxhjcQ4PMvQP6EPqeWYlZnp_UAh2GzcWQt9B6ntSXpI8LL50ddHupp4k',
}

params = {
    'prettyPrint': 'false',
}

json_data = {
    'videoId': 'Cy0s_bxzqkw',
    'context': {
        'client': {
            'hl': 'en',
            'gl': 'BR',
            'remoteHost': '154.205.156.51',
            'deviceMake': '',
            'deviceModel': '',
            'visitorData': 'Cgs0YUdLeklaeEdFNCj3lZ3EBjIKCgJCUhIEGgAgYw%3D%3D',
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36,gzip(gfe)',
            'clientName': 'WEB_EMBEDDED_PLAYER',
            'clientVersion': '1.20250722.00.00',
            'osName': 'Windows',
            'osVersion': '10.0',
            'originalUrl': 'https://www.youtube.com/embed/Cy0s_bxzqkw?autoplay=true',
            'platform': 'DESKTOP',
            'clientFormFactor': 'UNKNOWN_FORM_FACTOR',
            'configInfo': {
                'appInstallData': 'CPeVncQGEParsAUQipeAExCHrM4cEMXLzxwQ78TPHBDT4a8FEPa6zxwQ9svPHBDds88cEJmYsQUQ_M7PHBDJ968FEPyyzhwQqZmAExCZjbEFEIGzzhwQvbauBRDOrM8cELCGzxwQzMDPHBC9irAFEOLKzxwQvZmwBRCU_rAFELjkzhwQ8sTPHBCly88cEMfIzxwQt-r-EhCJsM4cEAAQ4cvPHBDjvs8cELnZzhwQioKAExDa984cEJi5zxwQiIewBRDKys8cEJLRzxwQ3rzOHBCBzc4cEOq7zxwQ8JywBRCe0LAFEMXDzxwQn6HPHBCI468FEJOGzxwQu9nOHBCvj_8SEMzfrgUQ8OLOHBDmxc8cEKTPzxwqHENBTVNEeFVNLVpxLURPSGRoUXJMM0E0ZEJ3PT0%3D',
            },
            'browserName': 'Chrome',
            'browserVersion': '138.0.0.0',
            'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'deviceExperimentId': 'ChxOelV6TWpBM01UTXlOekl3TmprM05qRTBNZz09EPeVncQGGPeVncQG',
            'rolloutToken': 'CKjCjYS_ouy--gEQsLKfvabfjgMYsLKfvabfjgM%3D',
            'screenWidthPoints': 706,
            'screenHeightPoints': 411,
            'screenPixelDensity': 2,
            'screenDensityFloat': 1.5,
            'utcOffsetMinutes': 480,
            'userInterfaceTheme': 'USER_INTERFACE_THEME_LIGHT',
            'connectionType': 'CONN_CELLULAR_3G',
            'timeZone': 'Asia/Shanghai',
            'playerType': 'UNIPLAYER',
            'tvAppInfo': {
                'livingRoomAppMode': 'LIVING_ROOM_APP_MODE_UNSPECIFIED',
            },
            'clientScreen': 'EMBED',
        },
        'user': {
            'lockedSafetyMode': False,
        },
        'request': {
            'useSsl': True,
            'internalExperimentFlags': [],
            'consistencyTokenJars': [],
        },
        'thirdParty': {
            'embeddedPlayerContext': {
                'embeddedPlayerEncryptedContext': 'AD5ZzFQ8Ad4WfIONAn5b_Ish5-WAsg4cY0mFQ-JYlsEmGm6o6qremuI8Hr91_eKFvya4usrjmoWQ9-ByAx_Fxb4X2-cp_ZAGsrrSeTDRSf1ueSagA1HLNxZ-2AWuBri3IRVRj4KG3dAUVTvBdomZBX1Ng1gk39UPhxg',
                'ancestorOriginsSupported': False,
                'ancestorOrigins': [
                    'https://www.cxtvlive.com',
                ],
                'autoplayBrowserPolicy': 'AUTOPLAY_BROWSER_POLICY_UNSPECIFIED',
                'autoplayIntended': True,
                'autoplayStatus': 'AUTOPLAY_STATUS_UNAVAILABLE',
            },
            'embedUrl': 'https://www.cxtvlive.com/',
        },
        'clientScreenNonce': 'CG6z5QsuBskeMULX',
        'adSignalsInfo': {
            'params': [
                {
                    'key': 'dt',
                    'value': '1753697018696',
                },
                {
                    'key': 'flash',
                    'value': '0',
                },
                {
                    'key': 'frm',
                    'value': '2',
                },
                {
                    'key': 'u_tz',
                    'value': '480',
                },
                {
                    'key': 'u_his',
                    'value': '8',
                },
                {
                    'key': 'u_h',
                    'value': '960',
                },
                {
                    'key': 'u_w',
                    'value': '1707',
                },
                {
                    'key': 'u_ah',
                    'value': '960',
                },
                {
                    'key': 'u_aw',
                    'value': '1707',
                },
                {
                    'key': 'u_cd',
                    'value': '24',
                },
                {
                    'key': 'bc',
                    'value': '31',
                },
                {
                    'key': 'bih',
                    'value': '-12245933',
                },
                {
                    'key': 'biw',
                    'value': '-12245933',
                },
                {
                    'key': 'brdim',
                    'value': '834,12,834,12,1707,0,810,966,706,411',
                },
                {
                    'key': 'vis',
                    'value': '1',
                },
                {
                    'key': 'wgl',
                    'value': 'true',
                },
                {
                    'key': 'ca_type',
                    'value': 'image',
                },
            ],
        },
        'clickTracking': {
            'clickTrackingParams': 'CAAQru4BIhMIw5mmvabfjgMVOmtMCB0Y8SWb',
        },
    },
    'playbackContext': {
        'contentPlaybackContext': {
            'html5Preference': 'HTML5_PREF_WANTS',
            'lactMilliseconds': '40',
            'referer': 'https://www.youtube.com/embed/Cy0s_bxzqkw?autoplay=true',
            'signatureTimestamp': 20292,
            'autoCaptionsDefaultOn': False,
            'autoplay': True,
            'mdxContext': {},
            'playerWidthPixels': 706,
            'playerHeightPixels': 411,
            'ancestorOrigins': [
                'https://www.cxtvlive.com',
            ],
            'encryptedHostFlags': 'AD5ZzFQeoFFOlFOrukfDTLq97ofgR-rtJlTGDlt3zEacPu58dZE0y5TbhTVcx05GLOl1OykgtME8UP2eijrSpZdbggTvPjocLY-aYZAd5nnNInGoRaHmMnVdmTG6OUsXEjlicFdyaH8CJq6WMhw6PKagOPXnTzvtNA',
        },
        'devicePlaybackCapabilities': {
            'supportsVp9Encoding': True,
            'supportXhr': True,
        },
    },
    'cpn': '6Yvg_DVK10J3B255',
    'serializedThirdPartyEmbedConfig': '{}',
    'captionParams': {},
    'serviceIntegrityDimensions': {
        'poToken': 'IgisnKyexBvmZg==',
    },
}

response = requests.post(
    'https://www.youtube.com/youtubei/v1/player',
    params=params,
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"videoId":"Cy0s_bxzqkw","context":{"client":{"hl":"en","gl":"BR","remoteHost":"154.205.156.51","deviceMake":"","deviceModel":"","visitorData":"Cgs0YUdLeklaeEdFNCj3lZ3EBjIKCgJCUhIEGgAgYw%3D%3D","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36,gzip(gfe)","clientName":"WEB_EMBEDDED_PLAYER","clientVersion":"1.20250722.00.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/embed/Cy0s_bxzqkw?autoplay=true","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CPeVncQGEParsAUQipeAExCHrM4cEMXLzxwQ78TPHBDT4a8FEPa6zxwQ9svPHBDds88cEJmYsQUQ_M7PHBDJ968FEPyyzhwQqZmAExCZjbEFEIGzzhwQvbauBRDOrM8cELCGzxwQzMDPHBC9irAFEOLKzxwQvZmwBRCU_rAFELjkzhwQ8sTPHBCly88cEMfIzxwQt-r-EhCJsM4cEAAQ4cvPHBDjvs8cELnZzhwQioKAExDa984cEJi5zxwQiIewBRDKys8cEJLRzxwQ3rzOHBCBzc4cEOq7zxwQ8JywBRCe0LAFEMXDzxwQn6HPHBCI468FEJOGzxwQu9nOHBCvj_8SEMzfrgUQ8OLOHBDmxc8cEKTPzxwqHENBTVNEeFVNLVpxLURPSGRoUXJMM0E0ZEJ3PT0%3D"},"browserName":"Chrome","browserVersion":"138.0.0.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7","deviceExperimentId":"ChxOelV6TWpBM01UTXlOekl3TmprM05qRTBNZz09EPeVncQGGPeVncQG","rolloutToken":"CKjCjYS_ouy--gEQsLKfvabfjgMYsLKfvabfjgM%3D","screenWidthPoints":706,"screenHeightPoints":411,"screenPixelDensity":2,"screenDensityFloat":1.5,"utcOffsetMinutes":480,"userInterfaceTheme":"USER_INTERFACE_THEME_LIGHT","connectionType":"CONN_CELLULAR_3G","timeZone":"Asia/Shanghai","playerType":"UNIPLAYER","tvAppInfo":{"livingRoomAppMode":"LIVING_ROOM_APP_MODE_UNSPECIFIED"},"clientScreen":"EMBED"},"user":{"lockedSafetyMode":false},"request":{"useSsl":true,"internalExperimentFlags":[],"consistencyTokenJars":[]},"thirdParty":{"embeddedPlayerContext":{"embeddedPlayerEncryptedContext":"AD5ZzFQ8Ad4WfIONAn5b_Ish5-WAsg4cY0mFQ-JYlsEmGm6o6qremuI8Hr91_eKFvya4usrjmoWQ9-ByAx_Fxb4X2-cp_ZAGsrrSeTDRSf1ueSagA1HLNxZ-2AWuBri3IRVRj4KG3dAUVTvBdomZBX1Ng1gk39UPhxg","ancestorOriginsSupported":false,"ancestorOrigins":["https://www.cxtvlive.com"],"autoplayBrowserPolicy":"AUTOPLAY_BROWSER_POLICY_UNSPECIFIED","autoplayIntended":true,"autoplayStatus":"AUTOPLAY_STATUS_UNAVAILABLE"},"embedUrl":"https://www.cxtvlive.com/"},"clientScreenNonce":"CG6z5QsuBskeMULX","adSignalsInfo":{"params":[{"key":"dt","value":"1753697018696"},{"key":"flash","value":"0"},{"key":"frm","value":"2"},{"key":"u_tz","value":"480"},{"key":"u_his","value":"8"},{"key":"u_h","value":"960"},{"key":"u_w","value":"1707"},{"key":"u_ah","value":"960"},{"key":"u_aw","value":"1707"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"-12245933"},{"key":"biw","value":"-12245933"},{"key":"brdim","value":"834,12,834,12,1707,0,810,966,706,411"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]},"clickTracking":{"clickTrackingParams":"CAAQru4BIhMIw5mmvabfjgMVOmtMCB0Y8SWb"}},"playbackContext":{"contentPlaybackContext":{"html5Preference":"HTML5_PREF_WANTS","lactMilliseconds":"40","referer":"https://www.youtube.com/embed/Cy0s_bxzqkw?autoplay=true","signatureTimestamp":20292,"autoCaptionsDefaultOn":false,"autoplay":true,"mdxContext":{},"playerWidthPixels":706,"playerHeightPixels":411,"ancestorOrigins":["https://www.cxtvlive.com"],"encryptedHostFlags":"AD5ZzFQeoFFOlFOrukfDTLq97ofgR-rtJlTGDlt3zEacPu58dZE0y5TbhTVcx05GLOl1OykgtME8UP2eijrSpZdbggTvPjocLY-aYZAd5nnNInGoRaHmMnVdmTG6OUsXEjlicFdyaH8CJq6WMhw6PKagOPXnTzvtNA"},"devicePlaybackCapabilities":{"supportsVp9Encoding":true,"supportXhr":true}},"cpn":"6Yvg_DVK10J3B255","serializedThirdPartyEmbedConfig":"{}","captionParams":{},"serviceIntegrityDimensions":{"poToken":"IgisnKyexBvmZg=="}}'
#response = requests.post('https://www.youtube.com/youtubei/v1/player', params=params, cookies=cookies, headers=headers, data=data)