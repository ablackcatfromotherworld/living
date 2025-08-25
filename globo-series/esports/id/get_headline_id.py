

import requests
from save_json import save_json

@save_json(name='episo_id')
def get_episo_id(item: dict):
    title_id = item.get('titleId')
    season = item.get('season')

    headers = {
        'x-glb-exp-id': 'jra0VrIvHRqinAH_pXpN1yz0GMQpgp9DMK_FgRfdmNw=',
        'authorization': '139c8bca2815a1c71b11c874f68082c8d51556531524b56614d44416f52455374707246666f793873454e71674d64724c666a4a6f4a7a737375666b49734c706747445a6748473953413634314c636f56584b6559643344505f66794a427761643138504137673d3d3a303a75716f7a75346764773369397535317676656664',
        'x-platform-id': 'web',
        'x-user-id': '93cc4ec3-958b-41e7-8531-c1c1c320bf39',
        'x-device-id': 'desktop',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'Referer': 'https://globoplay.globo.com/',
        'sec-ch-ua-mobile': '?0',
        'x-hsid': '08fb7c2a-ccc7-4219-a2d8-9667fb3fb075',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'accept': '*/*',
        'x-client-version': '2025.08-7',
        'content-type': 'application/json',
        'x-tenant-id': 'globo-play',
        }


    episo_id_list = []
    page = 1
    while True:
        response = requests.get('https://cloud-jarvis.globo.com/graphql', params=get_params(page=page, title_id=title_id), headers=headers)
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
    return episo_id_list 

def get_params(page: int, title_id: str):
    params = {
        'operationName': 'getEpisodesPlaylist',
        'variables': f'{{"titleId":"{title_id}","page":{page},"perPage":40}}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"77fbf2cae4a7a8f5a39e33c4d8b37a40b566d7dc3506d3ea876dd7a1dc1d74a4"}}',
    }
    return params 



if __name__ == "__main__":
    item = {
        "titleId": "XY6jnccMv9",
    }
    
    data = get_episo_id(item)


