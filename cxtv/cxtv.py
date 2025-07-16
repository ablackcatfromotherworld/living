import subprocess
import requests
import json
import re
import schedule
import parsel
from DrissionPage import Chromium
from DrissionPage.common import Settings
import logging
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean, Float, ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
base = declarative_base()
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/movie')
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



class CXTV():
    def __init__(self):
        self.cookies = {
            '_gid': 'GA1.3.115383137.1750156862',
            'PHPSESSID': '58tc0ubin681qn8qp5egq2ac7u',
            'cf_clearance': 'KcD.UFSKgHKJQwhVxZwMjJkXGnecuiEQ7Bnm7JUEb3Y-1750228744-1.2.1.1-utXRXmPY3iCCQORnGbY0IJT6pczgBYkGh.wvpdTWwpiKuP2nyCMUZKy0h9W.pnPBbBml2jFn6TaDtkYWDZ4GjIKqHVgX5BdrL0qtvRIYt52on.VYPj69wJuZ4RLm4tY4JMwOD_inOP5QVJ9js0sZbaudb7Y44tMAutBMI81dIROzBSLfqXGl6ZZjzHfqDSRjq9J6bPeDFctJsxKlyHG8aszJ4sewzCZ4n75YkTqKBTeCrlDmr2wUHppMQD3wkJt5J0PdHMUK6JT5wPByfYHo5OUm1rtGfjkp.3_FZW_DYSkP6kgEwqzMLlo1HY1R.R_mEZJbR0wwMDTOhnUBvI_td8mpV0Dy1C04K2tnDtfHlBw',
            '_ga': 'GA1.1.1840867124.1750156862',
            'FCNEC': '%5B%5B%22AKsRol9nn7LkYKUABWGUGn7mslCOITKWAxVl06uZZc4h_s9cP6tWNg1q5MiTPDjkEvgmKTb-4LpH7-KYNBNzzuhO8tPN5DJgsRFPSpnvH4Vr9HmK-HOiq_Sa8_vAxczj1rPpsSoWqnVbT1YbGNJOnRbdrtGRu_yWlA%3D%3D%22%5D%5D',
            '__gads': 'ID=bf1b400fb06a3947:T=1750156864:RT=1750228746:S=ALNI_MZ28HqulQz9uoXTbvFG1HQCK-WDxw',
            '__gpi': 'UID=0000110570906949:T=1750156864:RT=1750228746:S=ALNI_MafzYURyKm1pl3ARU7fR7Izt1L1fw',
            '__eoi': 'ID=af43358ba290696b:T=1750156864:RT=1750228746:S=AA-AfjanN5-VVBbslx3QEiiubELv',
            '_ga_802KDW3REV': 'GS2.1.s1750226229$o5$g1$t1750228752$j53$l0$h0',
        }
        self.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.cxtv.com.br/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"137.0.7151.104"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="137.0.7151.104", "Chromium";v="137.0.7151.104", "Not/A)Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'cookie': '_gid=GA1.3.115383137.1750156862; PHPSESSID=58tc0ubin681qn8qp5egq2ac7u; cf_clearance=KcD.UFSKgHKJQwhVxZwMjJkXGnecuiEQ7Bnm7JUEb3Y-1750228744-1.2.1.1-utXRXmPY3iCCQORnGbY0IJT6pczgBYkGh.wvpdTWwpiKuP2nyCMUZKy0h9W.pnPBbBml2jFn6TaDtkYWDZ4GjIKqHVgX5BdrL0qtvRIYt52on.VYPj69wJuZ4RLm4tY4JMwOD_inOP5QVJ9js0sZbaudb7Y44tMAutBMI81dIROzBSLfqXGl6ZZjzHfqDSRjq9J6bPeDFctJsxKlyHG8aszJ4sewzCZ4n75YkTqKBTeCrlDmr2wUHppMQD3wkJt5J0PdHMUK6JT5wPByfYHo5OUm1rtGfjkp.3_FZW_DYSkP6kgEwqzMLlo1HY1R.R_mEZJbR0wwMDTOhnUBvI_td8mpV0Dy1C04K2tnDtfHlBw; _ga=GA1.1.1840867124.1750156862; FCNEC=%5B%5B%22AKsRol9nn7LkYKUABWGUGn7mslCOITKWAxVl06uZZc4h_s9cP6tWNg1q5MiTPDjkEvgmKTb-4LpH7-KYNBNzzuhO8tPN5DJgsRFPSpnvH4Vr9HmK-HOiq_Sa8_vAxczj1rPpsSoWqnVbT1YbGNJOnRbdrtGRu_yWlA%3D%3D%22%5D%5D; __gads=ID=bf1b400fb06a3947:T=1750156864:RT=1750228746:S=ALNI_MZ28HqulQz9uoXTbvFG1HQCK-WDxw; __gpi=UID=0000110570906949:T=1750156864:RT=1750228746:S=ALNI_MafzYURyKm1pl3ARU7fR7Izt1L1fw; __eoi=ID=af43358ba290696b:T=1750156864:RT=1750228746:S=AA-AfjanN5-VVBbslx3QEiiubELv; _ga_802KDW3REV=GS2.1.s1750226229$o5$g1$t1750228752$j53$l0$h0',
        }
        self.url = 'https://www.cxtv.com.br/tv'

    # def get_categories(self):
    #     response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
    #     html = parsel.Selector(response.text)
    #     categories = html.xpath('//a[@class="m-b-20 btn btn-white btn-block padding-20"]/@href').getall()
    #     return categories

    def get_categories(self):
        tab = Chromium().latest_tab
        tab.get(self.url)
        elements = tab.eles('x://a[@class="m-b-20 btn btn-white btn-block padding-20"]')
        categories = []
        for element in elements:
            categories.append(element.attr('href'))
        # categories = ['https://www.cxtv.com.br/tv/categorias/carros']
        return {'categories': categories, 'tab': tab}

    def get_details(self):
        details = []
        categories, tab = self.get_categories().values()
        for detail in categories:
            tab.get(detail)
            logging.info(f'正在处理{detail}')
            while tab.ele('x://div[@id="loadMore"]'):
                if loadMore := tab.ele('x://div[@id="loadMore"]'):
                    loadMore.click()
                    tab.wait(1)
            logging.info(f'翻页完成{detail}')
            detail_urls = tab.eles('x://a[@class="m-b-20 btn btn-white btn-block"]')
            for detail_url in detail_urls:
                detail_url = detail_url.attr('href')
                details.append(detail_url)
        return {'details': details, 'tab': tab}

    def get_m3u8_url(self):
        m3u8_urls = []
        details, tab = self.get_details().values()
        m3u8_count = 0
        for i in range(len(details)):
            logging.info(f"正在处理第{i+1}个详情页")
            detail = details[i]
            tab.get(detail)
            if m3u8_url := tab.ele('x://section[@class="video bg-silver b-radius-5 padding-5"]//source'):
                if m3u8_url := m3u8_url.attr('src'):
                    m3u8_count += 1
                    logging.info(f"获取到{m3u8_count}个m3u8")
                    name = tab.ele('x://h1').text
                    category = tab.ele('x://*[@id="page-stream"]/div/div/div[1]/div[1]/div[2]/div[2]/a[1]').text
                    profile = tab.ele('x://*[@id="page-stream"]/div/div/div[1]/span').text
                    country_img = tab.ele('x://*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]/a[1]/img').attr('src')
                    country = tab.ele('x://*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]/a[1]').text
                    areas = tab.ele('x://*[@id="page-stream"]/div/div/div[1]/div[5]/div/div[1]').text
                    img_cover = tab.ele('x://img[@class="b-radius-5"]').attr('src')
                    m3u8_urls.append({'name': name, 'category':category ,'areas': areas, 'country': country, 'profile': profile,'country_img': country_img,  'img_cover': img_cover, 'm3u8_url': m3u8_url})
                else:
                    continue
            else:
                continue
        return m3u8_urls

    def get_useful_m3u8_urls(self):
        m3u8_urls = self.get_m3u8_url()
        m3u8_useful_urls = []
        for i in range(len(m3u8_urls)):
            m3u8_url = m3u8_urls[i]
            logging.info(f'正在处理第{i+1}个m3u8链接：{m3u8_url['m3u8_url']}')
            try:
                data = subprocess.run(
                    ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", f"{m3u8_url['m3u8_url']}"],
                    capture_output=True, timeout=60
                ).stdout.decode()
            except subprocess.TimeoutExpired:
                logging.warning(f"ffprobe 检查超时，跳过：{m3u8_url['m3u8_url']}")
                continue
            except Exception as e:
                logging.warning(f"ffprobe 检查异常，跳过：{m3u8_url['m3u8_url']}，错误：{e}")
                continue

            data_json = json.loads(data)
            logging.info(f"data_json: {data_json}")
            if data_json != {}:
                try:
                    if data_json['streams'][1]['codec_name'] == 'h264':
                        codec_name = data_json['streams'][1]['codec_name']
                        width = data_json['streams'][1].get('coded_width', 0) or data_json['streams'][1].get('width', 0)
                        height = data_json['streams'][1].get('coded_height', 0) or data_json['streams'][1].get('height', 0)
                        variant_bitrate = data_json['streams'][1]['tags']['variant_bitrate'] or 0
                        logging.info(f"m3u8_url: {m3u8_url['m3u8_url']}, codec_name: {codec_name}, width: {width}, height: {height}, variant_bitrate: {variant_bitrate}")
                        if codec_name == 'h264' and height >= 720 and int(variant_bitrate) >= 1000000:
                            m3u8_url.update({'codec_name': codec_name, 'width': width, 'height': height,
                                            'variant_bitrate': variant_bitrate})
                            m3u8_useful_urls.append(m3u8_url)
                    else:
                        highest_quality_stream  = self.find_best_video_stream(data_json)
                        codec_name = highest_quality_stream.get('codec_name')
                        height = highest_quality_stream.get('height')
                        width = highest_quality_stream.get('width')
                        variant_bitrate = highest_quality_stream.get('tags').get('variant_bitrate')
                        logging.info(f"m3u8_url: {m3u8_url['m3u8_url']}, codec_name: {codec_name}, width: {width}, height: {height}, variant_bitrate: {variant_bitrate}")
                        if codec_name == 'h264' and height >= 720 and int(variant_bitrate) >= 1000000:
                            m3u8_url.update({'codec_name': codec_name, 'width': width, 'height': height,
                                            'variant_bitrate': variant_bitrate})
                            m3u8_useful_urls.append(m3u8_url)
                except Exception as e:
                    logging.info(f"m3u8_url: {m3u8_url['m3u8_url']}解析有误！！！！！")
                    continue
            else:
                continue

        return m3u8_useful_urls
    
    @staticmethod
    def find_best_video_stream(data_json):
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

    def upload_mysql(self, batch_size=100):
        m3u8_urls = self.get_useful_m3u8_urls()
        with Session() as db:
            for i in range(0, len(m3u8_urls), batch_size):
                batch = m3u8_urls[i:i+batch_size]
                try:
                    db.bulk_insert_mappings(CXTV_live_streaming, batch)
                    db.commit()
                    logging.info(f"成功上传第{i//batch_size+1}批，共{len(batch)}条数据")
                except Exception as e:
                    db.rollback()
                    logging.error(f"上传第{i//batch_size+1}批数据失败，错误：{e}")

    @staticmethod
    def my_task():
        current_time = datetime.datetime.now()
        logging.info(f"开始执行任务，当前时间: {current_time}")

    # 让程序在每次检查后暂停一秒，是为了避免CPU占用过高，导致其他任务无法正常执行
    # def run(self):
    #     self.my_task()
    #     schedule.every(3).hours.do(self.upload_mysql)

        # schedule.every(3).hours.do(self.get_m3u8_url)  # 每三小时执行一次
        # 这一步只负责安排计划，不负责执行计划
        # schedule.every().day.at("10:30").do(self.my_task)  # 每天10：30执行
        # schedule.every().monday.at("09:00").do(self.my_task, name='wnhmsy') # 每周一9：00执行
        # schedule.every(5).to(10).minutes.do(self.my_task)  # 每5到10分钟执行一次

    # def main(self):
    #     """
    #     主函数，用于启动定时任务
    #     schedule.run_pending() :检查当前所有待处理的任务，判断是否有任务的执行时间已到。如果时间到了，就立即执行任务
    #     :return:
    #     """
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)


if __name__ == '__main__':
    cxtv = CXTV()
    categories = cxtv.upload_mysql()
