import sys
import requests
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools.save_json import save_json
 

@save_json(name='offer')
def get_offer():
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

    params = {
        'operationName': 'getOffer',
        'variables': '{"id":"a00cf176-66e2-498e-aa28-6bae0c812ebe","page":1,"perPage":40,"offerContext":null}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"05885f9cb61e7aa9f5346bb0e83d1767b19d8273ede7cababbc1fd761a91ade7"}}',
    }

    response = requests.get('https://cloud-cdn-jarvis.globo.com/graphql', params=params, headers=headers)
    data = response.json()
    offer_list = []
    try:
        for item in data['data']['genericOffer']['paginatedItems']['resources']:
            offer_list.append({
                "titleId": item.get('titleId'),
                "slug": item.get('slug'),
                "headline": item.get('headline'),
                "originProgramId": item.get('originProgramId'),
                "season":1
            })
    except Exception as e:
        pass
    print(len(offer_list))

    return offer_list





if __name__ == "__main__":
    get_offer()
