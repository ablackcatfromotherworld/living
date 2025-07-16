import requests
from pathlib import Path
import logging
import subprocess
import time 
import functools
from datetime import datetime
import backoff 
import json
import csv
import asyncio
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, ForeignKey, BigInteger, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
Base = declarative_base()
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/movie')
Session = sessionmaker(bind=engine)


class TVBRAIL(Base):

    __tablename__ = 'tvbrail'

    id_episodio = Column(Integer, nullable=False, primary_key=True)
    nm_episodio = Column(String(255), nullable=False)
    id_midia = Column(Integer, nullable=False)
    nm_genero = Column(String(255), nullable=False)
    ds_sinopse = Column(Text, nullable=False)
    ds_caminho_capa_horizontal = Column(String(255), nullable=False)
    ds_caminho_capa_vertical = Column(String(255), nullable=False)
    m3u8_url = Column(String(255), nullable=False)
    codec_name = Column(String(255), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    variant_bitrate = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

class TVBRAIL_M3U8():
    def __init__(self):
        self.cookies = {
            '_ga': 'GA1.1.880391425.1750043858',
        '_ga_E0BYEPL16T': 'GS2.1.s1750043987$o1$g1$t1750044065$j43$l0$h0',
        '__gads': 'ID=cebc2d3e337d21ef:T=1750043865:RT=1751425048:S=ALNI_MYK9JiY7_4N8a1FJ8rBIL4J8eC-nw',
        '__gpi': 'UID=000011052525fdf0:T=1750043865:RT=1751425048:S=ALNI_MYm1pkjjZKgxfGFp5Mz_Oou4-ggxg',
        '__eoi': 'ID=075108d65a1ce47a:T=1750043865:RT=1751425048:S=AA-AfjaRhnqUx5b5aYeIzpHAVoTc',
        '_ga_0SNLMPXB24': 'GS2.1.s1751425044$o5$g1$t1751425126$j41$l0$h0',
        '_ga_TGW7R30M20': 'GS2.1.s1751425046$o5$g1$t1751425126$j41$l0$h1644060216',
        '_ga_E7XFVGNNPX': 'GS2.1.s1751447386$o2$g1$t1751448182$j60$l0$h0',
    }

        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://play.ebc.com.br/programas/68/episodios/9885/samba-na-gamboa',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            # 'cookie': '_ga=GA1.1.880391425.1750043858; _ga_E0BYEPL16T=GS2.1.s1750043987$o1$g1$t1750044065$j43$l0$h0; __gads=ID=cebc2d3e337d21ef:T=1750043865:RT=1751425048:S=ALNI_MYK9JiY7_4N8a1FJ8rBIL4J8eC-nw; __gpi=UID=000011052525fdf0:T=1750043865:RT=1751425048:S=ALNI_MYm1pkjjZKgxfGFp5Mz_Oou4-ggxg; __eoi=ID=075108d65a1ce47a:T=1750043865:RT=1751425048:S=AA-AfjaRhnqUx5b5aYeIzpHAVoTc; _ga_0SNLMPXB24=GS2.1.s1751425044$o5$g1$t1751425126$j41$l0$h0; _ga_TGW7R30M20=GS2.1.s1751425046$o5$g1$t1751425126$j41$l0$h1644060216; _ga_E7XFVGNNPX=GS2.1.s1751447386$o2$g1$t1751448182$j60$l0$h0',
        }

        self.path = Path(__file__).parent

    async def get_id(self):
        params = {
            'geo': 'true',
            'limit': '1000',
            'sort': 'populares',
            'order': 'desc',
            'idade': '18',
        }

        response = requests.get('https://play.ebc.com.br/v2/conteudos/populares', params=params, cookies=self.cookies, headers=self.headers)
        a = set()
        for item in response.json():
            a.add(item.get('id_conteudo'))
        return a

    async def get_episodios(self, i: Optional[int]=None):
        params = {
            'geo': 'true',
            'limit': '100',
            'sort': 'nr_episodio',
            'order': 'asc',
        }
        try:
            response = requests.get(f'https://play.ebc.com.br/v2/conteudos/{i}/episodios', params=params, cookies=self.cookies, headers=self.headers)
            data = []
            for episodios in response.json().get('temporada'):
                for episodio in episodios.get('episodios'):
                    id_episodio = episodio.get('id_episodio')
                    nm_episodio = episodio.get('nm_episodio')
                    id_midia = episodio.get('id_midia')
                    nm_genero = episodio.get('nm_genero')
                    ds_sinopse = episodio.get('ds_sinopse')
                    ds_caminho_capa_horizontal = episodio.get('ds_caminho_capa_horizontal')
                    ds_caminho_capa_vertical = episodio.get('ds_caminho_capa_vertical')
                    cd_identificador = episodio.get('cd_identificador')
                    data.append({
                        'id_episodio': id_episodio,
                        'nm_episodio': nm_episodio,
                        'id_midia': id_midia,
                        'nm_genero': nm_genero,
                        'ds_sinopse': ds_sinopse,
                        'ds_caminho_capa_horizontal': ds_caminho_capa_horizontal,
                        'ds_caminho_capa_vertical': ds_caminho_capa_vertical,
                        'm3u8_url': f"https://videos.ebc.com.br/play/{cd_identificador}/hls/master.m3u8"
                        })
            return data
        except Exception as e:
            logging.warning(f"获取第{i}集数据失败，错误：{e}")
            return []

    # def save_csv(self, data: list):
    #     fieldnames = ['id_episodio', 'nm_episodio', 'nm_genero', 'm3u8_url']
    #     with open(self.path / 'tvbrail.csv', 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.DictWriter(f, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerows(data)

    async def is_useful(self, item: object):
        
        try:
            data = subprocess.run(
                ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", f"{item['m3u8_url']}"],
                capture_output=True, timeout=60
            ).stdout.decode()
        except subprocess.TimeoutExpired:
            logging.warning(f"ffprobe 检查超时，跳过：{item['m3u8_url']}")
            return None
        except Exception as e:
            logging.warning(f"ffprobe 检查异常，跳过：{item['m3u8_url']}，错误：{e}")
            return None

        data_json = json.loads(data)
        # logging.info(f"data_json: {data_json}")
        if data_json != {}:
            try:
                if data_json['streams'][1]['codec_name'] == 'h264':
                    codec_name = data_json['streams'][1]['codec_name']
                    width = data_json['streams'][1].get('coded_width', 0) or data_json['streams'][1].get('width', 0)
                    height = data_json['streams'][1].get('coded_height', 0) or data_json['streams'][1].get('height', 0)
                    variant_bitrate = data_json['streams'][1]['tags']['variant_bitrate'] or 0
                    logging.info(f"m3u8_url: {item['m3u8_url']}, codec_name: {codec_name}, width: {width}, height: {height}, variant_bitrate: {variant_bitrate}")
                    if codec_name == 'h264' and height >= 720 and int(variant_bitrate) >= 1000000:
                        item.update({'codec_name': codec_name, 'width': width, 'height': height,
                                        'variant_bitrate': variant_bitrate})
                        return item
                else:
                    highest_quality_stream  = self.find_best_video_stream(data_json)
                    codec_name = highest_quality_stream.get('codec_name')
                    height = highest_quality_stream.get('height')
                    width = highest_quality_stream.get('width')
                    variant_bitrate = highest_quality_stream.get('tags').get('variant_bitrate')
                    logging.info(f"m3u8_url: {item['m3u8_url']}, codec_name: {codec_name}, width: {width}, height: {height}, variant_bitrate: {variant_bitrate}")
                    if codec_name == 'h264' and height >= 720 and int(variant_bitrate) >= 1000000:
                        item.update({'codec_name': codec_name, 'width': width, 'height': height,
                                        'variant_bitrate': variant_bitrate})
                        return item
                    
            except Exception as e:
                logging.info(f"m3u8_url: {item['m3u8_url']}解析有误！！！！！")
                return None
        else:
            return None
        
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
    

    async def save_mysql(self, data: list, batch_size=100):
        try:
            with Session() as db:
                for i in range(0, len(data), batch_size):
                    batch = data[i:i+batch_size]
                    db.bulk_insert_mappings(TVBRAIL, batch)
                    db.commit()
                    logging.info(f"成功上传第{i//batch_size+1}批，共{len(batch)}条数据")
        except Exception as e:
            db.rollback()
            logging.error(f"上传第{i//batch_size+1}批数据失败，错误：{e}")

    async def my_task(self):
        m3u8_urls = []
        id_list = await self.get_id()
        count = 0
        for i in id_list:
            data = await self.get_episodios(i)
            if data:
                for item in data:
                    m3u8_url = await self.is_useful(item)
                    if m3u8_url:
                        m3u8_urls.append(m3u8_url)
                    count += 1
                    logging.info(f"已处理{count}条数据")
        await self.save_mysql(m3u8_urls)


if __name__ == '__main__':
    asyncio.run(TVBRAIL_M3U8().my_task())

