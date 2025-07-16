import requests
from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Actions
from pathlib import Path
import parsel
import codecs
import json
import time
cookies = {
    '_gcl_au': '1.1.124352188.1747130524',
    'GBID': 'GBID.1747130523522.51cb3d8c-a3c0-4c26-8392-96d138e0e58b',
    '_evga_8981': '{%22uuid%22:%22b43ac7e4fd955cc0%22}',
    '_sfid_fd4e': '{%22anonymousId%22:%22b43ac7e4fd955cc0%22%2C%22consents%22:[]}',
    '_fbp': 'fb.1.1747130678732.67868538980030603',
    '_tt_enable_cookie': '1',
    '_ttp': '01JV4HN0F3HWT3Z4SWY6RXYGV2_.tt.1',
    '_scor_uid': 'a8ba5305524b473a907a0b7049037855',
    'cookie-banner-consent-accepted': 'true',
    'cookie-banner-accepted-version': '1.4.2.4',
    'glb_uid': 'tP7VYsnQ13jLAAZEl044uRa29kVFChdog-YB84oOAhE=',
    'gpixel_uid': 'tP7VYsnQ13jLAAZEl044uRa29kVFChdog-YB84oOAhE=',
    '_cc_id': '6e4cf98cbd54a186d5c972073da5702a',
    '_ym_uid': '1747130774624775093',
    '_ym_d': '1747130774',
    '_ga': 'GA1.3.1601349020.1747130692',
    '_lc2_fpi': 'da5812f14a1e--01jxvna4p4kxq8504p90w56j6y',
    '_lc2_fpi_meta': '%7B%22w%22%3A1750053753540%7D',
    'pbjs_sharedId': 'f2d26ae4-7179-43a4-b7c7-23c54e6d4b29',
    '_lr_env_src_ats': 'false',
    'compass_uid': 'e7a93525-f09b-4f11-a78e-3d12913928f1',
    'OptanonAlertBoxClosed': '2025-06-16T06:41:59.077Z',
    'pbjs_sharedId_cst': 'zix7LPQsHA%3D%3D',
    '___nrbic': '%7B%22sessionId%22%3A%2236882a88-a689-4d55-8815-42428e1fb00e%22%2C%22currentVisitStarted%22%3A1750055333%2C%22sessionVars%22%3A%5B%5D%2C%22lastBeat%22%3A1750056413%2C%22previousVisit%22%3A1750055333%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A1%2C%22landingPage%22%3A%22https%3A//g1.globo.com/globonews/%22%2C%22referrer%22%3A%22https%3A//www.lineup.tv.br/%22%2C%22lpti%22%3A%222018-07-26T19%3A09%3A53.280Z%22%7D',
    '___nrbi': '%7B%22firstVisit%22%3A1750055333%2C%22userId%22%3A%22e7a93525-f09b-4f11-a78e-3d12913928f1%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1750056413%2C%22timesVisited%22%3A2%7D',
    '_ga_HCQVSN1VBN': 'GS2.1.s1750056489$o1$g1$t1750057530$j60$l0$h439603389',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Jul+02+2025+17%3A08%3A47+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.38.0&isIABGlobal=false&hosts=&consentId=6a86992d-be2c-4411-840e-948b9c22ae73&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&iType=1&geolocation=US%3BWA&AwaitingReconsent=false',
    'GLBID': '163045356402aa56d95d5a7eff9f612b17a306878585164656e374a685a6c4474546c6442666d55657a667a3661695f3579613878785954344e4177516149394a6875694b4c4d4536344b5469496279715066556a667a53463364484851574f6a5461763776413d3d3a303a75346f6b366d6b6e30663362316a717031723334',
    'GLOBO_ID': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJnbG9ib0lkIjoiMDU1ZGJmZjgtZWM3Yi00ZGI4LWI2ODgtNGEzZmEyNmVmZTBhIiwgInVzZXJOYW1lIjoiYmxhY2sgY2F0IiwgInBob3RvVXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0hOUHFlaW45YmRVU3g3TFpnZmt0aW5teXpMNlJrRHZVV2c1bk1LM3pHRDVqSHd0Yz1zOTYtYyJ9.qyKTXH-z0ZP975PcFp_AqtUqFQi7yutyUXhGmgL2S1Enxef5N2pN_Wa-PFwwhldDkXAeBrGbb39_BdH1FO-pMx6fQK9WX-VxmvHOS_V1TX_0g1cBNKLcDhJm9CyWsxdRKRI6B80wVf9dy4sBdO3WzI-csiANjjWTB_xNQ2q15uQlTvq3npP-jBKvO4UG-D4frWuKoVH8WNjONBjt6ExLok9LCx_r-C8UHpvrxEJ5AETEOYBo5vAM9pS3if1iR-N4ITtC7TB01vtuC4IDBbuXVFjgpjUFTFQxAkOYZPGE9ivlMLLA8D8OExk53f7bxNF79yqqxzMvJ1CjtEQx4aM-RQ',
    '_ga_G5YX0X0P68': 'GS2.1.s1752118369$o2$g1$t1752118457$j44$l0$h0',
    'utag_main': 'v_id:0197f26607a000680824b235f9b00506f024d06700a83$_sn:1$_ss:1$_st:1752120262368$ses_id:1752118462368%3Bexp-session$_pn:1%3Bexp-session',
    '_ga_WLHSK1RZ32': 'GS2.1.s1752126457$o7$g1$t1752126482$j35$l0$h549488848',
    'ttcsid_CS2543JC77U61CV1R35G': '1752126501227::6SqgOj_a4SSU3KfO9QzD.7.1752126554023',
    'ttcsid_D0AH3JRC77UD5RFHJE10': '1752126501228::ys81CTQf6vtH0ZxiWEpj.7.1752126554034',
    'ttcsid': '1752126501228::6S6vVwePMDdasucL635E.7.1752126559463',
    'ttcsid_C5NM1IDO3VNUQLVLF980': '1752126559455::mcZpfP86Ifzo3MCxxII-.6.1752126559785',
    'permutive-id': '8de706d0-9085-459b-a90b-fa104a606def',
    'panoramaId_expiry': '1752825077025',
    'panoramaId': '9f3519d22907065c235002ab4393185ca02cdc7cf67fdb29449656a22ca7a758',
    'panoramaIdType': 'panoDevice',
    '_lr_sampling_rate': '100',
    '_li_dcdm_c': '.globo.com',
    '_lr_retry_request': 'true',
    'pbjs_li_nonid': '%7B%22nonId%22%3A%2218-oxqh6FLCL3k1TbWOPxugBAKWb%2B1LwhBfkKm3FkQfq94zG0uo0MX4NUmbktkwnjh1Ar3AGrqJg2kWpq82HInMIXBI%2FZvedNgt6xNPislVfZD8ZQ%3D%3D%22%7D',
    'pbjs_li_nonid_cst': 'zix7LPQsHA%3D%3D',
    '_gid': 'GA1.2.102484174.1752458052',
    'cto_bidid': 'lyclCF9YVVZSOTdrNnE2UGdEOGhKNWx0TVdoR0MzZmNnMW82c3NKbzFmeVJDQXRuaEFRUlpLSHRUZGl2M3JFeldkZlFtOXdUVnVxOG0wMEFJdEdMJTJCWTljaTRNUGVXUG5ja2haRUR2eDBPUzBCajI0JTNE',
    'hsid': '75e692fa-376a-462d-9ab0-65753e1ecc80',
    '_clck': '1tfgyj9%7C2%7Cfxl%7C0%7C2018',
    '__gads': 'ID=e6817da217de5d2b:T=1750053754:RT=1752458056:S=ALNI_MZyn5BJnvosgDW55B_mADdDNwPtoQ',
    '__gpi': 'UID=000011052b3e44a2:T=1750053754:RT=1752458056:S=ALNI_Mb5WzheMqW5j_KOhwtz-wLv4Qm85A',
    '__eoi': 'ID=571ee0c22f01613b:T=1750053754:RT=1752458056:S=AA-AfjZWfOiybOwnVI_yfFxoFFOh',
    'cto_bundle': '_VW6YV8wYlJYMmRvVTBhSXN5V1pwTEx5YjBUQW16bW02MzROZnZvSkxwTXEwdUF6Y0FVMEtpMmRNTTIyV1lWcGpYVHRDT2lJWHgyTU5IRkk1bkQwQ0h1NHJCZ3VXaUxoU3BZSFhFS3FBYXlaT3hoUGZBYU9PNVlURmFJdjJ6emdFU3haJTJGZ1oyaTRuNFZpMCUyQm9iNE5YSWR5dFU4QXVGaWtuSUExJTJGOGNKTEtQMzdMZG1WWVZRTDY1YWNaU1FUYzclMkZVOTN4YnE5ekE5SE5iRWVNMFREelgwbUVQUlElM0QlM0Q',
    '_ga_5401XJ0K8J': 'GS2.1.s1752458137$o3$g0$t1752458137$j60$l0$h0',
    '_ga': 'GA1.1.1601349020.1747130692',
    'FCNEC': '%5B%5B%22AKsRol-vvC8P8mS_l8WhwbpUbwLaQfd4nouqVhVi_QTMavBJ749KDo1II8OW2BrDibNAB_L2hg-HAf3Of7UxYiJBfsMol6uRdL-3sKqlM4Rw61S0cJpnZP_c93lw3JCDwGTfp2479eUS3O7hqPPI_R-hJO0nBTaGLw%3D%3D%22%5D%5D',
    '_clsk': '1ap5qii%7C1752458927973%7C6%7C1%7Cq.clarity.ms%2Fcollect',
    '_ga_7D6HZKQYC8': 'GS2.1.s1752458051$o4$g1$t1752459137$j57$l0$h0',
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
    # 'cookie': '_gcl_au=1.1.124352188.1747130524; GBID=GBID.1747130523522.51cb3d8c-a3c0-4c26-8392-96d138e0e58b; _evga_8981={%22uuid%22:%22b43ac7e4fd955cc0%22}; _sfid_fd4e={%22anonymousId%22:%22b43ac7e4fd955cc0%22%2C%22consents%22:[]}; _fbp=fb.1.1747130678732.67868538980030603; _tt_enable_cookie=1; _ttp=01JV4HN0F3HWT3Z4SWY6RXYGV2_.tt.1; _scor_uid=a8ba5305524b473a907a0b7049037855; cookie-banner-consent-accepted=true; cookie-banner-accepted-version=1.4.2.4; glb_uid=tP7VYsnQ13jLAAZEl044uRa29kVFChdog-YB84oOAhE=; gpixel_uid=tP7VYsnQ13jLAAZEl044uRa29kVFChdog-YB84oOAhE=; _cc_id=6e4cf98cbd54a186d5c972073da5702a; _ym_uid=1747130774624775093; _ym_d=1747130774; _ga=GA1.3.1601349020.1747130692; _lc2_fpi=da5812f14a1e--01jxvna4p4kxq8504p90w56j6y; _lc2_fpi_meta=%7B%22w%22%3A1750053753540%7D; pbjs_sharedId=f2d26ae4-7179-43a4-b7c7-23c54e6d4b29; _lr_env_src_ats=false; compass_uid=e7a93525-f09b-4f11-a78e-3d12913928f1; OptanonAlertBoxClosed=2025-06-16T06:41:59.077Z; pbjs_sharedId_cst=zix7LPQsHA%3D%3D; ___nrbic=%7B%22sessionId%22%3A%2236882a88-a689-4d55-8815-42428e1fb00e%22%2C%22currentVisitStarted%22%3A1750055333%2C%22sessionVars%22%3A%5B%5D%2C%22lastBeat%22%3A1750056413%2C%22previousVisit%22%3A1750055333%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A1%2C%22landingPage%22%3A%22https%3A//g1.globo.com/globonews/%22%2C%22referrer%22%3A%22https%3A//www.lineup.tv.br/%22%2C%22lpti%22%3A%222018-07-26T19%3A09%3A53.280Z%22%7D; ___nrbi=%7B%22firstVisit%22%3A1750055333%2C%22userId%22%3A%22e7a93525-f09b-4f11-a78e-3d12913928f1%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1750056413%2C%22timesVisited%22%3A2%7D; _ga_HCQVSN1VBN=GS2.1.s1750056489$o1$g1$t1750057530$j60$l0$h439603389; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Jul+02+2025+17%3A08%3A47+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.38.0&isIABGlobal=false&hosts=&consentId=6a86992d-be2c-4411-840e-948b9c22ae73&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&iType=1&geolocation=US%3BWA&AwaitingReconsent=false; GLBID=163045356402aa56d95d5a7eff9f612b17a306878585164656e374a685a6c4474546c6442666d55657a667a3661695f3579613878785954344e4177516149394a6875694b4c4d4536344b5469496279715066556a667a53463364484851574f6a5461763776413d3d3a303a75346f6b366d6b6e30663362316a717031723334; GLOBO_ID=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJnbG9ib0lkIjoiMDU1ZGJmZjgtZWM3Yi00ZGI4LWI2ODgtNGEzZmEyNmVmZTBhIiwgInVzZXJOYW1lIjoiYmxhY2sgY2F0IiwgInBob3RvVXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jS0hOUHFlaW45YmRVU3g3TFpnZmt0aW5teXpMNlJrRHZVV2c1bk1LM3pHRDVqSHd0Yz1zOTYtYyJ9.qyKTXH-z0ZP975PcFp_AqtUqFQi7yutyUXhGmgL2S1Enxef5N2pN_Wa-PFwwhldDkXAeBrGbb39_BdH1FO-pMx6fQK9WX-VxmvHOS_V1TX_0g1cBNKLcDhJm9CyWsxdRKRI6B80wVf9dy4sBdO3WzI-csiANjjWTB_xNQ2q15uQlTvq3npP-jBKvO4UG-D4frWuKoVH8WNjONBjt6ExLok9LCx_r-C8UHpvrxEJ5AETEOYBo5vAM9pS3if1iR-N4ITtC7TB01vtuC4IDBbuXVFjgpjUFTFQxAkOYZPGE9ivlMLLA8D8OExk53f7bxNF79yqqxzMvJ1CjtEQx4aM-RQ; _ga_G5YX0X0P68=GS2.1.s1752118369$o2$g1$t1752118457$j44$l0$h0; utag_main=v_id:0197f26607a000680824b235f9b00506f024d06700a83$_sn:1$_ss:1$_st:1752120262368$ses_id:1752118462368%3Bexp-session$_pn:1%3Bexp-session; _ga_WLHSK1RZ32=GS2.1.s1752126457$o7$g1$t1752126482$j35$l0$h549488848; ttcsid_CS2543JC77U61CV1R35G=1752126501227::6SqgOj_a4SSU3KfO9QzD.7.1752126554023; ttcsid_D0AH3JRC77UD5RFHJE10=1752126501228::ys81CTQf6vtH0ZxiWEpj.7.1752126554034; ttcsid=1752126501228::6S6vVwePMDdasucL635E.7.1752126559463; ttcsid_C5NM1IDO3VNUQLVLF980=1752126559455::mcZpfP86Ifzo3MCxxII-.6.1752126559785; permutive-id=8de706d0-9085-459b-a90b-fa104a606def; panoramaId_expiry=1752825077025; panoramaId=9f3519d22907065c235002ab4393185ca02cdc7cf67fdb29449656a22ca7a758; panoramaIdType=panoDevice; _lr_sampling_rate=100; _li_dcdm_c=.globo.com; _lr_retry_request=true; pbjs_li_nonid=%7B%22nonId%22%3A%2218-oxqh6FLCL3k1TbWOPxugBAKWb%2B1LwhBfkKm3FkQfq94zG0uo0MX4NUmbktkwnjh1Ar3AGrqJg2kWpq82HInMIXBI%2FZvedNgt6xNPislVfZD8ZQ%3D%3D%22%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; _gid=GA1.2.102484174.1752458052; cto_bidid=lyclCF9YVVZSOTdrNnE2UGdEOGhKNWx0TVdoR0MzZmNnMW82c3NKbzFmeVJDQXRuaEFRUlpLSHRUZGl2M3JFeldkZlFtOXdUVnVxOG0wMEFJdEdMJTJCWTljaTRNUGVXUG5ja2haRUR2eDBPUzBCajI0JTNE; hsid=75e692fa-376a-462d-9ab0-65753e1ecc80; _clck=1tfgyj9%7C2%7Cfxl%7C0%7C2018; __gads=ID=e6817da217de5d2b:T=1750053754:RT=1752458056:S=ALNI_MZyn5BJnvosgDW55B_mADdDNwPtoQ; __gpi=UID=000011052b3e44a2:T=1750053754:RT=1752458056:S=ALNI_Mb5WzheMqW5j_KOhwtz-wLv4Qm85A; __eoi=ID=571ee0c22f01613b:T=1750053754:RT=1752458056:S=AA-AfjZWfOiybOwnVI_yfFxoFFOh; cto_bundle=_VW6YV8wYlJYMmRvVTBhSXN5V1pwTEx5YjBUQW16bW02MzROZnZvSkxwTXEwdUF6Y0FVMEtpMmRNTTIyV1lWcGpYVHRDT2lJWHgyTU5IRkk1bkQwQ0h1NHJCZ3VXaUxoU3BZSFhFS3FBYXlaT3hoUGZBYU9PNVlURmFJdjJ6emdFU3haJTJGZ1oyaTRuNFZpMCUyQm9iNE5YSWR5dFU4QXVGaWtuSUExJTJGOGNKTEtQMzdMZG1WWVZRTDY1YWNaU1FUYzclMkZVOTN4YnE5ekE5SE5iRWVNMFREelgwbUVQUlElM0QlM0Q; _ga_5401XJ0K8J=GS2.1.s1752458137$o3$g0$t1752458137$j60$l0$h0; _ga=GA1.1.1601349020.1747130692; FCNEC=%5B%5B%22AKsRol-vvC8P8mS_l8WhwbpUbwLaQfd4nouqVhVi_QTMavBJ749KDo1II8OW2BrDibNAB_L2hg-HAf3Of7UxYiJBfsMol6uRdL-3sKqlM4Rw61S0cJpnZP_c93lw3JCDwGTfp2479eUS3O7hqPPI_R-hJO0nBTaGLw%3D%3D%22%5D%5D; _clsk=1ap5qii%7C1752458927973%7C6%7C1%7Cq.clarity.ms%2Fcollect; _ga_7D6HZKQYC8=GS2.1.s1752458051$o4$g1$t1752459137$j57$l0$h0',
}
path = Path(__file__).parent

# response = requests.get('https://redeglobo.globo.com/sao-paulo/programacao/', cookies=cookies, headers=headers)

# selector = parsel.Selector(response.text)
# accordions = selector.xpath('//div[@class="accordion"]')
# for accordion in accordions:
#     time = accordion.xpath('./div[@class="accordionTitle__time"]/time/p/text()').get()
#     log = accordion.xpath('./div[@class="accordionTitle__logo"]/img/@src').get()
#     name = accordion.xpath('./div[@class="accordionTitle__name"]/p/text()').get()
co = ChromiumOptions().auto_port()
tab = Chromium(co).latest_tab
tab.set.load_mode.eager()
data = []
ac = Actions(tab)
tab.get('https://redeglobo.globo.com/sao-paulo/programacao/')
dateselectorv2__dates = tab.eles('x://ul[@class="date-selector-v2__dates"]/li/button')
for dateselectorv2__date in dateselectorv2__dates:
    ac.move_to(dateselectorv2__date).click()
    tab.wait(1)
    # date = tab.ele('x://p[@class="a11y.day-agenda__a11y-description"]/text()')

    x = []
    accordions = tab.eles('x://div[@class="accordion"]')
    
    print(len(accordions))
    date = accordions[0].ele('x:./@id')[:-1]
    # print(date)
    for accordion in accordions:
        time = accordion.ele('x:.//div[@class="accordionTitle__time"]/time/p/text()')
        log = accordion.ele('x:.//div[@class="accordionTitle__logo"]/img/@src')
        name = accordion.ele('x:.//div[@class="accordionTitle__name"]/p/text()')
        x.append({'time':time, 'log':log, 'name':name})
    data.append({date:x})


# with open(path / 'globo.html', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(response.text))
with open(path / 'globo.jaon', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data))