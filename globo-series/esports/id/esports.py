from csv import QUOTE_ALL
import requests
import parsel 
from pathlib import Path 
import re 
import execjs
import json
from save_json import save_json

path = Path(__file__).parent

@save_json('esports')
def get_esports():  

    cookies = {
        '_fbp': 'fb.1.1754451185088.498990760755977959',
        'glb_uid_jwt': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnbGJfdWlkIjoiMTM2OTExODYxNzgxMzc2MDEzMDE2NiJ9.6qUtA6c3fOXuueloSHMM4ghNKmFlF6BeiGVdrfmvQF4',
        'gpixel_uid': 'jra0VrIvHRqinAH_pXpN19VeEVSNBRWzfPZww4h_tgY=',
        'GLBID': '1787bc2f58d7000eee93b0d15d2bcb87f6b6e5464396d5f4b2d51444c6d446965593076414f5759474234635843484f6e71397a45413371454a6a342d7568502d45696e7a79766251353233304c6d74424b697868385449557477664d67737233724e4e6552413d3d3a303a75716f7a75346764773369397535317676656664',
        'GLOBO_ID': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJnbG9ib0lkIjoiOTNjYzRlYzMtOTU4Yi00MWU3LTg1MzEtYzFjMWMzMjBiZjM5IiwgInVzZXJOYW1lIjoiRGVuZyBTaGVuZ2JvIiwgInBob3RvVXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTEN2eXM2MWhPZ1J6WXE3NU50cEFqNDE2ZzBXb0FTSkd0bDJxQTgxSmZiT1YxQUJBPXM5Ni1jIn0.bp8GXdTHAcpShSwh_GgF7rRMaY7KxhWnGTXbi0aD6thTJjXC3V4C0UKNggfwye0c-m7rwIq58asuCmFWivpxdJwLT1ttsJy19PedSXGTxP7KLTHnL9q6ZZJWzilOuL7aLc07jjMEG1C7lUzQm9IW8EtgT6IUE7uN7bEpZzIrDs9_2YVc2YhD1mMUmzX93tzeVNwpiFDZAAyozuMRnMRKhjCP9qKPLGiYL3iaR02JHfzoLxXGZK6HrflCufjjpqiOcLtOdcVVKCPnbR6YSWAxOZ9yyO2HQPdEsw1iqT33sHLQ1Ryg8OoJ7bx0er7w4vAFuXgE0KVRPscDyOWfZ7BbUg',
        'GBID': 'GBID.1754451357333.4e4bf68b-42e7-4d0b-bbd0-69ecb626cc71',
        '__spdt': '23cba56d0ce64133a51bc3b46473563b',
        '_sfid_fd4e': '{%22anonymousId%22:%225a976894ed508914%22%2C%22consents%22:[]}',
        '_tt_enable_cookie': '1',
        '_ttp': '01K1YQ6MXX1MEGDXV6980E6S0C_.tt.1',
        '_cc_id': '6e4cf98cbd54a186d5c972073da5702a',
        '_evga_8981': '{%22uuid%22:%225a976894ed508914%22%2C%22puid%22:%22NZqvyTi00NM7AMfrrWqQ9UQ7tKYP2SsvJ6fthtHY5xyHHFdSTmn3NWVg2Mbthb-y5sS_3_fIQmqWisjru356aI22dUeAiq5Vfj2dfWkdDXLlEvRiN-NvKUsi8UjzD21I%22%2C%22affinityId%22:%2208x%22}',
        '_scor_uid': '5e3f50adad7744849fd45ef38832a929',
        'CB_Subject': 'eyJpZCI6IjkzY2M0ZWMzLTk1OGItNDFlNy04NTMxLWMxYzFjMzIwYmYzOSIsInRva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBZWFFpT2pFM05UUTBOek0zTXpBc0luTjFZaUk2SWprelkyTTBaV016TFRrMU9HSXROREZsTnkwNE5UTXhMV014WXpGak16SXdZbVl6T1NKOS5jVWtma0dxVXoxUWtyRFUzT3YyNEtNUndQWkdDR2RGX0RaaGRvQUF1andJIiwiaXNBbm9ueW1vdXMiOmZhbHNlfQ==',
        '_ym_uid': '1754473768809257324',
        '_ym_d': '1754473768',
        '__utmz': 'other',
        'OptanonAlertBoxClosed': '2025-08-06T03:36:44.121553797Z',
        'OptanonConsent': 'groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&datestamp=Sat+Aug+09+2025+13%3A29%3A50+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.38.0&isGpcEnabled=0&geolocation=CN%3BSC&isIABGlobal=false&consentId=93cc4ec3-958b-41e7-8531-c1c1c320bf39&hosts=&interactionCount=0&landingPath=https%3A%2F%2Fgloboplay.globo.com%2Fv%2F13814808%2F%3Fs%3D0s',
        'permutive-id': '89ae82d3-f962-4a37-b95c-ac12ef6554d0',
        'cookie-banner-consent-accepted': 'true',
        'cookie-banner-accepted-version': '1.4.2.4',
        '__gads': 'ID=9734edf1182b77c4:T=1754727485:RT=1754727485:S=ALNI_MZL4jO_SJGQIheLAWhkouSZ3bJfNw',
        '_pin_unauth': 'dWlkPU4yRXlNbVE1WkdVdFpEWTBOQzAwTlRkaExXSTVZekl0WVRaalpXUTJNMlV5TlRJeQ',
        '_clck': '1wbhiti%7C2%7Cfyb%7C0%7C2047',
        '_did': 'web_245016914461DE6B',
        'kwai_uuid': 'd91b81d4a3c88891ef9883ae39c8d095',
        '_gcl_au': '1.1.584162474.1754451357',
        '_uetvid': 'a418c71074f911f09dc1bd6967a50519',
        'bv_page': '{"beeviral.produtosCarrinho":"GG-GP-MC-4D-A-WB","beeviral.origemId":"92979","beeviral.glbproduct":"UA-296593-56","beeviral.conversion":"vitrine","beeviral.assinaturaHIT":"assinante","beeviral._gl":"1*sqxlch*_gcl_au*NTg0MTYyNDc0LjE3NTQ0NTEzNTc.*_ga*MTUwNjI3MDgwMS4xNzUyODA2MDYw*_ga_G5YX0X0P68*czE3NTQ3Mjc1OTQkbzIkZzEkdDE3NTQ3Mjc2MjQkajMwJGwwJGgw"}',
        'bv_token': 'Q1BucnBSKnR3UUVvQjVvdHVKSTNJNXlhS1J6RGFKMEtOVmw1SDlRdGpOMTdob0ZpY2Y3NGxRQnRkcGRFRnNmdw==',
        'bvfield_cap': '%7B%7D',
        'bvfieldadd_cap': '%7B%7D',
        'IsActiveDebug': 'N',
        'bv_form_data': '%7B%22valorconversao%22%3A%22358.8%22%7D',
        'bv_key_campaign': '',
        '_ga_G5YX0X0P68': 'GS2.1.s1754727594$o2$g1$t1754728232$j60$l0$h0',
        'panoramaId_expiry': '1756195545237',
        'panoramaId': '16d378c877c95967bd4f8921e60216d53938ca0406fd1c3ad7627af897acb18a',
        'panoramaIdType': 'panoIndiv',
        'glb_uid': '"jra0VrIvHRqinAH_pXpN19VeEVSNBRWzfPZww4h_tgY="',
        '_ga_NWTRTWY1TF': 'GS2.1.s1755597433$o1$g0$t1755597434$j59$l0$h0',
        '_ga': 'GA1.1.1506270801.1752806060',
        '_ym_isad': '2',
        '_ga_WLHSK1RZ32': 'GS2.1.s1756095392$o32$g0$t1756095392$j60$l0$h1870378789',
        'hsid': '66568dce-08cf-4df4-85e2-b6dea0f7336e',
        'ttcsid': '1756100670778::WQvjYKwnC8k0Gn_DSTVo.23.1756100670778',
        'ttcsid_CS2543JC77U61CV1R35G': '1756100670777::qAllxQcCrJPUWpy0ycHI.23.1756100671005',
        'ttcsid_D0AH3JRC77UD5RFHJE10': '1756100670778::j5AKdAbQEUxn85KItd7g.24.1756100671005',
        'FCNEC': '%5B%5B%22AKsRol9107GzLRFc7hatLJUkCVqwwN9ExhLEAAxKYvzW1DE3z0hDIGsHdGkZYj6wnB8APzlKx_KPP2OnmvbhUXiy8r26_K3LbgKEDJCfSpRBqXcLWT0NlxwenaaTHArU3CC9clglThJu75hCEq02cDAvFyjxmUFSHw%3D%3D%22%5D%5D',
        'ttcsid_C5NM1IDO3VNUQLVLF980': '1756100705295::hV8jegaV_iSEuEutxKPW.21.1756100705295',
        '_ga_5401XJ0K8J': 'GS2.1.s1756100648$o17$g0$t1756100711$j60$l0$h0',
        '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-08-25T05%3A45%3A24.469Z%22%7D',
        '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22sD4Yc3G7NiXkLypHHh1U%22%2C%22expiryDate%22%3A%222026-08-25T05%3A45%3A24.469Z%22%7D',
        'cto_bundle': 'd33StV9ydWkyWXE5ZjNyU25iZ1lFS2RyR2pSSTRkVHRtJTJCc09VbFBqJTJGdzJHTDYzb1lrZ2RkbjElMkZqVEJtSGdGakRuOHdpNm1WYkRyTyUyRkpJMHl0YkhjWXB0cUFxYXZEdnBzNHFtNVlucFNOZGZ3U0xNNnVsQmQlMkJDZ1dvNEliRlNqZHAlMkZNcmdxYzAwZkViZFhCTksxeCUyRkhtNTlEbVZHU3Z0THZTRGM3YVRodiUyRmhySUVlNE44QXkzQVlCUHltUGRsNWQwJTJCZG93aW5raFZ5azVhakY0bzZiRnlMR1d3JTNEJTNE',
        '_hzt.interval': '20000',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://globoplay.globo.com/callback.html',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        # 'cookie': '_fbp=fb.1.1754451185088.498990760755977959; glb_uid_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJnbGJfdWlkIjoiMTM2OTExODYxNzgxMzc2MDEzMDE2NiJ9.6qUtA6c3fOXuueloSHMM4ghNKmFlF6BeiGVdrfmvQF4; gpixel_uid=jra0VrIvHRqinAH_pXpN19VeEVSNBRWzfPZww4h_tgY=; GLBID=1787bc2f58d7000eee93b0d15d2bcb87f6b6e5464396d5f4b2d51444c6d446965593076414f5759474234635843484f6e71397a45413371454a6a342d7568502d45696e7a79766251353233304c6d74424b697868385449557477664d67737233724e4e6552413d3d3a303a75716f7a75346764773369397535317676656664; GLOBO_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJnbG9ib0lkIjoiOTNjYzRlYzMtOTU4Yi00MWU3LTg1MzEtYzFjMWMzMjBiZjM5IiwgInVzZXJOYW1lIjoiRGVuZyBTaGVuZ2JvIiwgInBob3RvVXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTEN2eXM2MWhPZ1J6WXE3NU50cEFqNDE2ZzBXb0FTSkd0bDJxQTgxSmZiT1YxQUJBPXM5Ni1jIn0.bp8GXdTHAcpShSwh_GgF7rRMaY7KxhWnGTXbi0aD6thTJjXC3V4C0UKNggfwye0c-m7rwIq58asuCmFWivpxdJwLT1ttsJy19PedSXGTxP7KLTHnL9q6ZZJWzilOuL7aLc07jjMEG1C7lUzQm9IW8EtgT6IUE7uN7bEpZzIrDs9_2YVc2YhD1mMUmzX93tzeVNwpiFDZAAyozuMRnMRKhjCP9qKPLGiYL3iaR02JHfzoLxXGZK6HrflCufjjpqiOcLtOdcVVKCPnbR6YSWAxOZ9yyO2HQPdEsw1iqT33sHLQ1Ryg8OoJ7bx0er7w4vAFuXgE0KVRPscDyOWfZ7BbUg; GBID=GBID.1754451357333.4e4bf68b-42e7-4d0b-bbd0-69ecb626cc71; __spdt=23cba56d0ce64133a51bc3b46473563b; _sfid_fd4e={%22anonymousId%22:%225a976894ed508914%22%2C%22consents%22:[]}; _tt_enable_cookie=1; _ttp=01K1YQ6MXX1MEGDXV6980E6S0C_.tt.1; _cc_id=6e4cf98cbd54a186d5c972073da5702a; _evga_8981={%22uuid%22:%225a976894ed508914%22%2C%22puid%22:%22NZqvyTi00NM7AMfrrWqQ9UQ7tKYP2SsvJ6fthtHY5xyHHFdSTmn3NWVg2Mbthb-y5sS_3_fIQmqWisjru356aI22dUeAiq5Vfj2dfWkdDXLlEvRiN-NvKUsi8UjzD21I%22%2C%22affinityId%22:%2208x%22}; _scor_uid=5e3f50adad7744849fd45ef38832a929; CB_Subject=eyJpZCI6IjkzY2M0ZWMzLTk1OGItNDFlNy04NTMxLWMxYzFjMzIwYmYzOSIsInRva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnBZWFFpT2pFM05UUTBOek0zTXpBc0luTjFZaUk2SWprelkyTTBaV016TFRrMU9HSXROREZsTnkwNE5UTXhMV014WXpGak16SXdZbVl6T1NKOS5jVWtma0dxVXoxUWtyRFUzT3YyNEtNUndQWkdDR2RGX0RaaGRvQUF1andJIiwiaXNBbm9ueW1vdXMiOmZhbHNlfQ==; _ym_uid=1754473768809257324; _ym_d=1754473768; __utmz=other; OptanonAlertBoxClosed=2025-08-06T03:36:44.121553797Z; OptanonConsent=groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&datestamp=Sat+Aug+09+2025+13%3A29%3A50+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.38.0&isGpcEnabled=0&geolocation=CN%3BSC&isIABGlobal=false&consentId=93cc4ec3-958b-41e7-8531-c1c1c320bf39&hosts=&interactionCount=0&landingPath=https%3A%2F%2Fgloboplay.globo.com%2Fv%2F13814808%2F%3Fs%3D0s; permutive-id=89ae82d3-f962-4a37-b95c-ac12ef6554d0; cookie-banner-consent-accepted=true; cookie-banner-accepted-version=1.4.2.4; __gads=ID=9734edf1182b77c4:T=1754727485:RT=1754727485:S=ALNI_MZL4jO_SJGQIheLAWhkouSZ3bJfNw; _pin_unauth=dWlkPU4yRXlNbVE1WkdVdFpEWTBOQzAwTlRkaExXSTVZekl0WVRaalpXUTJNMlV5TlRJeQ; _clck=1wbhiti%7C2%7Cfyb%7C0%7C2047; _did=web_245016914461DE6B; kwai_uuid=d91b81d4a3c88891ef9883ae39c8d095; _gcl_au=1.1.584162474.1754451357; _uetvid=a418c71074f911f09dc1bd6967a50519; bv_page={"beeviral.produtosCarrinho":"GG-GP-MC-4D-A-WB","beeviral.origemId":"92979","beeviral.glbproduct":"UA-296593-56","beeviral.conversion":"vitrine","beeviral.assinaturaHIT":"assinante","beeviral._gl":"1*sqxlch*_gcl_au*NTg0MTYyNDc0LjE3NTQ0NTEzNTc.*_ga*MTUwNjI3MDgwMS4xNzUyODA2MDYw*_ga_G5YX0X0P68*czE3NTQ3Mjc1OTQkbzIkZzEkdDE3NTQ3Mjc2MjQkajMwJGwwJGgw"}; bv_token=Q1BucnBSKnR3UUVvQjVvdHVKSTNJNXlhS1J6RGFKMEtOVmw1SDlRdGpOMTdob0ZpY2Y3NGxRQnRkcGRFRnNmdw==; bvfield_cap=%7B%7D; bvfieldadd_cap=%7B%7D; IsActiveDebug=N; bv_form_data=%7B%22valorconversao%22%3A%22358.8%22%7D; bv_key_campaign=; _ga_G5YX0X0P68=GS2.1.s1754727594$o2$g1$t1754728232$j60$l0$h0; panoramaId_expiry=1756195545237; panoramaId=16d378c877c95967bd4f8921e60216d53938ca0406fd1c3ad7627af897acb18a; panoramaIdType=panoIndiv; glb_uid="jra0VrIvHRqinAH_pXpN19VeEVSNBRWzfPZww4h_tgY="; _ga_NWTRTWY1TF=GS2.1.s1755597433$o1$g0$t1755597434$j59$l0$h0; _ga=GA1.1.1506270801.1752806060; _ym_isad=2; _ga_WLHSK1RZ32=GS2.1.s1756095392$o32$g0$t1756095392$j60$l0$h1870378789; hsid=66568dce-08cf-4df4-85e2-b6dea0f7336e; ttcsid=1756100670778::WQvjYKwnC8k0Gn_DSTVo.23.1756100670778; ttcsid_CS2543JC77U61CV1R35G=1756100670777::qAllxQcCrJPUWpy0ycHI.23.1756100671005; ttcsid_D0AH3JRC77UD5RFHJE10=1756100670778::j5AKdAbQEUxn85KItd7g.24.1756100671005; FCNEC=%5B%5B%22AKsRol9107GzLRFc7hatLJUkCVqwwN9ExhLEAAxKYvzW1DE3z0hDIGsHdGkZYj6wnB8APzlKx_KPP2OnmvbhUXiy8r26_K3LbgKEDJCfSpRBqXcLWT0NlxwenaaTHArU3CC9clglThJu75hCEq02cDAvFyjxmUFSHw%3D%3D%22%5D%5D; ttcsid_C5NM1IDO3VNUQLVLF980=1756100705295::hV8jegaV_iSEuEutxKPW.21.1756100705295; _ga_5401XJ0K8J=GS2.1.s1756100648$o17$g0$t1756100711$j60$l0$h0; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%2C%22expiryDate%22%3A%222026-08-25T05%3A45%3A24.469Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22sD4Yc3G7NiXkLypHHh1U%22%2C%22expiryDate%22%3A%222026-08-25T05%3A45%3A24.469Z%22%7D; cto_bundle=d33StV9ydWkyWXE5ZjNyU25iZ1lFS2RyR2pSSTRkVHRtJTJCc09VbFBqJTJGdzJHTDYzb1lrZ2RkbjElMkZqVEJtSGdGakRuOHdpNm1WYkRyTyUyRkpJMHl0YkhjWXB0cUFxYXZEdnBzNHFtNVlucFNOZGZ3U0xNNnVsQmQlMkJDZ1dvNEliRlNqZHAlMkZNcmdxYzAwZkViZFhCTksxeCUyRkhtNTlEbVZHU3Z0THZTRGM3YVRodiUyRmhySUVlNE44QXkzQVlCUHltUGRsNWQwJTJCZG93aW5raFZ5azVhakY0bzZiRnlMR1d3JTNEJTNE; _hzt.interval=20000',
    }

    response = requests.get('https://globoplay.globo.com/categorias/esportes/', cookies=cookies, headers=headers)
    selector = parsel.Selector(response.text)
    Quicksilver = selector.xpath('//script[@type="application/javascript"]/text()').get()
    # Quicksilver = re.findall(r'var Quicksilver\s*=\s*({.*?});', Quicksilver, re.DOTALL)[0]
    # Quicksilver = re.sub('document.getElementById("app")', '', Quicksilver)

    
    with open(path / 'a.js', 'w', encoding='utf-8') as f:
        f.write(Quicksilver)


    # Quicksilver = json.loads(Quicksilver)
    print(type(Quicksilver))
    return Quicksilver


if __name__ == "__main__":
    get_esports()
    ctx = execjs.compile('a.js')
    print(ctx.call('Quicksilver'))



