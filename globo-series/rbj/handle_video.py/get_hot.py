import requests
from save_json import save_json
import json
import uuid 

random_uuid = str(uuid.uuid4())


@save_json(name='hot')
def get_hot():
    headers = {
    'authorization': '1787bc2f58d7000eee93b0d15d2bcb87f6b6e5464396d5f4b2d51444c6d446965593076414f5759474234635843484f6e71397a45413371454a6a342d7568502d45696e7a79766251353233304c6d74424b697868385449557477664d67737233724e4e6552413d3d3a303a75716f7a75346764773369397535317676656664',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-tenant-id': 'globo-play-us',
    }


    params = {
        'operationName': 'getOffer',
        # 'variables': json.dumps({"id":"468df581-e4b1-474d-810b-3b467b02193f","page":1,"perPage":24,"offerContext":None}),

        'variables': '{"id":"24a526f8-e01c-4488-b749-7b619b8546d4","page":1,"perPage":24,"offerContext":null}',
        'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"05885f9cb61e7aa9f5346bb0e83d1767b19d8273ede7cababbc1fd761a91ade7"}}',
    }

    response = requests.get('https://cloud-cdn-jarvis.globo.com/graphql', params=params, headers=headers)
    print(response)
    print(response.json())

    print(len(response.json()['data']['genericOffer']['paginatedItems']['resources']))


    return response.json()


if __name__ == '__main__':
    get_hot()



