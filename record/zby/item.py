import requests
import parsel
import re
import json
from pathlib import Path

def get_url_live(channel_link):
    cookies = {
        '_gcl_au': '1.1.187042639.1752831152',
        'G_ENABLED_IDPS': 'google',
        'afUserId': 'abbb993f-00a9-4dac-87bb-9740ff622689-p',
        'AF_SYNC': '1752831213369',
        '_fbp': 'fb.1.1752831329367.509982846733869306',
        'mm': 'wv',
        '_gid': 'GA1.2.1424046564.1753176361',
        '__gpi': 'UID=000010ecc657e75a:T=1753179127:RT=1753179673:S=ALNI_Mb1wBSzONhpkPMRq1VMTU77Qvt4Kw',
        '__eoi': 'ID=cc8116846165a601:T=1753179127:RT=1753179673:S=AA-Afjbvy2LwqZ1xhFkm3lPw9zO0',
        'TiPMix': '41.74665559438737',
        'x-ms-routing-name': 'self',
        '.AspNetCore.Antiforgery.RtGCWVXC8-4': 'CfDJ8O69TXDWjUBDmMQ3RazeVOxeuOFM9KqJwr9CeG7uw1u0C7RsqntptG58qaOnuo0AgWBRZMCYB1g4w2I_zlLmLfYen37dxAywcGCTUMTF4w0RS8DqxfwAJYSqLMSMYHBe7JysTtIh28mmuph5RFAA2-o',
        '_ga_XHNLH4V0GQ': 'GS2.1.s1753236598$o5$g1$t1753238427$j60$l0$h0',
        '_X_PLAYPLUS': 'EncUserID%3D5B9578621722A05DEC70746EA3FD6309%26PlanID%3D-1%26Login.FirstName%3Dblack%20cat%26FullName%3Dblack%20cat%20%26Email%3Dwnhmsy%40gmail.com%26UserToken%3DD9F8CAF720F369D1E475E46EA1CB2FFC65A3BB5EBBC4FF6A57E8700D214A64DB75C35E59576E394E98172EB5BA2CEED6BBE89B4BA3507A1A4EADB7F78E16BF5722426897803BEC546F1F905D175BE5D72ABF2816C1C29E2A96EC071C763F052E%26CurrentCulture%3Dzh-CN%26ProfileId%3Db01aae7e-e23f-415f-a71b-dba33b1bebc2%26ProfileName%3DYmxhY2sgY2F0%26ProfileImage%3D%26AgeRatingId%3D8%26IsKids%3DFalse',
        '_X_PLAYPLUSTOKEN': 'ValidationToken%3D9588A5E5596EC17C4613A75B1D5BAF9D336138E9B769CDE31DCD19C69DA4C610',
        '_ga': 'GA1.2.1539446295.1752831152',
        '_gat': '1',
        '__gads': 'ID=774c5cb7057f8d30:T=1752836513:RT=1753238769:S=ALNI_MY3bqErtNvPCa_I5pyrMUUHYoeASA',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.playplus.com/live',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'groupId': '10',
    }

    try:
        response = requests.get(channel_link, params=params, cookies=cookies, headers=headers)
        response.raise_for_status()
        url_live = re.search(r"urlLive = '(.*?)';", response.text)
        if url_live:
            return url_live.group(1)
    except requests.exceptions.RequestException as e:
        print(f"请求 {channel_link} 时出错: {e}")
    except Exception as e:
        print(f"处理 {channel_link} 时发生未知错误: {e}")
    return None

if __name__ == "__main__":
    path = Path(__file__).parent
    try:
        with open(path / 'living.json', 'r', encoding='utf-8') as f:
            channels = json.load(f)
    except FileNotFoundError:
        print("错误: living.json 文件未找到.")
        exit()
    except json.JSONDecodeError:
        print("错误: living.json 文件格式不正确.")
        exit()

    for channel in channels:
        link = channel.get('link')
        if link:
            print(f"正在为频道 '{channel.get('name')}' 获取 urlLive...")
            url_live = get_url_live(link)
            if url_live:
                channel['urlLive'] = url_live
                print(f"  > 成功获取 urlLive.")
            else:
                print(f"  > 未能获取 urlLive.")

    try:
        with open(path / 'living.json', 'w', encoding='utf-8') as f:
            json.dump(channels, f, indent=4, ensure_ascii=False)
        print("\n已成功更新 living.json 文件.")
    except IOError as e:
        print(f"写入 living.json 文件时出错: {e}")