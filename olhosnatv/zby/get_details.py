import parsel 
import requests
from get_category import GetCategory
import re
import json 
from pathlib import Path 

class GetDetails:
    def __init__(self, url):
        self.url = url
        self.params = {
            "max-results": "10000",
            "start": "0",
        }
        self.response = requests.get(self.url,params=self.params)
    
    def get_details(self):
        return self.response.text
    
    def get_details_list(self):
        details_list = parsel.Selector(self.get_details()).xpath('//h3[@class="post-title entry-title"]/a/@href').getall()
        return details_list


if __name__ == "__main__":
    url_list = GetCategory().get_category_list()
    total = []
    for url in url_list:
        try:
            get_details = GetDetails(url)
            details_list = get_details.get_details_list()
            total.extend(details_list)
        except:
            print(url)
    j = 0
    m3u8_urls = []
    for i,url in enumerate(total):
        try:
           selector = parsel.Selector(requests.get(url).text)
           m3u8_url = re.search("hls.loadSource\('(.*?)'\);",requests.get(url).text).group(1)
           m3u8_urls.append(m3u8_url)
           print(f"成功获取到第{i}个视频的m3u8地址为：{m3u8_url}")
           j += 1
        except:
            print(f"第{i}个视频获取m3u8地址失败")
    path = Path(__file__).parent
    with open(path / 'm3u8_urls.json', 'w') as f:
        json.dump(m3u8_urls,f)
    print(f"成功获取到{j}个视频的m3u8地址")
