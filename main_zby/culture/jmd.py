import parsel.selector
import requests
import time
import datetime
from pathlib import Path
import execjs
import parsel
import html
import ujson
from urllib.parse import urljoin
import ujson
path = Path(__file__).parent

_url = 'https://cultura.uol.com.br/grade/'
response = requests.get(_url).text
base_url = 'https://cultura.uol.com.br'
selector = parsel.Selector(response)
lis = selector.xpath('//section[@class="content"]//li')
urls = {'urls': [base_url + i.xpath('./a/@href').get() for i in lis], 'date':[i.xpath('./a/@data-title').get() for i in lis]}
data_culture = []
for date, url in zip(urls['date'], urls['urls']):
    response = requests.get(url=url).text
    selector = parsel.Selector(response)
    sections = selector.xpath('//section[@class="programas"]/section')
    data_ = []
    for section in sections:
        img = section.xpath('./div/a/img/@src').get()
        time = section.xpath('./div/a/time/text()').get()
        title = section.xpath('./div/h3/a/text()').get()
        profile = section.xpath('./section[@class="mais"]/section/div/text()').get().strip()
        data_.append({'title':title, 'time':time, 'img':img, 'profile':profile})
    data_culture.append({date: data_})

with open(path / 'globo.jaon', 'w', encoding='utf-8') as f:
    ujson.dump(data_culture, f)