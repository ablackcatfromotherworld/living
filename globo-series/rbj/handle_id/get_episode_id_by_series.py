import sys
from turtle import title
import requests
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools.save_json import save_json

@save_json(name='episode_id_by_series')
def get_episode_id_by_series(item: dict):
    title_id = item.get('titleId')
    season = item.get('season')


    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'authorization': '139c8bca2815a1c71b11c874f68082c8d51556531524b56614d44416f52455374707246666f793873454e71674d64724c666a4a6f4a7a737375666b49734c706747445a6748473953413634314c636f56584b6559643344505f66794a427761643138504137673d3d3a303a75716f7a75346764773369397535317676656664',
        'x-platform-id': 'web',
        'x-user-id': '93cc4ec3-958b-41e7-8531-c1c1c320bf39',
        'x-device-id': 'desktop',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'Referer': 'https://globoplay.globo.com/',
        'sec-ch-ua-mobile': '?0',
        'x-hsid': 'a17c4118-4cd9-4156-8cc0-2233cd749b9f',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'accept': '*/*',
        'x-client-version': '2025.08-1',
        'content-type': 'application/json',
        'x-tenant-id': 'globo-play-us',
    }

    params = {
        'operationName': 'getEpisodesByPage',
        'variables': f'{{"titleId":"{title_id}","page":1,"perPage":40}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"3fc060d3872ada1413782ae2ab6c1511b0b0df7fafdc549028e3f3b35c13d247"}}',
    }

    response = requests.get('https://cloud-cdn-jarvis.globo.com/graphql', params=params, headers=headers)
    data = response.json()
    print(len(data.get('data').get('title').get('structure').get('episodes').get('resources')))

    return data 

if __name__ == "__main__":
    item = {
        "titleId": "Sg7Y2Z1CsJ",
        "originProgramId": "28297",
        "season": 1
    }
    data = get_episode_id_by_series(item)

