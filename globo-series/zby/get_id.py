import requests
import execjs
import parsel
from pathlib import Path
import re
import json5
import json

cookies = {
     'panoramaId_expiry': f'{execjs.compile("return new Date().getTime()").call("this")}',
}


path = Path(__file__).parent
response = requests.get('https://globoplay.globo.com/tv-globo/ao-vivo/6120663/', cookies=cookies)
selector = parsel.Selector(response.text)
quicksilver_string = selector.xpath('//script[@type="application/javascript"]/text()').get()
start = quicksilver_string.find('{')
end = quicksilver_string.rfind('}')
quicksilver = quicksilver_string[start:end+1]
quicksilver = re.sub(r'^\s*rootNodeElement:.*\n?', '', quicksilver, flags=re.MULTILINE)
quicksilver_dict = json5.loads(quicksilver)
apolloState = quicksilver_dict.get('apolloState')
ROOT_QUERY = quicksilver_dict.get('apolloState').get('ROOT_QUERY')
refs = ROOT_QUERY.get("broadcasts({\"filtersInput\":{\"affiliateCode\":null}})")
Broadcasts = []
for ref in refs:
    Broadcasts.append(ref.get('__ref'))
detail_tv_ids = []
for Broadcast in Broadcasts:
    data = apolloState.get(Broadcast)
    mediaId = data.get('mediaId')
    name = data.get('name')
    description = data.get('customSEOMetadata').get('description') if data.get('customSEOMetadata') else ''
    img_cover = data.get('imageOnAir({\"scale\":\"X1080\"})')
    withoutDVRMediaId = data.get('withoutDVRMediaId')
    slug = data.get('slug')
    channel_ref = data.get('channel').get('__ref')
    categories = data.get('categories')[0].get('slug')

    detail_tv_ids.append({
        'mediaId':mediaId,
        'name' : name,
        'description':description,
        'img_cover':img_cover,
        'withoutDVRMediaId':withoutDVRMediaId,
        'slug':slug,
        'channel_ref':channel_ref,
        'categories': categories
    })
with open(path/'detail_tv_ids.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(detail_tv_ids))
