from DrissionPage import Chromium, ChromiumOptions
from DrissionPage.common import Actions
from pathlib import Path
import json

# --- 设置 ---
path = Path(__file__).parent
co = ChromiumOptions().auto_port()
tab = Chromium(co).latest_tab
tab.set.load_mode.normal()
ac = Actions(tab)

# --- 导航到页面 ---
tab.get('https://www.band.com.br/programacao')

# --- 准备工作 ---
# 先打开一次下拉菜单，获取总选项数
ac.move_to('x://h2[@class="filter_selected"]').click()
# 等待下拉菜单加载完成
tab.wait.ele_displayed('x://ul[@class="filter_box"]/li')
options_count = len(tab.eles('x://ul[@class="filter_box"]/li'))
# 点击页面其他地方收起菜单，为循环做准备
ac.move_to('x://h2[@class="filter_selected"]').click()
tab.wait(0.5)

# --- 主循环 ---
data_band = []
# 使用索引进行循环，而不是 for-each
for i in range(options_count):
    # 在每次循环开始时，都重新打开下拉菜单
    ac.move_to('x://h2[@class="filter_selected"]').click()
    tab.wait.ele_displayed('x://ul[@class="filter_box"]/li')  # 等待菜单出现

    # 重新获取最新的选项列表
    options = tab.eles('x://ul[@class="filter_box"]/li')

    # 获取当前选项的名称并点击
    current_option = options[i]
    option_name = current_option.text

    print(f"开始抓取频道: {option_name}")  # 增加日志，方便调试

    ac.move_to(current_option).click()
    tab.wait.ele_displayed('x://ul[@class="bar__days"]/li[@class="active"]')  # 等待日期栏加载

    # --- 抓取该频道下所有日期的数据 ---
    bar_days = tab.eles('x://ul[@class="bar__days"]/li')
    data_options = []
    for bar_day in bar_days:
        data = []
        try:
            ac.move_to(bar_day).click()
            # 等待节目列表刷新，可以等待某个节目项出现
            tab.wait.ele_displayed('x://span[@class="program__item"]')

            date = bar_day.ele('x:./span').text
            program_items = tab.eles('x://span[@class="program__item"]')

            for program_item in program_items:
                time = program_item.ele('x:./span[@class="program__hour"]').text
                # 使用 try-except 避免某个节目没有图片导致报错
                try:
                    img = program_item.ele('x:./span[@class="program__img program__img--small"]/img').attr('src')
                except Exception:
                    img = None  # 如果没有图片，则为 None
                title = program_item.ele('x:./span[@class="program__title"]').text
                data.append({'time': time, 'img': img, 'title': title})
        except Exception as e:
            print(e)

        data_options.append({date: data})

    data_band.append({option_name: data_options})

# --- 保存数据 ---
output_file = path / 'band.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data_band, f, ensure_ascii=False, indent=4)

print(f"数据已成功保存到: {output_file}")