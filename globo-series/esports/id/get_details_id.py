import requests

headers = {
    'authorization': '139c8bca2815a1c71b11c874f68082c8d51556531524b56614d44416f52455374707246666f793873454e71674d64724c666a4a6f4a7a737375666b49734c706747445a6748473953413634314c636f56584b6559643344505f66794a427761643138504137673d3d3a303a75716f7a75346764773369397535317676656664',
    'referer': 'https://globoplay.globo.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-client-version': '2025.08-7',
    'x-device-id': 'desktop',
    'x-glb-exp-id': 'jra0VrIvHRqinAH_pXpN1yz0GMQpgp9DMK_FgRfdmNw=',
    'x-hsid': '08fb7c2a-ccc7-4219-a2d8-9667fb3fb075',
    'x-platform-id': 'web',
    'x-tenant-id': 'globo-play',
    'x-user-id': '93cc4ec3-958b-41e7-8531-c1c1c320bf39',
}

params = {
    'operationName': 'getEpisodesPlaylist',
    'variables': '{"perPage":24,"titleId":"XY6jnccMv9","page":1}',
    'extensions': '{"persistedQuery":{"version":1,"sha256Hash":"77fbf2cae4a7a8f5a39e33c4d8b37a40b566d7dc3506d3ea876dd7a1dc1d74a4"}}',
}

response = requests.get('https://cloud-jarvis.globo.com/graphql', params=params, headers=headers)
print(response.json())
print(response)