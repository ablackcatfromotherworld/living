import json 
import parsel 
from curl_cffi import requests 
from save_file import save_file



@save_file('popular.json')
def get_popular():

    cookies = {
        'akamai_generated_location': '{"zip":"""","city":"CHENGDU","state":"SC","county":"""","areacode":"""","lat":"30.67","long":"104.07","countrycode":"CN"}',
        'akacd_RTReplatform': '2147483647~rv=28~id=d780e472bada1ae6d786dc85fefe6d07',
        'ak_bmsc': 'AD9E8ED0A5FC57021734683BDF41050B~000000000000000000000000000000~YAAQh7gpFxvL+2CYAQAA0g1sjRwWXS7KKldiMu58+RB3h1loqx++y680/DPEEGch7+NPagTXibccTRK3YYTC/7HFNCxG48bUAwpCzPTNgTvT+3z4i/DBIMMqnlTJV30TV9ZzzgVtj3EvLJBOnEuJ/o0ezqvMC7Vf8zKxRhIajIR1O/FhjOlrKlNekxDSOSNIqd0JmDvsX2lyOMBEhB/8/SLal2WsCF05hyYI1ck+DltStPdS+5qv7tXCf77ijqMk3GQaupb/ktL8OwVhv7G3zQH9Ny4NEYPU9ntF6RPsFPNQphfBCzAmY63cL4h3/PwnZp9ZXmYbApHtANsDj2K+FcjIO8j9Mv0k6F2cYe9JP84Q7NzOYoczPzgkkNoCxp995R094e2y4kQype7U6WHsDfr+',
        'eXr91Jra': 'A8cQbI2YAQAARxi8M4hjLqI6loPTgarBwWaAfU17RQdxPMO7uo7lhRSM6rdTAXZwRLGuchxGwH8AAEB3AAAAAA|1|0|0bd591f6154c08fe4d11f4cc246f29eb52c430de',
        'usprivacy': '1---',
        '__host_color_scheme': 'OroIuZT9-WS6tbS3USMEtCWLmNlxewr5uKG3VFvuM5BdvutG-wto',
        '__host_theme_options': '1754719330201',
        'algoliaUT': '8ecf6b13-3f2e-4a70-b8c5-a1c2270da3db',
        'AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg': '1',
        'AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg': '-408604571%7CMCIDTS%7C20310%7CMCMID%7C07870750718867146303300676330597253150%7CMCAAMLH-1755324135%7C11%7CMCAAMB-1755324135%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1754726535s%7CNONE%7CvVersion%7C4.6.0',
        's_cc': 'true',
        'check': 'true',
        'sailthru_pageviews': '2',
        'mbox': 'session#628b220029014c9d95ed7d8a3f0fddab#1754721199|PC#628b220029014c9d95ed7d8a3f0fddab.32_0#1817964139',
        '_cb': 'CbIpSv6jLysBO2gxb',
        '_chartbeat2': '.1754719339385.1754719339385.1.CutXbdGDMYpBaOnCWCU1CL_C2pHP7.1',
        '_cb_svref': 'external',
        '_ALGOLIA': 'anonymous-9c16693a-6012-41f8-b579-13324a28efd5',
        '_awl': '2.1754719343.5-46e4aa6eb7366c86b4b942aff1232900-6763652d75732d7765737431-0',
        'QSI_HistorySession': 'https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F~1754719344768',
        's_sq': 'wbrosrottentomatoes%3D%2526c.%2526a.%2526activitymap.%2526page%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526link%253DTV%252520SHOWS%2526region%253Dmain-page-content%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526pidt%253D1%2526oid%253DTV%252520SHOWS%252520%2526oidt%253D3%2526ot%253DSUBMIT',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Aug+09+2025+14%3A22%3A15+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5697e666-99f7-4186-b4a7-e520e90d7efd&interactionCount=1&landingPath=https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F&groups=1%3A1%2C4%3A1%2C6%3A1%2C7%3A1%2COOF%3A1%2CUSP%3A1',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        # 'cookie': 'akamai_generated_location={"zip":"""","city":"CHENGDU","state":"SC","county":"""","areacode":"""","lat":"30.67","long":"104.07","countrycode":"CN"}; akacd_RTReplatform=2147483647~rv=28~id=d780e472bada1ae6d786dc85fefe6d07; ak_bmsc=AD9E8ED0A5FC57021734683BDF41050B~000000000000000000000000000000~YAAQh7gpFxvL+2CYAQAA0g1sjRwWXS7KKldiMu58+RB3h1loqx++y680/DPEEGch7+NPagTXibccTRK3YYTC/7HFNCxG48bUAwpCzPTNgTvT+3z4i/DBIMMqnlTJV30TV9ZzzgVtj3EvLJBOnEuJ/o0ezqvMC7Vf8zKxRhIajIR1O/FhjOlrKlNekxDSOSNIqd0JmDvsX2lyOMBEhB/8/SLal2WsCF05hyYI1ck+DltStPdS+5qv7tXCf77ijqMk3GQaupb/ktL8OwVhv7G3zQH9Ny4NEYPU9ntF6RPsFPNQphfBCzAmY63cL4h3/PwnZp9ZXmYbApHtANsDj2K+FcjIO8j9Mv0k6F2cYe9JP84Q7NzOYoczPzgkkNoCxp995R094e2y4kQype7U6WHsDfr+; eXr91Jra=A8cQbI2YAQAARxi8M4hjLqI6loPTgarBwWaAfU17RQdxPMO7uo7lhRSM6rdTAXZwRLGuchxGwH8AAEB3AAAAAA|1|0|0bd591f6154c08fe4d11f4cc246f29eb52c430de; usprivacy=1---; __host_color_scheme=OroIuZT9-WS6tbS3USMEtCWLmNlxewr5uKG3VFvuM5BdvutG-wto; __host_theme_options=1754719330201; algoliaUT=8ecf6b13-3f2e-4a70-b8c5-a1c2270da3db; AMCVS_8CF467C25245AE3F0A490D4C%40AdobeOrg=1; AMCV_8CF467C25245AE3F0A490D4C%40AdobeOrg=-408604571%7CMCIDTS%7C20310%7CMCMID%7C07870750718867146303300676330597253150%7CMCAAMLH-1755324135%7C11%7CMCAAMB-1755324135%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1754726535s%7CNONE%7CvVersion%7C4.6.0; s_cc=true; check=true; sailthru_pageviews=2; mbox=session#628b220029014c9d95ed7d8a3f0fddab#1754721199|PC#628b220029014c9d95ed7d8a3f0fddab.32_0#1817964139; _cb=CbIpSv6jLysBO2gxb; _chartbeat2=.1754719339385.1754719339385.1.CutXbdGDMYpBaOnCWCU1CL_C2pHP7.1; _cb_svref=external; _ALGOLIA=anonymous-9c16693a-6012-41f8-b579-13324a28efd5; _awl=2.1754719343.5-46e4aa6eb7366c86b4b942aff1232900-6763652d75732d7765737431-0; QSI_HistorySession=https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F~1754719344768; s_sq=wbrosrottentomatoes%3D%2526c.%2526a.%2526activitymap.%2526page%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526link%253DTV%252520SHOWS%2526region%253Dmain-page-content%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Drt%252520%25257C%252520browse%252520%25257C%252520list%252520page%252520%25257C%252520tv%252520series%252520browse%2526pidt%253D1%2526oid%253DTV%252520SHOWS%252520%2526oidt%253D3%2526ot%253DSUBMIT; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Aug+09+2025+14%3A22%3A15+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202309.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5697e666-99f7-4186-b4a7-e520e90d7efd&interactionCount=1&landingPath=https%3A%2F%2Fwww.rottentomatoes.com%2Fbrowse%2Ftv_series_browse%2F&groups=1%3A1%2C4%3A1%2C6%3A1%2C7%3A1%2COOF%3A1%2CUSP%3A1',
    }

    response = requests.get('https://www.rottentomatoes.com/browse/tv_series_browse', cookies=cookies, headers=headers)
    selector = parsel.Selector(response.text)
    data = selector.xpath('//script[@type="application/ld+json"]/text()').get()
    data = json.loads(data)
    itemListElements = data['itemListElement']['itemListElement']
    lfc = []
    data_list = []
    for item in itemListElements:
        data_list.append({
            'position': item['position'],
            'name': item['video']['name'] if item.get('video') else item['name'],
            'uploadDate': item['video']['uploadDate'] if item.get('video') else item['dateCreated'],
        })
    lfc.append({'tv_show': data_list})
    

    return lfc

if __name__ == '__main__':
    get_popular()


