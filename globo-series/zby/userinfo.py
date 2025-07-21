import requests
import execjs
import parsel
from pathlib import Path
import re
import json5
import json
import uuid
import base64

token1 = {"alg":"RS256","kid":str(uuid.uuid4()),"typ":"JWT"}
token2 = {"aud":["globoplay-web@globoid-connect"],"azp":"globoplay-web@globoid-connect","email":"wnhmsy@gmail.com","exp":1752821340,"federated_sid":"17f2f046e16a2e1d213d2e4d16660be7f70744c416361734431614952625272305361727732337872586450734846324c4552484e553035666857667436597a69506c432d63586a4e6f614e385947333864386e785f41505043783347493035426e5741574a513d3d3a303a75346f6b366d6b6e30663362316a717031723334","fs_id":"ptLAcasD1aIRbRr0Sarw23xrXdPsHF2LERHNU05fhWft6YziPlC-cXjNoaN8YG38d8nx_APPCx3GI05BnWAWJQ==","glbid":"17f2f046e16a2e1d213d2e4d16660be7f70744c416361734431614952625272305361727732337872586450734846324c4552484e553035666857667436597a69506c432d63586a4e6f614e385947333864386e785f41505043783347493035426e5741574a513d3d3a303a75346f6b366d6b6e30663362316a717031723334","globo_id":"055dbff8-ec7b-4db8-b688-4a3fa26efe0a","iat":1752817735,"iss":"https://goidc.globo.com/auth/realms/globo.com","jti":"9eeeb603-7b2d-44fd-a5a4-f0f83985505a","nonce":"a4db764d-5455-4649-8c84-22e94067d993","preferred_username":"u4ok6mkn0f3b1jqp1r34","scp":["openid","profile-globoplay"],"session_state":"7b35bda0-6a56-45bb-9a9a-1e3b261b5487","sid":"7b35bda0-6a56-45bb-9a9a-1e3b261b5487","sub":"055dbff8-ec7b-4db8-b688-4a3fa26efe0a","typ":"Bearer"}
token3 = (base64.b64encode(json.dumps(token1).encode('utf-8')).decode('utf-8') + '.' + base64.b64encode(json.dumps(token2).encode('utf-8')).decode('utf-8')).replace('=','')
headers = {
     'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg5NWIwYmIwLTI4ODMtNDE3MC1hMDY2LTZkMDIwZjkzNGRlMyIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZ2xvYm9wbGF5LXdlYkBnbG9ib2lkLWNvbm5lY3QiXSwiYXpwIjoiZ2xvYm9wbGF5LXdlYkBnbG9ib2lkLWNvbm5lY3QiLCJlbWFpbCI6InduaG1zeUBnbWFpbC5jb20iLCJleHAiOjE3NTI4MjY3MzAsImZlZGVyYXRlZF9zaWQiOiIxN2YyZjA0NmUxNmEyZTFkMjEzZDJlNGQxNjY2MGJlN2Y3MDc0NGM0MTYzNjE3MzQ0MzE2MTQ5NTI2MjUyNzIzMDUzNjE3Mjc3MzIzMzc4NzI1ODY0NTA3MzQ4NDYzMjRjNDU1MjQ4NGU1NTMwMzU2NjY4NTc2Njc0MzY1OTdhNjk1MDZjNDMyZDYzNTg2YTRlNmY2MTRlMzg1OTQ3MzMzODY0Mzg2ZTc4NWY0MTUwNTA0Mzc4MzM0NzQ5MzAzNTQyNmU1NzQxNTc0YTUxM2QzZDNhMzAzYTc1MzQ2ZjZiMzY2ZDZiNmUzMDY2MzM2MjMxNmE3MTcwMzE3MjMzMzQiLCJmc19pZCI6InB0TEFjYXNEMWFJUmJScjBTYXJ3MjN4clhkUHNIRjJMRVJITlUwNWZoV2Z0Nll6aVBsQy1jWGpOb2FOOFlHMzhkOG54X0FQUEN4M0dJMDVCbldBV0pRPT0iLCJnbGJpZCI6IjE3ZjJmMDQ2ZTE2YTJlMWQyMTNkMmU0ZDE2NjYwYmU3ZjcwNzQ0YzQxNjM2MTczNDQzMTYxNDk1MjYyNTI3MjMwNTM2MTcyNzczMjMzNzg3MjU4NjQ1MDczNDg0NjMyNGM0NTUyNDg0ZTU1MzAzNTY2Njg1NzY2NzQzNjU5N2E2OTUwNmM0MzJkNjM1ODZhNGU2ZjYxNGUzODU5NDczMzM4NjQzODZlNzg1ZjQxNTA1MDQzNzgzMzQ3NDkzMDM1NDI2ZTU3NDE1NzRhNTEzZDNkM2EzMDNhNzUzNDZmNmIzNjZkNmI2ZTMwNjYzMzYyMzE2YTcxNzAzMTcyMzMzNCIsImdsb2JvX2lkIjoiMDU1ZGJmZjgtZWM3Yi00ZGI4LWI2ODgtNGEzZmEyNmVmZTBhIiwiaWF0IjoxNzUyODIzMTI3LCJpc3MiOiJodHRwczovL2dvaWRjLmdsb2JvLmNvbS9hdXRoL3JlYWxtcy9nbG9iby5jb20iLCJqdGkiOiI5NzY5NjQ0Yi1kZmJiLTQxNDktOGJhOS05OWZlMjk1ZjMwYmEiLCJub25jZSI6ImRiNTYxMTFjLTkxMzItNDgxZS04YWQwLWI0ZmQxY2E5ODAxNCIsInByZWZlcnJlZF91c2VybmFtZSI6InU0b2s2bWtuMGYzYjFqcXAxcjM0Iiwic2NwIjpbIm9wZW5pZCIsInByb2ZpbGUtZ2xvYm9wbGF5Il0sInNlc3Npb25fc3RhdGUiOiI3YjM1YmRhMC02YTU2LTQ1YmItOWE5YS0xZTNiMjYxYjU0ODciLCJzaWQiOiI3YjM1YmRhMC02YTU2LTQ1YmItOWE5YS0xZTNiMjYxYjU0ODciLCJzdWIiOiIwNTVkYmZmOC1lYzdiLTRkYjgtYjY4OC00YTNmYTI2ZWZlMGEiLCJ0eXAiOiJCZWFyZXIifQ.Ha-6wUgHLqNxi519N_wI_s9y7SdZK6dHfRUmQFlzCfHQKaH8JHdqh5pI8IO6YGod6xbmi2teB3YwsM3uwOq1iWy5BrI9NV8Ln51vtukB4qAuMgwiL3ZAtX_p8S12JADevClipngARNPl3OJFKmRYyxoseyOsiNk6E6RQd6Snef837pk4a-FafjJCop2uBWJxjOTlmux1oUewJivyh5ZaNw95lJLRdXd98HGIb1Nz2YTdGJyP9uFEwo8xA8giAur2zTULrZ0Om4bIP_sXK-VpbYJWdvV8N2d5WAdB52F5_O_UN7v_vd2IIy2ukXPT3psTn_X23bQWYAoixyh8VmF6Wg',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

userinfo = requests.post(
    'https://goidc.globo.com/auth/realms/globo.com/protocol/openid-connect/userinfo',
    headers=headers,
).json()

path = Path(__file__).parent

with open(path/'userinfo.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(userinfo))
