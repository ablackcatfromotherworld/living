import requests
import execjs
import hashlib
import parsel
from pathlib import Path
import re
import json5
import json
import uuid
import datetime


sha256_hash = hashlib.sha256()
sha256_hash.update('123456'.encode('utf-8'))
hex_digest = sha256_hash.hexdigest()

sha256_hash = hashlib.sha256()
today = datetime.date.today()
headers = {
    'x-platform-id': 'web',
    'Referer': 'https://globoplay.globo.com/',
    'x-device-id': 'desktop',
    'x-hsid': str(uuid.uuid4()),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'accept': '*/*',
    'x-client-version': today.strftime('%Y.%m-%d'),
}

params = {
    'operationName': 'getBroadcastList',
    'variables': '{"epgSlotsLimit":20,"filtersInput":{"affiliateCode":"RJ"}}',
    'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"2e7cfff6ec815f0c5c828a4e273ab57475ab4d48dd8a58e6b0bcfb0ad028f188"}}',
}
path = Path(__file__).parent
graphql = []
broadcasts = requests.get('https://cloud-jarvis.globo.com/graphql', params=params, headers=headers).json().get('data').get('broadcasts')
for broadcast in broadcasts:
    mediaId = broadcast.get('mediaId')
    name = broadcast.get('name')
    description = broadcast.get('customSEOMetadata').get('description') if broadcast.get('customSEOMetadata') else ''
    img_cover = broadcast.get('imageOnAir')
    withoutDVRMediaId = broadcast.get('withoutDVRMediaId')
    slug = broadcast.get('slug')
    channel_ref = broadcast.get('channel').get('id')
    categories = broadcast.get('categories')[0].get('slug')
    subscriptionServices_id = broadcast.get('media').get('subscriptionServices')[0].get('id') if broadcast.get('media').get('subscriptionServices') else ''
    # print(len(broadcast.get('epgCurrentSlots')))

    graphql.append({
        'mediaId':mediaId,
        'name' : name,
        'description':description,
        'img_cover':img_cover,
        'withoutDVRMediaId':withoutDVRMediaId,
        'slug':slug,
        'channel_ref':channel_ref,
        'categories': categories,
        'subscriptionServices_id' : subscriptionServices_id
    })
with open(path/'graphql.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(graphql))
