import requests
import execjs
import parsel
from pathlib import Path
import re
import json5
import json
import uuid

cookies = {
     'panoramaId_expiry': f'{execjs.compile("return new Date().getTime()").call("this")}',
}

headers = {'authorization': 'Bearer 17f2f046e16a2e1d213d2e4d16660be7f70744c416361734431614952625272305361727732337872586450734846324c4552484e553035666857667436597a69506c432d63586a4e6f614e385947333864386e785f41505043783347493035426e5741574a513d3d3a303a75346f6b366d6b6e30663362316a717031723334'
    }

random_uuid = uuid.uuid4()
path = Path(__file__).parent
json_data = {
    'player_type': 'desktop',
    'video_id': '12136724',
    'quality': 'max',
    'content_protection': 'widevine',
    'vsid': str(random_uuid),
    'tz': '+08:00',
    'capabilities': {
        'low_latency': True,
        'smart_mosaic': True,
        'dvr': True,
    },
    'consumption': 'streaming',
    'metadata': {
        'name': 'web',
        'device': {
            'type': 'desktop',
            'os': {},
        },
    },
    'version': 2,
}

response = requests.post('https://playback.video.globo.com/v4/video-session', cookies=cookies,  json=json_data, headers=headers)
video_session = response.json()
with open(path/'video_session.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(video_session))


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"player_type":"desktop","video_id":"4452349","quality":"max","content_protection":"widevine","vsid":"441b6ddb-7e79-e08a-5e6c-8ac92929c83c","tz":"+08:00","capabilities":{"low_latency":true,"smart_mosaic":true,"dvr":true},"consumption":"streaming","metadata":{"name":"web","device":{"type":"desktop","os":{}}},"version":2}'
#response = requests.post('https://playback.video.globo.com/v4/video-session', cookies=cookies, headers=headers, data=data)