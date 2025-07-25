import requests
import parsel
import json
from pathlib import Path
def fetch_live_channels():
    """
    Fetches and prints live channel information from playplus.com.
    """
    cookies = {
        '_gcl_au': '1.1.187042639.1752831152',
        'G_ENABLED_IDPS': 'google',
        'afUserId': 'abbb993f-00a9-4dac-87bb-9740ff622689-p',
        'AF_SYNC': '1752831213369',
        '_fbp': 'fb.1.1752831329367.509982846733869306',
        'mm': 'wv',
        '_gid': 'GA1.2.1424046564.1753176361',
        '__gads': 'ID=774c5cb7057f8d30:T=1752836513:RT=1753179673:S=ALNI_MY3bqErtNvPCa_I5pyrMUUHYoeASA',
        '__gpi': 'UID=000010ecc657e75a:T=1753179127:RT=1753179673:S=ALNI_Mb1wBSzONhpkPMRq1VMTU77Qvt4Kw',
        '__eoi': 'ID=cc8116846165a601:T=1753179127:RT=1753179673:S=AA-Afjbvy2LwqZ1xhFkm3lPw9zO0',
        'TiPMix': '41.74665559438737',
        'x-ms-routing-name': 'self',
        '.AspNetCore.Antiforgery.RtGCWVXC8-4': 'CfDJ8O69TXDWjUBDmMQ3RazeVOxeuOFM9KqJwr9CeG7uw1u0C7RsqntptG58qaOnuo0AgWBRZMCYB1g4w2I_zlLmLfYen37dxAywcGCTUMTF4w0RS8DqxfwAJYSqLMSMYHBe7JysTtIh28mmuph5RFAA2-o',
        '_X_PLAYPLUS': 'EncUserID%3D5B9578621722A05DEC70746EA3FD6309%26PlanID%3D-1%26Login.FirstName%3Dblack%20cat%26FullName%3Dblack%20cat%20%26Email%3Dwnhmsy%40gmail.com%26UserToken%3DD9F8CAF720F369D1E475E46EA1CB2FFC65A3BB5EBBC4FF6A57E8700D214A64DB75C35E59576E394E98172EB5BA2CEED6BBE89B4BA3507A1A4EADB7F78E16BF5722426897803BEC546F1F905D175BE5D72ABF2816C1C29E2A96EC071C763F052E%26CurrentCulture%3Dzh-CN%26ProfileId%3Db01aae7e-e23f-415f-a71b-dba33b1bebc2%26ProfileName%3DYmxhY2sgY2F0%26ProfileImage%3D%26AgeRatingId%3D8%26IsKids%3DFalse',
        '_X_PLAYPLUSTOKEN': 'ValidationToken%3D9588A5E5596EC17C4613A75B1D5BAF9D336138E9B769CDE31DCD19C69DA4C610',
        '_ga': 'GA1.1.1539446295.1752831152',
        '_ga_XHNLH4V0GQ': 'GS2.1.s1753236598$o5$g1$t1753236718$j60$l0$h0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,en-GB-oxendict;q=0.5,zh-TW;q=0.4,ja;q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.playplus.com/Live/',
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
    path = Path(__file__).parent
    try:
        response = requests.get('https://www.playplus.com/live', cookies=cookies, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        selector = parsel.Selector(response.text)
        items = selector.xpath('//div[@class="channel-item"]')

        channels = []
        for item in items:
            name = item.xpath('.//p/text()').get()
            slug = item.xpath('./a/@href').get()
            img = item.xpath('.//img/@src').get()

            if name and slug and img:
                channel_data = {
                    'name': name.strip(),
                    'link': f"https://www.playplus.com{slug}",
                    'image': img
                }
                channels.append(channel_data)

        with open(path / 'living.json', 'w', encoding='utf-8') as f:
            json.dump(channels, f, ensure_ascii=False, indent=4)

        print(f"Successfully saved {len(channels)} channels to living.json")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_live_channels()