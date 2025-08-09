import sys
import requests
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools.save_json import save_json


@save_json(name='episo_id')
def get_episo_id(item: dict):
    title_id = item.get('titleId')
    season = item.get('season')

    headers = {
        'authority': 'cloud-cdn-jarvis.globo.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'sec-ch-ua-platform': '"Windows"',
        'authorization': '139c8bca2815a1c71b11c874f68082c8d51556531524b56614d44416f52455374707246666f793873454e71674d64724c666a4a6f4a7a737375666b49734c706747445a6748473953413634314c636f56584b6559643344505f66794a427761643138504137673d3d3a303a75716f7a75346764773369397535317676656664',
        'x-platform-id': 'web',
        'x-user-id': '93cc4ec3-958b-41e7-8531-c1c1c320bf39',
        'x-device-id': 'desktop',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'Referer': 'https://globoplay.globo.com/',
        'sec-ch-ua-mobile': '?0',
        'x-hsid': 'f1b430d9-ae1f-4e3d-bd3d-414cad8b6129',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'accept': '*/*',
        'x-client-version': '2025.07-16',
        'content-type': 'application/json',
        'x-tenant-id': 'globo-play-us',
    }


    episo_id_list = []
    page = 1
    while True:
        response = requests.get('https://cloud-cdn-jarvis.globo.com/graphql', params=get_params(page=page, title_id=title_id), headers=headers)
        data = response.json()
        # print(data['data']['title']['structure']['episodes']['resources'])
        if data['data']['title']['structure']['episodes']['resources']:
            for item in data['data']['title']['structure']['episodes']['resources']:
                episo_id_list.append({
                    "episode_id": item.get('video').get('id'),
                    "headline": item.get('video').get('headline'),
                })
            page += 1
        else:
            break

    episo_id_list = handle_episo_id_list(episo_id_list, season)
    return episo_id_list 

def get_params(page: int, title_id: str):
    params = {
        'operationName': 'getEpisodes',
        'variables': f'{{"titleId":"{title_id}","page":{page},"perPage":40}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"88a40da093acd13f3be038cb4d666328e1a3bac142f9829ab5d40e60fb61702b"}}',
    }
    return params 

def handle_episo_id_list(episo_id_list: list, season: int):
    reverse_episo_id_list = episo_id_list[::-1]
    for index, item in enumerate(reverse_episo_id_list, start=1):
        item['season'] = season
        item['episode_number'] = index 
    return reverse_episo_id_list


if __name__ == "__main__":
    item = {
        "titleId": "'NGvxTCrNkQ'",
        "originProgramId": "27202",
        "season": 1
    }
    
    data = get_episo_id(item)


