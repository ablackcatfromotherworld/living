import requests
import execjs
import hashlib
import parsel
from pathlib import Path
import re
import json5
import json
import uuid
import datetime

# sha256_hash = hashlib.sha256()
# sha256_hash.update('123456'.encode('utf-8'))

# hex_digest = sha256_hash.hexdigest()
# print(type(hex_digest))
# print(len(hex_digest))
# print(hex_digest)

import requests

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
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
}

data = {
    'grant_type': 'authorization_code',
    'code': 'ory_ac_AR51KSHv3VKwcS9xCgCH7cK_hZegZzapDrtTX0n9vVk.3q6YjVeCqJZ6LSdmM1EM8vVRtF41ETooLCUfPf0K_QY',
    'client_id': 'globoplay-web@globoid-connect',
    'redirect_uri': 'https://globoplay.globo.com/callback.html',
    'code_verifier': '6ClCCUO8r6gryhSFF5XRDcuzMKHM3gHw15ojzPbfYnmO1M96hOnLkspDNcp9YqhNsgFsyqBTrhQb9HxeGsYA33an9AVyozd0',
}

response = requests.post(
    'https://goidc.globo.com/auth/realms/globo.com/protocol/openid-connect/token',
    headers=headers,
    data=data,
)
print(response.text)