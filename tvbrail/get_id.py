import requests

cookies = {
    '_ga': 'GA1.1.880391425.1750043858',
    '_ga_E0BYEPL16T': 'GS2.1.s1750043987$o1$g1$t1750044065$j43$l0$h0',
    '__gads': 'ID=cebc2d3e337d21ef:T=1750043865:RT=1751425048:S=ALNI_MYK9JiY7_4N8a1FJ8rBIL4J8eC-nw',
    '__gpi': 'UID=000011052525fdf0:T=1750043865:RT=1751425048:S=ALNI_MYm1pkjjZKgxfGFp5Mz_Oou4-ggxg',
    '__eoi': 'ID=075108d65a1ce47a:T=1750043865:RT=1751425048:S=AA-AfjaRhnqUx5b5aYeIzpHAVoTc',
    '_ga_0SNLMPXB24': 'GS2.1.s1751425044$o5$g1$t1751425126$j41$l0$h0',
    '_ga_TGW7R30M20': 'GS2.1.s1751425046$o5$g1$t1751425126$j41$l0$h1644060216',
    '_ga_E7XFVGNNPX': 'GS2.1.s1751451490$o3$g1$t1751452183$j51$l0$h0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://play.ebc.com.br/tabs/home',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '_ga=GA1.1.880391425.1750043858; _ga_E0BYEPL16T=GS2.1.s1750043987$o1$g1$t1750044065$j43$l0$h0; __gads=ID=cebc2d3e337d21ef:T=1750043865:RT=1751425048:S=ALNI_MYK9JiY7_4N8a1FJ8rBIL4J8eC-nw; __gpi=UID=000011052525fdf0:T=1750043865:RT=1751425048:S=ALNI_MYm1pkjjZKgxfGFp5Mz_Oou4-ggxg; __eoi=ID=075108d65a1ce47a:T=1750043865:RT=1751425048:S=AA-AfjaRhnqUx5b5aYeIzpHAVoTc; _ga_0SNLMPXB24=GS2.1.s1751425044$o5$g1$t1751425126$j41$l0$h0; _ga_TGW7R30M20=GS2.1.s1751425046$o5$g1$t1751425126$j41$l0$h1644060216; _ga_E7XFVGNNPX=GS2.1.s1751451490$o3$g1$t1751452183$j51$l0$h0',
}

params = {
    'geo': 'true',
    'limit': '10000',
    'sort': 'populares',
    'order': 'desc',
    'idade': '18',
}

response = requests.get('https://play.ebc.com.br/v2/conteudos/populares', params=params, cookies=cookies, headers=headers)
print(len(response.json()))
a = set()
for item in response.json():
    a.add(item.get('id_conteudo'))

print(len(set(a)))