import requests

cookies = {
    'deviceId': '29548.102479178386-1751443049349',
    'sessionId': '17514430493491358552931',
    'cookieIsAgree': 'true',
    '_ym_uid': '175144306966333850',
    '_ym_d': '1751443069',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'lastChannel': 'tv5monde',
    'appGuid': '44e7d0f9-3570-4731-8a73-baf0e2afb65b',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.brasilaovivo.tv/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-device-id': '29548.102479178386-1751443049349',
    'x-lhd-agent': '{"platform":"web","app":"afriqueendirect.tv"}',
    # 'cookie': 'deviceId=29548.102479178386-1751443049349; sessionId=17514430493491358552931; cookieIsAgree=true; _ym_uid=175144306966333850; _ym_d=1751443069; _ym_isad=1; _ym_visorc=w; lastChannel=tv5monde; appGuid=44e7d0f9-3570-4731-8a73-baf0e2afb65b',
}

params = {
    'grouping': '0',
    'epg_from': '0',
    'epg_limit': '1',
}

response = requests.get('https://www.brasilaovivo.tv/api/v4/epg/france24-fr', params=params, cookies=cookies, headers=headers)
print(response.json())
with open('./brasilaovivo.json', 'w', encoding='utf-8') as f:
    f.write(response.text)
