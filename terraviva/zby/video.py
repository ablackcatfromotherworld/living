import requests

import time
import os
import string

# 1. 准备一个用于32进制转换的字符集 (0-9, a-v)
BASE32_ALPHABET = string.digits + string.ascii_lowercase[:22]

def to_base32(n: int) -> str:
    """
    将一个十进制整数转换为32进制字符串。
    这相当于实现了 JavaScript 的 n.toString(32) 功能。
    """
    if n == 0:
        return '0'
    
    base32_str = ""
    while n > 0:
        # 取余数，然后在字符集中找到对应的字符
        remainder = n % 32
        base32_str = BASE32_ALPHABET[remainder] + base32_str
        # 地板除，继续下一次循环
        n //= 32
        
    return base32_str

def generate_view_id() -> str:
    """
    生成一个高度唯一的ID，功能与您提供的JavaScript代码完全相同。
    """
    # =========================================================================
    # Part 1: 生成10位的16进制随机字符串 (对应JavaScript中的变量 o)
    # =========================================================================
    
    # 1. 获取5个密码学安全的随机字节 (等同于 new Uint8Array(5) + getRandomValues)
    random_bytes = os.urandom(5)
    # 此时 random_bytes 类似于 b'\x1f\x8a\x03\xe2\x9b'
    
    # 2. 将字节序列直接转换为16进制字符串 (等同于 Array.from + join)
    #    Python的 .hex() 方法会自动将每个字节转为2位16进制字符，
    #    所以5个字节正好得到10个字符的字符串，无需像JS那样手动补零。
    o = random_bytes.hex()
    # o 的结果会是类似 "1f8a03e29b" 的字符串
    
    # =========================================================================
    # Part 2: 获取32进制的时间戳，并与随机字符串拼接 (对应变量 t)
    # =========================================================================
    
    # 1. 获取当前时间的毫秒时间戳 (等同于 Date.now())
    #    time.time() 返回的是秒，所以需要乘以1000
    now_in_ms = int(time.time() * 1000)
    
    # 2. 将时间戳转换为32进制字符串
    timestamp_part = to_base32(now_in_ms)
    
    # 3. 使用f-string拼接，生成最终的ID (等同于模板字面量)
    t = f"{timestamp_part}{o}"
    
    return t

# =========================================================================
# 模拟JavaScript代码的最后部分
# =========================================================================

# 假设P是一个字典或类的实例，用于存储状态
P = {} 
# 假设e是传入的视频索引
e = 1 

# 调用函数生成ID
view_id = generate_view_id()

# 将值赋给P
P['videoIndex'] = e
P['viewId'] = view_id

# 打印结果查看
print(f"生成的 View ID: {P['viewId']}")
print(f"视频索引 (Video Index): {P['videoIndex']}")
# 可能的输出:
# 生成的 View ID: 1f6bkpsgqco7a9b1c2d3e4
# 视频索引 (Video Index): 1


cookies = {
    'ts': '831292',
    'v1st': '54f212b9-464c-dd60-acd4-3c90ff5c3fc9',
    'dm-gpp-mspa': 'DBABLA~BVQqAAAAAWA',
    'usprivacy': '1YNY',
    'damd': 'XgqDoBKtq05LIX_1iKgfKUugG9NiZVmxqRiXYcPAZ2UmPQSCbopXNWpqyGdietjR5TQQUxtfdmF4jr98SFB2liSEeqOXVLXu1SW5OjzveJXqj_tE_65pZjZPIfrEV6vpQ4eLkGNCZ4N9O_Q8s8DLmtnpXC4Cogc4xBJEQhvH48YuaF8cuAFJhvHqhMe_GDb4etRVQjj08_O-ek3T22eStrLJ2ce6wiHDob-QV9H333SQeMP4itQ6KWnoltZDl7OkuzZhJSeAHBtaF_mZfiQL_smZNWa3f0O127fgTXJ6UeGF6iqHyJnSTlcjR9zdu2lAcQjAtL4Mj0BTx2UizJhiG0da2mjde788kCdLzCErsWndqcHxkjzylK7aGIEYOr_9AVgsMfY4cd26DDn51CYVBw',
    'dmvk': '68871b03b0c44',
    'client_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhaWQiOiJmMWEzNjJkMjg4YzFiOTgwOTljNyIsInJvbCI6ImNhbi1tYW5hZ2UtcGFydG5lcnMtcmVwb3J0cyBjYW4tcmVhZC12aWRlby1zdHJlYW1zIGNhbi1zcG9vZi1jb3VudHJ5IGNhbi1hZG9wdC11c2VycyBjYW4tcmVhZC1jbGFpbS1ydWxlcyBjYW4tbWFuYWdlLWNsYWltLXJ1bGVzIGNhbi1tYW5hZ2UtdXNlci1hbmFseXRpY3MgY2FuLXJlYWQtbXktdmlkZW8tc3RyZWFtcyBjYW4tZG93bmxvYWQtbXktdmlkZW9zIGFjdC1hcyBhbGxzY29wZXMgYWNjb3VudC1jcmVhdG9yIGNhbi1yZWFkLWFwcGxpY2F0aW9ucyIsInNjbyI6Im1hbmFnZV9zdWJzY3JpcHRpb25zIG1hbmFnZV92aWRlb3MgdXNlcmluZm8iLCJsdG8iOiJiV2h3Vmx4OVcyRjZkVDRKWVZvdkMzZ19ZQUFqS3lzTE1Dd2hjdyIsImFpbiI6MSwiYWRnIjoxLCJpYXQiOjE3NTM2ODQ3NzAsImV4cCI6MTc1MzcyMDQ2NiwiZG12IjoiMSIsImF0cCI6ImJyb3dzZXIiLCJhZGEiOiJ3d3cuZGFpbHltb3Rpb24uY29tIiwidmlkIjoiNTRmMjEyYjktNDY0Yy1kZDYwLWFjZDQtM2M5MGZmNWMzZmM5IiwiZnRzIjo4MzEyOTIsImNhZCI6MiwiY3hwIjoyLCJjYXUiOjIsImtpZCI6IkFGODQ5REQ3M0E1ODYzQ0Q3RDk3RDBCQUIwNzIyNDNCIn0.V9QooN0f-CeDUOPNXgeNp36LbKjZP9WGMs6P9WryMBI',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://geo.dailymotion.com/player.html?video=x8qceqq',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'ts=831292; v1st=54f212b9-464c-dd60-acd4-3c90ff5c3fc9; dm-gpp-mspa=DBABLA~BVQqAAAAAWA; usprivacy=1YNY; damd=XgqDoBKtq05LIX_1iKgfKUugG9NiZVmxqRiXYcPAZ2UmPQSCbopXNWpqyGdietjR5TQQUxtfdmF4jr98SFB2liSEeqOXVLXu1SW5OjzveJXqj_tE_65pZjZPIfrEV6vpQ4eLkGNCZ4N9O_Q8s8DLmtnpXC4Cogc4xBJEQhvH48YuaF8cuAFJhvHqhMe_GDb4etRVQjj08_O-ek3T22eStrLJ2ce6wiHDob-QV9H333SQeMP4itQ6KWnoltZDl7OkuzZhJSeAHBtaF_mZfiQL_smZNWa3f0O127fgTXJ6UeGF6iqHyJnSTlcjR9zdu2lAcQjAtL4Mj0BTx2UizJhiG0da2mjde788kCdLzCErsWndqcHxkjzylK7aGIEYOr_9AVgsMfY4cd26DDn51CYVBw; dmvk=68871b03b0c44; client_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhaWQiOiJmMWEzNjJkMjg4YzFiOTgwOTljNyIsInJvbCI6ImNhbi1tYW5hZ2UtcGFydG5lcnMtcmVwb3J0cyBjYW4tcmVhZC12aWRlby1zdHJlYW1zIGNhbi1zcG9vZi1jb3VudHJ5IGNhbi1hZG9wdC11c2VycyBjYW4tcmVhZC1jbGFpbS1ydWxlcyBjYW4tbWFuYWdlLWNsYWltLXJ1bGVzIGNhbi1tYW5hZ2UtdXNlci1hbmFseXRpY3MgY2FuLXJlYWQtbXktdmlkZW8tc3RyZWFtcyBjYW4tZG93bmxvYWQtbXktdmlkZW9zIGFjdC1hcyBhbGxzY29wZXMgYWNjb3VudC1jcmVhdG9yIGNhbi1yZWFkLWFwcGxpY2F0aW9ucyIsInNjbyI6Im1hbmFnZV9zdWJzY3JpcHRpb25zIG1hbmFnZV92aWRlb3MgdXNlcmluZm8iLCJsdG8iOiJiV2h3Vmx4OVcyRjZkVDRKWVZvdkMzZ19ZQUFqS3lzTE1Dd2hjdyIsImFpbiI6MSwiYWRnIjoxLCJpYXQiOjE3NTM2ODQ3NzAsImV4cCI6MTc1MzcyMDQ2NiwiZG12IjoiMSIsImF0cCI6ImJyb3dzZXIiLCJhZGEiOiJ3d3cuZGFpbHltb3Rpb24uY29tIiwidmlkIjoiNTRmMjEyYjktNDY0Yy1kZDYwLWFjZDQtM2M5MGZmNWMzZmM5IiwiZnRzIjo4MzEyOTIsImNhZCI6MiwiY3hwIjoyLCJjYXUiOjIsImtpZCI6IkFGODQ5REQ3M0E1ODYzQ0Q3RDk3RDBCQUIwNzIyNDNCIn0.V9QooN0f-CeDUOPNXgeNp36LbKjZP9WGMs6P9WryMBI',
}

params = {
    'legacy': 'true',
    'embedder': 'https://terraviva.uol.com.br/',
    'geo': '1',
    'player-id': 'default',
    'locale': 'zh',
    'dmV1st': '54f212b9-464c-dd60-acd4-3c90ff5c3fc9',
    'dmTs': '831292',
    'is_native_app': '0',
    'dmViewId': '1j17tfch54c9f215fb1',
    'parallelCalls': '1',
}

response = requests.get('https://geo.dailymotion.com/video/x8qceqq.json', params=params, cookies=cookies, headers=headers)
