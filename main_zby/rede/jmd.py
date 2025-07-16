import requests
import time
import datetime
from pathlib import Path
import execjs
import parsel
import html
import ujson
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_param(i):

    params = {
    'dia': i,
    '_': execjs.compile('return new Date().getTime();').call('this'),
    }
    return params

time_now = datetime.datetime.now()
days_since_monday = time_now.weekday()
time_now -= datetime.timedelta(days=days_since_monday)
times = [(time_now + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0,7)]
path = Path(__file__).parent
data_sbt = []
for i in times:
    timeline = []
    response = requests.get('https://www.redetv.uol.com.br/Programacao', params=get_param(i))
    selector = parsel.Selector(response.text)
    list_programs = selector.xpath('//ul[@class="list-programs"]/li')
    for ul in list_programs:
        img = ul.xpath('./div[@class="img-wrap"]/img/@src').get()
        time = ul.xpath('./span/text()').get()
        title = html.unescape(ul.xpath('./h4/text()').get())
        timeline.append({'title':title, 'time':time, 'img':img})
    data_sbt.append({i:timeline})



with open(path / 'rede.json', 'w', encoding='utf-8') as f:
    ujson.dump(data_sbt, f)