import requests

cookies = {
    'af_id': 'abbb993f-00a9-4dac-87bb-9740ff622689-p',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'cache-control': 'no-cache',
    'content-type': 'text/plain',
    'origin': 'https://www.playplus.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.playplus.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'af_id=abbb993f-00a9-4dac-87bb-9740ff622689-p',
}

params = {
    'site-id': '9153e79f-b987-4d9c-9027-189af3551d4c',
}

data = '{"data":{"eventType":"LOAD","afWebUserId":"abbb993f-00a9-4dac-87bb-9740ff622689-p","webAppId":"9153e79f-b987-4d9c-9027-189af3551d4c"},"meta":{"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36","webDriver":"NOT_SUPPORTED","languageKey":"zh-CN","colorDepthKey":24,"cookieEnabled":true,"deviceMemoryKey":8,"pixelRatioKey":1.5,"screenResolutionWidth":1707,"screenResolutionHeight":960,"locationHref":"https://www.playplus.com/live/liveEvent/180?groupId=7","locationSearch":"?groupId=7","locationOrigin":"https://www.playplus.com","screenOrientation":{"angle":0,"type":"landscape-primary"},"availableScreenResolutionWidth":1707,"availableScreenResolutionHeight":960,"timezoneOffset":-480,"timeZone":"Asia/Shanghai","sessionStorageKey":"ENABLED","localStorageKey":"ENABLED","indexedDbKey":"ENABLED","addBehaviorKey":"NOT_SUPPORTED","openDatabaseKey":"NOT_SUPPORTED","cpuClassKey":"NOT_SUPPORTED","platformKey":"ENABLED","doNotTrackKey":"NOT_SUPPORTED","isCanvasSupported":"ENABLED","adBlockKey":"DISABLED","hasLiedLanguagesKey":"DISABLED","javaEnabled":"DISABLED","deviceClockSpeed":18962.600000023842,"loadEventStart":0,"loadEventEnd":0,"loadTime":0,"documentLoad":16029,"version":{"BASE":"0.0.54","PBA":"0.0.54","BANNERS":"0.0.54"},"query":{"groupId":"7"},"referrer":"https://www.playplus.com/live/liveEvent/187?groupId=7","timestamp":1753177188780,"lastInteractionTimestamp":1753177116475,"isDevMode":false,"clientHints":{"architecture":"x86","bitness":"64","brands":{"brands":[{"brand":"Not)A;Brand","version":"8"},{"brand":"Chromium","version":"138"},{"brand":"Google Chrome","version":"138"}]},"mobile":false,"model":"","platform":"Windows","platformVersion":"10.0.0","uaFullVersion":"138.0.7204.158"}}}'

import json
from pathlib import Path

response = requests.post('https://wa.appsflyer.com/events', params=params, cookies=cookies, headers=headers, data=data)

path = Path(__file__).parent

if response.status_code == 200:
    try:
        # 尝试解析JSON响应
        response_data = response.json()
        file_name = path / 'cookies.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
        print(f'成功将响应保存到 {file_name}')
    except json.JSONDecodeError:
        # 如果响应不是有效的JSON，则将其作为文本保存
        file_name = path / 'cookies.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f'响应不是有效的JSON，已将文本内容保存到 {file_name}')
else:
    print(f'请求失败，状态码: {response.status_code}')
    print(f'响应内容: {response.text}')