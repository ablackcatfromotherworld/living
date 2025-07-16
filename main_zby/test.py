import time
import execjs
import html
import codecs
import datetime
# time_now = time.strftime("%Y%m%d", time.localtime())
# print(time_now)
time_now = datetime.datetime.now()
# delta_day = datetime.timedelta(days=30)
# time_now = (time_now + delta_day).strftime("%Y%m%d")
# print(time_now)

# time_now = [(time_now + datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(1,8)]
# print(time_now)
# import codecs
# a = b'Bom Dia S\\u00e1bado'
# temp_str = a.decode('ascii')
# final_str = codecs.decode(temp_str, 'unicode_escape')
# print(final_str)

# a = 'adkfl'
# print(a[:-1])
# time = execjs.compile('return new Date().getTime();').call('this')
# print(time)
# print(datetime.datetime.now().timestamp())

a = 'Igreja Internacional da Gra &#231;a de Deus'
# final = codecs.decode(a.encode('utf-8').decode('ascii'), 'unicode_escape')
# b = html.unescape(a)
# print(b)
# print(final)



import requests

# cookies = {
#     '__goc_session__': 'smnwkfokztusqmlkijuwxoerpzhtnlcc',
#     '_ga': 'GA1.1.584055248.1752560750',
#     'cebs': '1',
#     '_ce.clock_data': '-1703%2C154.205.156.51%2C1%2C7ddeda88d0c599cc494da0dece6554d5%2CChrome%2CBR',
#     'AdoptVisitorId': 'MbAmGYCYBYFNoLQEMCsAGAbA6BOAZnsuKABwJ5oDslAjKJOFUgEZA===',
#     '_gcl_au': '1.1.1707420601.1752560863',
#     'AdoptConsent': 'N4Ig7gpgRgzglgFwgSQCIgFwgBwBMDsAzIbgMYAsAtAKzYCc2l5u5plAhnblJQEz+l2AM2qEoEOoRAAaEADc48BAHsATslyYQpUrkK9yEKu2oAGAGxM6QoRxKMhp/PgCMuXoSfsoMkAlJCAMoIqnAAdgDmmGEArgA2cbLKAA4IyGEAKuwRMJgA2iAAjqYA0gAWAGJgALLsAFLsvtUAogioAIJwpNUAahm+uAAaymXNvMgA+qSmvlwASu0A6gBelEIAWmG+ADLsgXoAqgjbqC6+qHWocwBCANYAcmbUvgCeyoEl29QQAAoAigAJXyBIT3ADy7TCL1U1SBsjClCgQjoYVQhCEPlkEAupl47HuQgA4hVfGUXBUSgArIQAWwB418cXWclMLjKvBiUHwvgyuEpgTkAE1KbgJoFfOsvj8oLcaXESj8QABdJKpMExBBZHL5FXaZRhGAQMJpTRYKCqCbsMFwXykfWG409CCqeD6zAuFyyGLJXDsJC4doILS8XHUShOSguagZCwYQjUOMuAB0hHwpnWIAAvkA',
#     '_clck': 'abc2rt%7C2%7Cfxm%7C0%7C2022',
#     '_fbp': 'fb.1.1752561334162.109175519847087459',
#     'cebsp_': '7',
#     '_ce.s': 'v~32be081c38d9028ec76624555552b86f4f3d5b28~lcw~1752561382866~vir~new~lva~1752561474753~vpv~0~as~false~v11.cs~442463~v11.s~9222f400-6144-11f0-9ebf-23686ab4356d~v11.vs~32be081c38d9028ec76624555552b86f4f3d5b28~v11.fsvd~eyJ1cmwiOiJhMTIuY29tL3R2L3R2LWFvLXZpdm8iLCJyZWYiOiJodHRwczovL2dlbWluaS5nb29nbGUuY29tLyIsInV0bSI6W119~v11.sla~1752560758615~v11.ss~1752560758629~v11ls~9222f400-6144-11f0-9ebf-23686ab4356d~lcw~1752561474753',
#     '_clsk': 'rk0zku%7C1752561495935%7C3%7C1%7Cl.clarity.ms%2Fcollect',
#     '_ga_KYZX4Q19GD': 'GS2.1.s1752560749$o1$g1$t1752561526$j59$l0$h1805957124',
#     '_ga_50E4KZ468W': 'GS2.1.s1752560751$o1$g1$t1752561526$j60$l0$h0',
# }

headers = {
    #'referer': 'https://www.a12.com/tv/programacao?data=17-07-2025',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '__goc_session__=smnwkfokztusqmlkijuwxoerpzhtnlcc; _ga=GA1.1.584055248.1752560750; cebs=1; _ce.clock_data=-1703%2C154.205.156.51%2C1%2C7ddeda88d0c599cc494da0dece6554d5%2CChrome%2CBR; AdoptVisitorId=MbAmGYCYBYFNoLQEMCsAGAbA6BOAZnsuKABwJ5oDslAjKJOFUgEZA===; _gcl_au=1.1.1707420601.1752560863; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgBwBMDsAzIbgMYAsAtAKzYCc2l5u5plAhnblJQEz+l2AM2qEoEOoRAAaEADc48BAHsATslyYQpUrkK9yEKu2oAGAGxM6QoRxKMhp/PgCMuXoSfsoMkAlJCAMoIqnAAdgDmmGEArgA2cbLKAA4IyGEAKuwRMJgA2iAAjqYA0gAWAGJgALLsAFLsvtUAogioAIJwpNUAahm+uAAaymXNvMgA+qSmvlwASu0A6gBelEIAWmG+ADLsgXoAqgjbqC6+qHWocwBCANYAcmbUvgCeyoEl29QQAAoAigAJXyBIT3ADy7TCL1U1SBsjClCgQjoYVQhCEPlkEAupl47HuQgA4hVfGUXBUSgArIQAWwB418cXWclMLjKvBiUHwvgyuEpgTkAE1KbgJoFfOsvj8oLcaXESj8QABdJKpMExBBZHL5FXaZRhGAQMJpTRYKCqCbsMFwXykfWG409CCqeD6zAuFyyGLJXDsJC4doILS8XHUShOSguagZCwYQjUOMuAB0hHwpnWIAAvkA; _clck=abc2rt%7C2%7Cfxm%7C0%7C2022; _fbp=fb.1.1752561334162.109175519847087459; cebsp_=7; _ce.s=v~32be081c38d9028ec76624555552b86f4f3d5b28~lcw~1752561382866~vir~new~lva~1752561474753~vpv~0~as~false~v11.cs~442463~v11.s~9222f400-6144-11f0-9ebf-23686ab4356d~v11.vs~32be081c38d9028ec76624555552b86f4f3d5b28~v11.fsvd~eyJ1cmwiOiJhMTIuY29tL3R2L3R2LWFvLXZpdm8iLCJyZWYiOiJodHRwczovL2dlbWluaS5nb29nbGUuY29tLyIsInV0bSI6W119~v11.sla~1752560758615~v11.ss~1752560758629~v11ls~9222f400-6144-11f0-9ebf-23686ab4356d~lcw~1752561474753; _clsk=rk0zku%7C1752561495935%7C3%7C1%7Cl.clarity.ms%2Fcollect; _ga_KYZX4Q19GD=GS2.1.s1752560749$o1$g1$t1752561526$j59$l0$h1805957124; _ga_50E4KZ468W=GS2.1.s1752560751$o1$g1$t1752561526$j60$l0$h0',
}

params = {
    'data': '18-07-2025',
}

response = requests.get('https://www.a12.com/tv/programacao', params=params,headers=headers)
print(response.text)