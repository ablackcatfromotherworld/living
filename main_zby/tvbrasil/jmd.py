# 获取电视节目表
import requests
from pathlib import Path
import parsel
import json
import datetime

path = Path(__file__).parent
time_now = datetime.datetime.now()
times = [(time_now + datetime.timedelta(days=i)).strftime("%Y%m%d") for i in range(0,8)]
programs = []
for i in times:
    url = f"https://tvbrasil.ebc.com.br/programacao/{i}/2"
    response = requests.get(url).text
    selector = parsel.Selector(response)
    broadcast_times = selector.xpath('//span[@class="date-display-single"]/text()').getall()
    # broadcast_nodes = selector.xpath('//span[@class="date-display-single"]')
    # program_nodes = []
    # for broadcast_node in broadcast_nodes:
    #     program_node = broadcast_node.xpath('../following-sibling::div[1]')
    #     program_nodes.append(program_node)
    program_names = selector.xpath('//div[@class="col-lg-11 col-md-11 col-sm-10 col-xs-9 nomeprograma"]')
    program_names = [text.strip() if text else '' for p in program_names if (text := p.xpath('./a/text()').get()) or text is None]
    # print(len(broadcast_times), len(program_names))
    data = {key.strip(): value.strip() for key, value in zip(broadcast_times, program_names)}
    programs.append({i:data})
# lis = selector.xpath("//ul[@class="programacao-datas"]/li")
# for li in lis:

with open(path / 'tvbrasil.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(programs))
# with open(path / 'tvbrasil.html', 'w', encoding='utf-8') as f:
#     f.write(response)


