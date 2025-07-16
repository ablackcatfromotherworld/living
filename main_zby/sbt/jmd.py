import requests
import datetime
from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Actions
from pathlib import Path
import parsel
import codecs
import json
import time

headers = {
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRpZ2l0YWwtc2J0IiwiZW5kcG9pbnRzIjpbIioiXSwiaG9zdHMiOlsiKiJdLCJzZXJ2aWNlcyI6WyIqIl0sImlhdCI6MTY4MzkwOTkyOX0.RpQCLWNz9jib1K4rzx3fefxBp5H69NrpJ-3qFXiNCio',
}

def get_param(i):

    params = {
    'datagrade': i,
    'limit': '100',
    }
    return params

time_now = datetime.datetime.now()
times = [(time_now + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0,7)]
path = Path(__file__).parent
data_sbt = []
for i in times:
    timeline = []
    response = requests.get('https://content.sbt.com.br/api/programgrade', params=get_param(i), headers=headers).json()
    for result in response.get('results'):
        timeline.append({'title':result.get('title'), 'startdate': result.get('startdate'), 'description':result.get('description'), 'thumbnail':result.get('thumbnail')})

    data_sbt.append({i:timeline})

with open(path / 'sbt.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data_sbt))