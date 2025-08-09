import requests
from save_json import save_json

@save_json(name='video')
def parse_video(video_id):


    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'authorization': 'Bearer 1787bc2f58d7000eee93b0d15d2bcb87f6b6e5464396d5f4b2d51444c6d446965593076414f5759474234635843484f6e71397a45413371454a6a342d7568502d45696e7a79766251353233304c6d74424b697868385449557477664d67737233724e4e6552413d3d3a303a75716f7a75346764773369397535317676656664',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://globoplay.globo.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://globoplay.globo.com/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-session-id': 'eyJhbGciOiJSUzUxMiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJhcHBsaWNhdGlvbiI6IjE1MSIsImNvdW50cnlfY29kZSI6IiIsImV4cCI6MTc1NTA1Nzk1NiwiaWF0IjoxNzU0NDUzMTU2LCJpc3MiOiJwbGF5YmFjay1hcGktcHJvZC1nY3AiLCJtYXhfc2xvdHMiOjMsIm9wZW5fc3RhdHVzIjoiRiIsIm93bmVyIjoiOTNjYzRlYzMtOTU4Yi00MWU3LTg1MzEtYzFjMWMzMjBiZjM5Iiwic2xvdHNfZ3JvdXAiOiJnbG9ib3BsYXlfdGllcl8xIiwidXNlclNlc3Npb25LZXkiOiJmYTZkZWU2MC1mNmFkLTRjODQtOTg3MS0yY2RlMWJhNGYyNTQiLCJ2aWRlb19zZXNzaW9uX2lkIjoiMTcwODI1NDYtMzdhYS1mYjE3LWY3NTQtMmM3MjgyM2M5NDZiIn0.hBknE1dRSTyEXh_yO_KdX527nJLX49g-5zvq0w79eU3qARcjorONbBUhRWPEFIMSHbcnFk-o83m3cyS8YrSc5rupayhL-YElxBWTNGoF0IbO6GoluuUqvmP09WDjg-u9w7lg_ICGEHxxBexbAGmFga-Aosa7T7-mFBMnqZC48WhNXIrT26oMd_-wd8kc2t61QNVqYXVlbGMEE7W5PjpKQ1-fh8DBIXWoDDNk419CCZpMhKhLRVZmiVZ1vN4GU310N6KQ2Xjhw9N55SXXs2VZX0nHwS1ecar1M1omtcW62sB9tFhtFL9-T7JcQ94k4vxHljjEKVhJ2t3k2-A2drjE7A',
         }

    json_data = {
        'player_type': 'desktop',
        'video_id': str(video_id),
        'quality': 'max',
        'content_protection': 'widevine',
        'vsid': '56148345-2a6b-c217-5d0b-6250ba4389e9',
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

    response = requests.post('https://playback.video.globo.com/v4/video-session', headers=headers, json=json_data)
    return response.json()

    # return response.json().get('sources')[0].get('url')

if __name__ == '__main__':
    parse_video(13820527)


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"player_type":"desktop","video_id":"13814808","quality":"max","content_protection":"widevine","vsid":"56148345-2a6b-c217-5d0b-6250ba4389e9","tz":"+08:00","capabilities":{"low_latency":true,"smart_mosaic":true,"dvr":true},"consumption":"streaming","metadata":{"name":"web","device":{"type":"desktop","os":{}}},"version":2}'
#response = requests.post('https://playback.video.globo.com/v4/video-session', cookies=cookies, headers=headers, data=data)