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

headers = {

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

def get_param(i):

    params = {
        'data':i
    }
    return params

time_now = datetime.datetime.now()
days_since_monday = time_now.weekday()
time_now -= datetime.timedelta(days=days_since_monday)
times = [(time_now + datetime.timedelta(days=i)).strftime("%d-%m-%Y") for i in range(0,7)]
path = Path(__file__).parent
data_Aparecida = []
for i in times:
    timeline = []
    response = requests.get('https://www.a12.com/tv/programacao', params=get_param(i), headers=headers)
    selector = parsel.Selector(response.text)
    list_programs = selector.xpath('//ul[@class="schedule__list"]/li')
    for ul in list_programs:
        img = ul.xpath('./div[@class="program__img"]/img/@src').get()
        time = ul.xpath('./div[@class="program__time"]/text()').get().strip()
        main_title = ul.xpath('.//span[@class="program__title"]/text()').get() or ul.xpath('./div[@class="program__info"]/a/text()').get()
        subtitle = ul.xpath('.//span[@class="program__subtitle"]/text()').get()
        if subtitle:
            title = main_title + subtitle
        else:
            title = main_title
        timeline.append({'title':title, 'time':time, 'img':img})
    data_Aparecida.append({i:timeline})



with open(path / 'Aparecida.json', 'w', encoding='utf-8') as f:
    ujson.dump(data_Aparecida, f)