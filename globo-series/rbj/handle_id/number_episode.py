import sys
import requests
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools.save_json import save_json

def get_number_episode(id):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'origin': 'https://flixbaba.tv',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://flixbaba.tv/tv/233519/vale-tudo',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://api.themoviedb.org/3/tv/233519?api_key=7045bc4055c6293e84534dd8f6dbb024&append_to_response=images,videos,credits,recommendations,similar',
        headers=headers,
    )
    data = response.json()
    return data
