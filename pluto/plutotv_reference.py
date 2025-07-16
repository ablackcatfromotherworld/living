# import requests

# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRmZGE2YjE2LWFjYzItNGVmYS04ZjY5LTE2ZjQwMGJmNzdmMCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJjODczNzg2OC01Yzc2LTExZjAtYjZiNi1iYWNmNGFlNzk3ODYiLCJjbGllbnRJUCI6IjM4LjE2NS4yLjM5IiwiY2l0eSI6IkxvcyBBbmdlbGVzIiwicG9zdGFsQ29kZSI6IjkwMDExIiwiY291bnRyeSI6IlVTIiwiZG1hIjo4MDMsImFjdGl2ZVJlZ2lvbiI6IlVTIiwiZGV2aWNlTGF0IjozNC4wMDk5OTgzMjE1MzMyLCJkZXZpY2VMb24iOi0xMTguMjYwMDAyMTM2MjMwNDcsInByZWZlcnJlZExhbmd1YWdlIjoiemgiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEzOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMTQuMS1jYTYwOThiYjVkMWYyZGI2OGMyY2NjY2Y2MDgzNDZmMjE2NTFmMDAzIiwiY2xpZW50SUQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzZXJ2ZXJTaWRlQWRzIjpmYWxzZSwiZTJlQmVhY29ucyI6ZmFsc2UsImZlYXR1cmVzIjp7ImFkTG9hZCI6eyJjb2hvcnQiOiIifSwibXVsdGlBdWRpbyI6eyJlbmFibGVkIjp0cnVlfSwibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX0sInNlYXJjaEFQSSI6eyJtYXRjaEV4YWN0SW5QaHJhc2VFbmFibGVkIjp0cnVlLCJtYXRjaEluQWN0b3JzQm9vc3QiOjI1LCJtYXRjaEluQWN0b3JzRWRpdERpc3RhbmNlIjoiQVVUTzo1LDExIiwibWF0Y2hJbkFjdG9yc0VuYWJsZWQiOnRydWUsIm1hdGNoSW5EaXJlY3RvcnNCb29zdCI6MjUsIm1hdGNoSW5EaXJlY3RvcnNFZGl0RGlzdGFuY2UiOiJBVVRPOjUsMTEiLCJtYXRjaEluRGlyZWN0b3JzRW5hYmxlZCI6dHJ1ZSwibmV4dXNUaW1lb3V0TXMiOjUwMCwicXVlcnlTeW5vbnltc0VuYWJsZWQiOnRydWUsInF1ZXJ5VmVyc2lvbiI6Imh5YnJpZCIsInNlYXJjaFByb3h5RW5oYW5jZW1lbnQiOmZhbHNlLCJ0aXRsZUF2YWlsYWJpbGl0eURldGVybWluYXRpb24iOmZhbHNlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZmY4ZjIwOGU0NDRlMWJkZWNiODk4YWIxMThmMzMyNzFkNTEyNjgzMmQ2ZThkNTQ5MTI1M2VmODUyM2E1Mzc5YiIsImZ3VmNJRDJDb3BwYSI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImZmOGYyMDhlNDQ0ZTFiZGVjYjg5OGFiMTE4ZjMzMjcxZDUxMjY4MzJkNmU4ZDU0OTEyNTNlZjg1MjNhNTM3OWIiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjg2NDlhMzlkZTYxZWZjM2E0MmU3OGIzIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IjEwNDAsMTA1MCwxMDMwLDEwMTAsMTA3MCwxMDgwIiwiX2Z3XzNQX1VJRCI6IklETDpBbUJaNllwTEZoVVNJa0F0R2t3S21SbnVwWldOQnZVelhIVjJPeUNHSlZGOXdFcHlxSmN2WDRQay02UDQxamthOW1oREZ0M2Vienk1eXFZaGFHZEo5Q21OZG00b0xVUWlSN2QyRldCN2tYYmZvRmlFRHFkR2hpdlhzWWZYNDFfXy0yVDRLd0tobWJCV2o4T3JNMlRfVXJ4TTNpVkhaUGNBMXNQMm1WZi02Vlh4RnU2NVZpeWx2NmUyT0NEdDgxR0xPQU1YbnZWUixQQUlSSUQ6QTNhRFVDeG8vOVRiZXZ1ZU9Cc1BhRis2eGxvL0ROemZrMUdSWUdnK3lvaFUsY29ubmVjdGlkOlY4amdOekNTWEhFbDNJNlZRRXRLOXpjMjA4LXRYem8tWFE3VlVFWkYtTWpmekJmNXI2aDk3cWRra1YwWDV3Vi1wbURZd2dmcWZPQU5yQ0xkenBINFVnLFVJRDI6QTRBQUFCS3JGQ01lcnEwaElFZ0M1NENMc3ZXUVRabEFOTm12QWUweGlVblBaX055OWdCOWRqb3dab3JETkZjbzJfdkRsV3BvRXJfbTU0Q19zemh2RFVKbzNpblR1X285ZHg5ODdUOFJfVzI5bnVhY1RYVG5IT20xSXBLZkJSNFBLQ3hMWUM2S25JT0dZa1pkTjFrcm1TazY3VHRXcWU2WHExRlY1Qm9sSXVueDJqOXUxclRwWHNHWm5TYkVpMFVOMFJyQXlHa0lSM1QySjNvMG1jeEhDMUViR0EsVklBTlRQOmIwZGFkNjc3NGViZGJkYTRhYWNmNmM1NzJkYWJmZDZmMTA4ZDFlZDMxZjYxMzk2NWQ1MDlhMWI3YzQ2ZTExNDksVElOVUlUSTo5YzM3ZWJhYjU4MDBiMTJkMTQ5MTAyMThkMWUwZDhiZTQyYWY2MjJlYWJhM2YyYzQzZGIxMDM5NDU5OTUyYjAwIiwiZm1zX3J1bGVpZCI6IjEwMDAwIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJhZFBvZFBhcmFtcyI6eyJhZ2UiOjIsImdlbmRlciI6MH0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VVM6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3OjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3NTIxMTkwMjYsImlhdCI6MTc1MjAzMjYyNiwianRpIjoiZTRkODI4ZDgtZjZiZi00OTk3LTk1Y2QtZmFmZWYzZDcxNDI3In0.IG9e2UzSs3ftiXvm33DI3STcWUUDnaSrFbco7HzMT6c',
#     'cache-control': 'no-cache',
#     'origin': 'https://pluto.tv',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://pluto.tv/',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
# }

# params = {
#     'channelIds': '',
#     'offset': '0',
#     'limit': '1000',
#     'sort': 'number:asc',
# }

# response = requests.get('https://service-channels.clusters.pluto.tv/v2/guide/channels', params=params, headers=headers)

# print(len(response.json().get('data')))
# 396

# import requests
# import json
# from pathlib import Path

# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRmZGE2YjE2LWFjYzItNGVmYS04ZjY5LTE2ZjQwMGJmNzdmMCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJjM2M5NDg3Ni01YzZhLTExZjAtODNkYy1kZTE0YmE5MjkwNDIiLCJjbGllbnRJUCI6IjM4LjE2NS4yLjM5IiwiY2l0eSI6IkxvcyBBbmdlbGVzIiwicG9zdGFsQ29kZSI6IjkwMDExIiwiY291bnRyeSI6IlVTIiwiZG1hIjo4MDMsImFjdGl2ZVJlZ2lvbiI6IlVTIiwiZGV2aWNlTGF0IjozNC4wMDk5OTgzMjE1MzMyLCJkZXZpY2VMb24iOi0xMTguMjYwMDAyMTM2MjMwNDcsInByZWZlcnJlZExhbmd1YWdlIjoiemgiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEzOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMTQuMS1jYTYwOThiYjVkMWYyZGI2OGMyY2NjY2Y2MDgzNDZmMjE2NTFmMDAzIiwiY2xpZW50SUQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzZXJ2ZXJTaWRlQWRzIjpmYWxzZSwiZTJlQmVhY29ucyI6ZmFsc2UsImZlYXR1cmVzIjp7ImFkTG9hZCI6eyJjb2hvcnQiOiIifSwibXVsdGlBdWRpbyI6eyJlbmFibGVkIjp0cnVlfSwibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX0sInNlYXJjaEFQSSI6eyJtYXRjaEV4YWN0SW5QaHJhc2VFbmFibGVkIjp0cnVlLCJtYXRjaEluQWN0b3JzQm9vc3QiOjI1LCJtYXRjaEluQWN0b3JzRWRpdERpc3RhbmNlIjoiQVVUTzo1LDExIiwibWF0Y2hJbkFjdG9yc0VuYWJsZWQiOnRydWUsIm1hdGNoSW5EaXJlY3RvcnNCb29zdCI6MjUsIm1hdGNoSW5EaXJlY3RvcnNFZGl0RGlzdGFuY2UiOiJBVVRPOjUsMTEiLCJtYXRjaEluRGlyZWN0b3JzRW5hYmxlZCI6dHJ1ZSwibmV4dXNUaW1lb3V0TXMiOjUwMCwicXVlcnlTeW5vbnltc0VuYWJsZWQiOnRydWUsInF1ZXJ5VmVyc2lvbiI6Imh5YnJpZCIsInNlYXJjaFByb3h5RW5oYW5jZW1lbnQiOmZhbHNlLCJ0aXRsZUF2YWlsYWJpbGl0eURldGVybWluYXRpb24iOmZhbHNlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZmY4ZjIwOGU0NDRlMWJkZWNiODk4YWIxMThmMzMyNzFkNTEyNjgzMmQ2ZThkNTQ5MTI1M2VmODUyM2E1Mzc5YiIsImZ3VmNJRDJDb3BwYSI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImZmOGYyMDhlNDQ0ZTFiZGVjYjg5OGFiMTE4ZjMzMjcxZDUxMjY4MzJkNmU4ZDU0OTEyNTNlZjg1MjNhNTM3OWIiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjg2NDlhMzlkZTYxZWZjM2E0MmU3OGIzIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IjEwNDAsMTA1MCwxMDMwLDEwMTAsMTA3MCwxMDgwIiwiX2Z3XzNQX1VJRCI6IklETDpBbUJaNllwTEZoVVNJa0F0R2t3S21SbnVwWldOQnZVelhIVjJPeUNHSlZGOXdFcHlxSmN2WDRQay02UDQxamthOW1oREZ0M2Vienk1eXFZaGFHZEo5Q21OZG00b0xVUWlSN2QyRldCN2tYYmZvRmlFRHFkR2hpdlhzWWZYNDFfXy0yVDRLd0tobWJCV2o4T3JNMlRfVXJ4TTNpVkhaUGNBMXNQMm1WZi02Vlh4RnU2NVZpeWx2NmUyT0NEdDgxR0xPQU1YbnZWUixQQUlSSUQ6QTNhRFVDeG8vOVRiZXZ1ZU9Cc1BhRis2eGxvL0ROemZrMUdSWUdnK3lvaFUsY29ubmVjdGlkOlY4amdOekNTWEhFbDNJNlZRRXRLOXpjMjA4LXRYem8tWFE3VlVFWkYtTWpmekJmNXI2aDk3cWRra1YwWDV3Vi1wbURZd2dmcWZPQU5yQ0xkenBINFVnLFVJRDI6QTRBQUFCS3JGQ01lcnEwaElFZ0M1NENMc3ZXUVRabEFOTm12QWUweGlVblBaX055OWdCOWRqb3dab3JETkZjbzJfdkRsV3BvRXJfbTU0Q19zemh2RFVKbzNpblR1X285ZHg5ODdUOFJfVzI5bnVhY1RYVG5IT20xSXBLZkJSNFBLQ3hMWUM2S25JT0dZa1pkTjFrcm1TazY3VHRXcWU2WHExRlY1Qm9sSXVueDJqOXUxclRwWHNHWm5TYkVpMFVOMFJyQXlHa0lSM1QySjNvMG1jeEhDMUViR0EsVklBTlRQOmIwZGFkNjc3NGViZGJkYTRhYWNmNmM1NzJkYWJmZDZmMTA4ZDFlZDMxZjYxMzk2NWQ1MDlhMWI3YzQ2ZTExNDksVElOVUlUSTo5YzM3ZWJhYjU4MDBiMTJkMTQ5MTAyMThkMWUwZDhiZTQyYWY2MjJlYWJhM2YyYzQzZGIxMDM5NDU5OTUyYjAwIiwiZm1zX3J1bGVpZCI6IjEwMDAwIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJhZFBvZFBhcmFtcyI6eyJhZ2UiOjIsImdlbmRlciI6MH0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VVM6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3OjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3NTIxMTM4MTMsImlhdCI6MTc1MjAyNzQxMywianRpIjoiMTUwZjc2YzMtNzYzNC00ZDdiLWJlZTYtNjZkMjRmZGUwYmEwIn0.Zc2UAs0WKRhG46q_1Fh01emZGsQIpKs3aK7lJv0k-8M',
#     'cache-control': 'no-cache',
#     'origin': 'https://pluto.tv',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://pluto.tv/',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
# }
# path = Path(__file__).parent

# response = requests.get('https://service-channels.clusters.pluto.tv/v2/guide/categories', headers=headers)
# data = response.json().get('data')
# a = []
# for i in data:
#     for j in i.get('channelIDs'):
#         a.append(j)
# print(len(a))
# print(len(set(a)))

# import requests
# from pathlib import Path
# import json

# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRmZGE2YjE2LWFjYzItNGVmYS04ZjY5LTE2ZjQwMGJmNzdmMCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJjODczNzg2OC01Yzc2LTExZjAtYjZiNi1iYWNmNGFlNzk3ODYiLCJjbGllbnRJUCI6IjM4LjE2NS4yLjM5IiwiY2l0eSI6IkxvcyBBbmdlbGVzIiwicG9zdGFsQ29kZSI6IjkwMDExIiwiY291bnRyeSI6IlVTIiwiZG1hIjo4MDMsImFjdGl2ZVJlZ2lvbiI6IlVTIiwiZGV2aWNlTGF0IjozNC4wMDk5OTgzMjE1MzMyLCJkZXZpY2VMb24iOi0xMTguMjYwMDAyMTM2MjMwNDcsInByZWZlcnJlZExhbmd1YWdlIjoiemgiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEzOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMTQuMS1jYTYwOThiYjVkMWYyZGI2OGMyY2NjY2Y2MDgzNDZmMjE2NTFmMDAzIiwiY2xpZW50SUQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzZXJ2ZXJTaWRlQWRzIjpmYWxzZSwiZTJlQmVhY29ucyI6ZmFsc2UsImZlYXR1cmVzIjp7ImFkTG9hZCI6eyJjb2hvcnQiOiIifSwibXVsdGlBdWRpbyI6eyJlbmFibGVkIjp0cnVlfSwibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX0sInNlYXJjaEFQSSI6eyJtYXRjaEV4YWN0SW5QaHJhc2VFbmFibGVkIjp0cnVlLCJtYXRjaEluQWN0b3JzQm9vc3QiOjI1LCJtYXRjaEluQWN0b3JzRWRpdERpc3RhbmNlIjoiQVVUTzo1LDExIiwibWF0Y2hJbkFjdG9yc0VuYWJsZWQiOnRydWUsIm1hdGNoSW5EaXJlY3RvcnNCb29zdCI6MjUsIm1hdGNoSW5EaXJlY3RvcnNFZGl0RGlzdGFuY2UiOiJBVVRPOjUsMTEiLCJtYXRjaEluRGlyZWN0b3JzRW5hYmxlZCI6dHJ1ZSwibmV4dXNUaW1lb3V0TXMiOjUwMCwicXVlcnlTeW5vbnltc0VuYWJsZWQiOnRydWUsInF1ZXJ5VmVyc2lvbiI6Imh5YnJpZCIsInNlYXJjaFByb3h5RW5oYW5jZW1lbnQiOmZhbHNlLCJ0aXRsZUF2YWlsYWJpbGl0eURldGVybWluYXRpb24iOmZhbHNlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZmY4ZjIwOGU0NDRlMWJkZWNiODk4YWIxMThmMzMyNzFkNTEyNjgzMmQ2ZThkNTQ5MTI1M2VmODUyM2E1Mzc5YiIsImZ3VmNJRDJDb3BwYSI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImZmOGYyMDhlNDQ0ZTFiZGVjYjg5OGFiMTE4ZjMzMjcxZDUxMjY4MzJkNmU4ZDU0OTEyNTNlZjg1MjNhNTM3OWIiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjg2NDlhMzlkZTYxZWZjM2E0MmU3OGIzIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IjEwNDAsMTA1MCwxMDMwLDEwMTAsMTA3MCwxMDgwIiwiX2Z3XzNQX1VJRCI6IklETDpBbUJaNllwTEZoVVNJa0F0R2t3S21SbnVwWldOQnZVelhIVjJPeUNHSlZGOXdFcHlxSmN2WDRQay02UDQxamthOW1oREZ0M2Vienk1eXFZaGFHZEo5Q21OZG00b0xVUWlSN2QyRldCN2tYYmZvRmlFRHFkR2hpdlhzWWZYNDFfXy0yVDRLd0tobWJCV2o4T3JNMlRfVXJ4TTNpVkhaUGNBMXNQMm1WZi02Vlh4RnU2NVZpeWx2NmUyT0NEdDgxR0xPQU1YbnZWUixQQUlSSUQ6QTNhRFVDeG8vOVRiZXZ1ZU9Cc1BhRis2eGxvL0ROemZrMUdSWUdnK3lvaFUsY29ubmVjdGlkOlY4amdOekNTWEhFbDNJNlZRRXRLOXpjMjA4LXRYem8tWFE3VlVFWkYtTWpmekJmNXI2aDk3cWRra1YwWDV3Vi1wbURZd2dmcWZPQU5yQ0xkenBINFVnLFVJRDI6QTRBQUFCS3JGQ01lcnEwaElFZ0M1NENMc3ZXUVRabEFOTm12QWUweGlVblBaX055OWdCOWRqb3dab3JETkZjbzJfdkRsV3BvRXJfbTU0Q19zemh2RFVKbzNpblR1X285ZHg5ODdUOFJfVzI5bnVhY1RYVG5IT20xSXBLZkJSNFBLQ3hMWUM2S25JT0dZa1pkTjFrcm1TazY3VHRXcWU2WHExRlY1Qm9sSXVueDJqOXUxclRwWHNHWm5TYkVpMFVOMFJyQXlHa0lSM1QySjNvMG1jeEhDMUViR0EsVklBTlRQOmIwZGFkNjc3NGViZGJkYTRhYWNmNmM1NzJkYWJmZDZmMTA4ZDFlZDMxZjYxMzk2NWQ1MDlhMWI3YzQ2ZTExNDksVElOVUlUSTo5YzM3ZWJhYjU4MDBiMTJkMTQ5MTAyMThkMWUwZDhiZTQyYWY2MjJlYWJhM2YyYzQzZGIxMDM5NDU5OTUyYjAwIiwiZm1zX3J1bGVpZCI6IjEwMDAwIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJhZFBvZFBhcmFtcyI6eyJhZ2UiOjIsImdlbmRlciI6MH0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VVM6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3OjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3NTIxMTkwMjYsImlhdCI6MTc1MjAzMjYyNiwianRpIjoiZTRkODI4ZDgtZjZiZi00OTk3LTk1Y2QtZmFmZWYzZDcxNDI3In0.IG9e2UzSs3ftiXvm33DI3STcWUUDnaSrFbco7HzMT6c',
#     'cache-control': 'no-cache',
#     'origin': 'https://pluto.tv',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://pluto.tv/',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
# }

# params = {
#     'offset': '1000',
#     'page': '1',
# }
# path = Path(__file__).parent


# response = requests.get(
#     'https://service-vod.clusters.pluto.tv/v4/vod/categories/6018833064d99100075a1e8a/items',
#     params=params,
#     headers=headers,
# )

# print(len(response.json().get('items')))
# print(response.json().get('items'))
# with open(path / 'items.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(response.json().get('items')))


# import requests
# from pathlib import Path
# import json
# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjRmZGE2YjE2LWFjYzItNGVmYS04ZjY5LTE2ZjQwMGJmNzdmMCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiJjODczNzg2OC01Yzc2LTExZjAtYjZiNi1iYWNmNGFlNzk3ODYiLCJjbGllbnRJUCI6IjM4LjE2NS4yLjM5IiwiY2l0eSI6IkxvcyBBbmdlbGVzIiwicG9zdGFsQ29kZSI6IjkwMDExIiwiY291bnRyeSI6IlVTIiwiZG1hIjo4MDMsImFjdGl2ZVJlZ2lvbiI6IlVTIiwiZGV2aWNlTGF0IjozNC4wMDk5OTgzMjE1MzMyLCJkZXZpY2VMb24iOi0xMTguMjYwMDAyMTM2MjMwNDcsInByZWZlcnJlZExhbmd1YWdlIjoiemgiLCJkZXZpY2VUeXBlIjoid2ViIiwiZGV2aWNlVmVyc2lvbiI6IjEzOC4wLjAiLCJkZXZpY2VNYWtlIjoiY2hyb21lIiwiZGV2aWNlTW9kZWwiOiJ3ZWIiLCJhcHBOYW1lIjoid2ViIiwiYXBwVmVyc2lvbiI6IjkuMTQuMS1jYTYwOThiYjVkMWYyZGI2OGMyY2NjY2Y2MDgzNDZmMjE2NTFmMDAzIiwiY2xpZW50SUQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJjbUF1ZGllbmNlSUQiOiIiLCJpc0NsaWVudEROVCI6ZmFsc2UsInVzZXJJRCI6IjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsInVzZXJCcmFuZCI6InBsdXRvdHYiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzZXJ2ZXJTaWRlQWRzIjpmYWxzZSwiZTJlQmVhY29ucyI6ZmFsc2UsImZlYXR1cmVzIjp7ImFkTG9hZCI6eyJjb2hvcnQiOiIifSwibXVsdGlBdWRpbyI6eyJlbmFibGVkIjp0cnVlfSwibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX0sInNlYXJjaEFQSSI6eyJtYXRjaEV4YWN0SW5QaHJhc2VFbmFibGVkIjp0cnVlLCJtYXRjaEluQWN0b3JzQm9vc3QiOjI1LCJtYXRjaEluQWN0b3JzRWRpdERpc3RhbmNlIjoiQVVUTzo1LDExIiwibWF0Y2hJbkFjdG9yc0VuYWJsZWQiOnRydWUsIm1hdGNoSW5EaXJlY3RvcnNCb29zdCI6MjUsIm1hdGNoSW5EaXJlY3RvcnNFZGl0RGlzdGFuY2UiOiJBVVRPOjUsMTEiLCJtYXRjaEluRGlyZWN0b3JzRW5hYmxlZCI6dHJ1ZSwibmV4dXNUaW1lb3V0TXMiOjUwMCwicXVlcnlTeW5vbnltc0VuYWJsZWQiOnRydWUsInF1ZXJ5VmVyc2lvbiI6Imh5YnJpZCIsInNlYXJjaFByb3h5RW5oYW5jZW1lbnQiOmZhbHNlLCJ0aXRsZUF2YWlsYWJpbGl0eURldGVybWluYXRpb24iOmZhbHNlfX0sImVudGl0bGVtZW50cyI6WyJSZWdpc3RlcmVkIl0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiZmY4ZjIwOGU0NDRlMWJkZWNiODk4YWIxMThmMzMyNzFkNTEyNjgzMmQ2ZThkNTQ5MTI1M2VmODUyM2E1Mzc5YiIsImZ3VmNJRDJDb3BwYSI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImN1c3RvbVBhcmFtcyI6eyJmbXNfbGl2ZXJhbXBfaWRsIjoiIiwiZm1zX2VtYWlsaGFzaCI6ImZmOGYyMDhlNDQ0ZTFiZGVjYjg5OGFiMTE4ZjMzMjcxZDUxMjY4MzJkNmU4ZDU0OTEyNTNlZjg1MjNhNTM3OWIiLCJmbXNfc3Vic2NyaWJlcmlkIjoiNjg2NDlhMzlkZTYxZWZjM2E0MmU3OGIzIiwiZm1zX2lmYSI6IiIsImZtc19pZGZ2IjoiIiwiZm1zX3VzZXJpZCI6IjJjMjJiYjdjLWYzNTMtNDE2MS1iOTlhLWRiZmM0YWQ0OGM0MCIsImZtc192Y2lkMnR5cGUiOiJlbWFpbGhhc2giLCJmbXNfcmFtcF9pZCI6IiIsImZtc19oaF9yYW1wX2lkIjoiIiwiZm1zX2JpZGlkdHlwZSI6IjEwNDAsMTA1MCwxMDMwLDEwMTAsMTA3MCwxMDgwIiwiX2Z3XzNQX1VJRCI6IklETDpBbUJaNllwTEZoVVNJa0F0R2t3S21SbnVwWldOQnZVelhIVjJPeUNHSlZGOXdFcHlxSmN2WDRQay02UDQxamthOW1oREZ0M2Vienk1eXFZaGFHZEo5Q21OZG00b0xVUWlSN2QyRldCN2tYYmZvRmlFRHFkR2hpdlhzWWZYNDFfXy0yVDRLd0tobWJCV2o4T3JNMlRfVXJ4TTNpVkhaUGNBMXNQMm1WZi02Vlh4RnU2NVZpeWx2NmUyT0NEdDgxR0xPQU1YbnZWUixQQUlSSUQ6QTNhRFVDeG8vOVRiZXZ1ZU9Cc1BhRis2eGxvL0ROemZrMUdSWUdnK3lvaFUsY29ubmVjdGlkOlY4amdOekNTWEhFbDNJNlZRRXRLOXpjMjA4LXRYem8tWFE3VlVFWkYtTWpmekJmNXI2aDk3cWRra1YwWDV3Vi1wbURZd2dmcWZPQU5yQ0xkenBINFVnLFVJRDI6QTRBQUFCS3JGQ01lcnEwaElFZ0M1NENMc3ZXUVRabEFOTm12QWUweGlVblBaX055OWdCOWRqb3dab3JETkZjbzJfdkRsV3BvRXJfbTU0Q19zemh2RFVKbzNpblR1X285ZHg5ODdUOFJfVzI5bnVhY1RYVG5IT20xSXBLZkJSNFBLQ3hMWUM2S25JT0dZa1pkTjFrcm1TazY3VHRXcWU2WHExRlY1Qm9sSXVueDJqOXUxclRwWHNHWm5TYkVpMFVOMFJyQXlHa0lSM1QySjNvMG1jeEhDMUViR0EsVklBTlRQOmIwZGFkNjc3NGViZGJkYTRhYWNmNmM1NzJkYWJmZDZmMTA4ZDFlZDMxZjYxMzk2NWQ1MDlhMWI3YzQ2ZTExNDksVElOVUlUSTo5YzM3ZWJhYjU4MDBiMTJkMTQ5MTAyMThkMWUwZDhiZTQyYWY2MjJlYWJhM2YyYzQzZGIxMDM5NDU5OTUyYjAwIiwiZm1zX3J1bGVpZCI6IjEwMDAwIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJhZFBvZFBhcmFtcyI6eyJhZ2UiOjIsImdlbmRlciI6MH0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6VVM6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3OjY4NjQ5YTM5ZGU2MWVmYzNhNDJlNzhiMyIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3NTIxMTkwMjYsImlhdCI6MTc1MjAzMjYyNiwianRpIjoiZTRkODI4ZDgtZjZiZi00OTk3LTk1Y2QtZmFmZWYzZDcxNDI3In0.IG9e2UzSs3ftiXvm33DI3STcWUUDnaSrFbco7HzMT6c',
#     'cache-control': 'no-cache',
#     'origin': 'https://pluto.tv',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://pluto.tv/',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
# }

# params = {
#     'start': '2025-07-09T03:30:00.000Z',
#     'channelIds': '561d7d484dc7c8770484914a',
#     'duration': '1440',
#     # 'limit': '1000',
# }
# path = Path(__file__).parent

# response = requests.get('https://service-channels.clusters.pluto.tv/v2/guide/timelines', params=params, headers=headers)
# print(response.json())
# print(response.json().get('data')[0].get('timelines'))
# with open(path / 'timelines.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(response.json()))


import requests

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjhlMTE5ZmMyLTY5MjQtNGVkMy1iMjQxLTlmYTBiMTAzMzM1OCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI3ZTkxNDQ1NS01ZDUzLTExZjAtYmQ5OS1iNjYwMDUzMWMzMGYiLCJjbGllbnRJUCI6IjE1NC4yMDUuMTU2LjUxIiwiY2l0eSI6IlNhbyBQYXVsbyIsInBvc3RhbENvZGUiOiIwMTEwMS0wODAiLCJjb3VudHJ5IjoiQlIiLCJkbWEiOjc2MDA5LCJhY3RpdmVSZWdpb24iOiJCUiIsImRldmljZUxhdCI6LTIzLjUyMDAwMDQ1Nzc2MzY3MiwiZGV2aWNlTG9uIjotNDYuNjMwMDAxMDY4MTE1MjM0LCJwcmVmZXJyZWRMYW5ndWFnZSI6InpoIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMzguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjE0LjEtY2E2MDk4YmI1ZDFmMmRiNjhjMmNjY2NmNjA4MzQ2ZjIxNjUxZjAwMyIsImNsaWVudElEIjoiMmMyMmJiN2MtZjM1My00MTYxLWI5OWEtZGJmYzRhZDQ4YzQwIiwiY21BdWRpZW5jZUlEIjoiIiwiaXNDbGllbnRETlQiOmZhbHNlLCJ1c2VySUQiOiIiLCJsb2dMZXZlbCI6IkRFRkFVTFQiLCJ0aW1lWm9uZSI6IkFtZXJpY2EvU2FvX1BhdWxvIiwic2VydmVyU2lkZUFkcyI6ZmFsc2UsImUyZUJlYWNvbnMiOmZhbHNlLCJmZWF0dXJlcyI6eyJtdWx0aVBvZEFkcyI6eyJlbmFibGVkIjp0cnVlfX0sImZtc1BhcmFtcyI6eyJmd1ZjSUQyIjoiMmMyMmJiN2MtZjM1My00MTYxLWI5OWEtZGJmYzRhZDQ4YzQwIiwiZndWY0lEMkNvcHBhIjoiMmMyMmJiN2MtZjM1My00MTYxLWI5OWEtZGJmYzRhZDQ4YzQwIiwiY3VzdG9tUGFyYW1zIjp7ImZtc19saXZlcmFtcF9pZGwiOiIiLCJmbXNfZW1haWxoYXNoIjoiIiwiZm1zX3N1YnNjcmliZXJpZCI6IiIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJmbXNfdmNpZDJ0eXBlIjoidXNlcmlkIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDE0LDEwMDE2LDEwMDIwLDEwMDIxLDEwMDIyLDEwMDAwLDEwMDA5LDEwMDEzIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJpc3MiOiJib290LnBsdXRvLnR2Iiwic3ViIjoicHJpOnYxOnBsdXRvOmRldmljZXM6QlI6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3IiwiYXVkIjoiKi5wbHV0by50diIsImV4cCI6MTc1MjIxMzc2MywiaWF0IjoxNzUyMTI3MzYzLCJqdGkiOiJiOGM1MzFkMC1jMzVlLTQzMTktOGM4ZS1hNGI5MWM0MWYyNGEifQ.7-1kf3G5PnyHrPjLCgRtAAwM-anLknGEevMc5T2a788',
    'cache-control': 'no-cache',
    'origin': 'https://pluto.tv',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pluto.tv/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-id-token': 'eyJhbGciOiJIUzI1NiIsImtpZCI6Ijc4NGQwZDAxLWRiNzktNDE2ZC1hZTBkLTRhN2E5N2E0OTZmNyIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2ODZlMjQyNzg2YjZhMjcyNjY4ODAzMmYiLCJlbWFpbEhhc2giOiI5ZTdmN2IyYWE0ODBhZjU5NTA3NTZkNGRmNGE3MjA5OWFmMTk0MWVhMWI3NDJkY2VkNGE2ZWRkM2RlY2U4NzFhIiwiYWdlIjoyLCJnZW5kZXIiOjAsImJyYW5kIjoicGx1dG90diIsIm9yaWdpbmF0aW5nU291cmNlIjoicGx1dG8iLCJpc3MiOiJzZXJ2aWNlLXVzZXJzLmNsdXN0ZXJzLnBsdXRvLnR2IiwiYXVkIjoiKi5wbHV0by50diIsImV4cCI6MTc1MjIxMzc2NywiaWF0IjoxNzUyMTI3MzY3LCJqdGkiOiI1NjQyYjg0Mi1kNzMzLTQ2OWQtODBmZS0yM2FmODEyMjg1NjgifQ.H_wX2-d3hZVgV1sesEiad_-gcaImhFDzn69we13YHbU',
}

params = {
    'constraints': '',
}

response = requests.get('https://boot.pluto.tv/v4/refresh', params=params, headers=headers)
print(response.json())

# import requests
# from pathlib import Path
# import json
# headers = {
#     'accept': '*/*',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
#     'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IjhlMTE5ZmMyLTY5MjQtNGVkMy1iMjQxLTlmYTBiMTAzMzM1OCIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uSUQiOiI3ZTkxNDQ1NS01ZDUzLTExZjAtYmQ5OS1iNjYwMDUzMWMzMGYiLCJjbGllbnRJUCI6IjE1NC4yMDUuMTU2LjUxIiwiY2l0eSI6IlNhbyBQYXVsbyIsInBvc3RhbENvZGUiOiIwMTEwMS0wODAiLCJjb3VudHJ5IjoiQlIiLCJkbWEiOjc2MDA5LCJhY3RpdmVSZWdpb24iOiJCUiIsImRldmljZUxhdCI6LTIzLjUyMDAwMDQ1Nzc2MzY3MiwiZGV2aWNlTG9uIjotNDYuNjMwMDAxMDY4MTE1MjM0LCJwcmVmZXJyZWRMYW5ndWFnZSI6InpoIiwiZGV2aWNlVHlwZSI6IndlYiIsImRldmljZVZlcnNpb24iOiIxMzguMC4wIiwiZGV2aWNlTWFrZSI6ImNocm9tZSIsImRldmljZU1vZGVsIjoid2ViIiwiYXBwTmFtZSI6IndlYiIsImFwcFZlcnNpb24iOiI5LjE0LjEtY2E2MDk4YmI1ZDFmMmRiNjhjMmNjY2NmNjA4MzQ2ZjIxNjUxZjAwMyIsImNsaWVudElEIjoiMmMyMmJiN2MtZjM1My00MTYxLWI5OWEtZGJmYzRhZDQ4YzQwIiwiY21BdWRpZW5jZUlEIjoiIiwiaXNDbGllbnRETlQiOmZhbHNlLCJ1c2VySUQiOiI2ODZlMjQyNzg2YjZhMjcyNjY4ODAzMmYiLCJ1c2VyQnJhbmQiOiJwbHV0b3R2IiwibG9nTGV2ZWwiOiJERUZBVUxUIiwidGltZVpvbmUiOiJBbWVyaWNhL1Nhb19QYXVsbyIsInNlcnZlclNpZGVBZHMiOmZhbHNlLCJlMmVCZWFjb25zIjpmYWxzZSwiZmVhdHVyZXMiOnsibXVsdGlQb2RBZHMiOnsiZW5hYmxlZCI6dHJ1ZX19LCJlbnRpdGxlbWVudHMiOlsiUmVnaXN0ZXJlZCJdLCJmbXNQYXJhbXMiOnsiZndWY0lEMiI6IjllN2Y3YjJhYTQ4MGFmNTk1MDc1NmQ0ZGY0YTcyMDk5YWYxOTQxZWExYjc0MmRjZWQ0YTZlZGQzZGVjZTg3MWEiLCJmd1ZjSUQyQ29wcGEiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJjdXN0b21QYXJhbXMiOnsiZm1zX2xpdmVyYW1wX2lkbCI6IiIsImZtc19lbWFpbGhhc2giOiI5ZTdmN2IyYWE0ODBhZjU5NTA3NTZkNGRmNGE3MjA5OWFmMTk0MWVhMWI3NDJkY2VkNGE2ZWRkM2RlY2U4NzFhIiwiZm1zX3N1YnNjcmliZXJpZCI6IjY4NmUyNDI3ODZiNmEyNzI2Njg4MDMyZiIsImZtc19pZmEiOiIiLCJmbXNfaWRmdiI6IiIsImZtc191c2VyaWQiOiIyYzIyYmI3Yy1mMzUzLTQxNjEtYjk5YS1kYmZjNGFkNDhjNDAiLCJmbXNfdmNpZDJ0eXBlIjoiZW1haWxoYXNoIiwiZm1zX3JhbXBfaWQiOiIiLCJmbXNfaGhfcmFtcF9pZCI6IiIsImZtc19iaWRpZHR5cGUiOiIiLCJfZndfM1BfVUlEIjoiIiwiZm1zX3J1bGVpZCI6IjEwMDIyLDEwMDAwLDEwMDEzLDEwMDE0LDEwMDE2LDEwMDIwLDEwMDIxIn19LCJkcm0iOnsibmFtZSI6IndpZGV2aW5lIiwibGV2ZWwiOiJMMyJ9LCJhZFBvZFBhcmFtcyI6eyJhZ2UiOjIsImdlbmRlciI6MH0sImlzcyI6ImJvb3QucGx1dG8udHYiLCJzdWIiOiJwcmk6djE6cGx1dG86dXNlcnMtdjE6QlI6TW1NeU1tSmlOMk10WmpNMU15MDBNVFl4TFdJNU9XRXRaR0ptWXpSaFpEUTRZelF3OjY4NmUyNDI3ODZiNmEyNzI2Njg4MDMyZiIsImF1ZCI6IioucGx1dG8udHYiLCJleHAiOjE3NTIyMTM3NzEsImlhdCI6MTc1MjEyNzM3MSwianRpIjoiN2FmYjk2YWItNDhiOC00MzJmLWIwZjUtNDE1YWRhY2FlOWQ5In0.C2e3pPzcsDc5_AXDq1KHo8k1Iheqn_EwdW_dBwz-fHc',
#     'cache-control': 'no-cache',
#     'origin': 'https://pluto.tv',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://pluto.tv/',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
# }

# response = requests.get('https://service-channels.clusters.pluto.tv/v2/guide/categories', headers=headers)
# with open(Path(__file__).parent / 'categories.json', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(response.json()))
# data = response.json().get('data')
# a = []
# for i in data:
#     for j in i.get('channelIDs'):
#         a.append(j)
# print(len(a))
# print(len(set(a)))