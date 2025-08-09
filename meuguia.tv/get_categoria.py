import requests
import parsel
from pathlib import Path
import json
import time

def get_categories():
    """
    获取meuguia.tv网站的分类页面链接
    返回格式: {name: url}
    """
    base_url = 'https://meuguia.tv'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        
        selector = parsel.Selector(response.text)
        
        # 获取分类链接和名称
        category_links = selector.xpath('//ul//a/@href').getall()
        category_names = selector.xpath('//ul//a//h2/text()').getall()
        
        # 构建结果字典
        categories = {}
        
        for i, (name, link) in enumerate(zip(category_names, category_links)):
            # 拼接完整URL
            if link.startswith('/'):
                full_url = base_url + link
            else:
                full_url = base_url + '/' + link
            
            categories[name.strip()] = full_url
        
        return categories
        
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return {}
    except Exception as e:
        print(f"解析失败: {e}")
        return {}

def get_channels_from_category(category_url):
    """
    从分类页面获取频道信息
    返回格式: {name: url}
    """
    base_url = 'https://meuguia.tv'
    
    try:
        response = requests.get(category_url)
        response.raise_for_status()
        
        selector = parsel.Selector(response.text)
        
        # 使用新的xpath语法获取频道链接和名称
        channel_links = selector.xpath('//ul/li/a/@href').getall()
        channel_names = selector.xpath('//ul/li//h2/text()').getall()
        
        # 构建结果字典
        channels = {}
        
        for name, link in zip(channel_names, channel_links):
            # 拼接完整URL
            if link.startswith('/'):
                full_url = base_url + link
            else:
                full_url = base_url + '/' + link
            
            channels[name.strip()] = full_url
        
        return channels
        
    except requests.RequestException as e:
        print(f"请求分类页面失败 {category_url}: {e}")
        return {}
    except Exception as e:
        print(f"解析分类页面失败 {category_url}: {e}")
        return {}

def get_all_channels():
    """
    获取所有分类页面的频道信息
    返回格式: {name: url}
    """
    # 先获取所有分类页面
    categories = get_categories()
    
    if not categories:
        print("未获取到分类页面")
        return {}
    
    print(f"获取到 {len(categories)} 个分类页面")
    
    all_channels = {}
    
    # 遍历每个分类页面
    for category_name, category_url in categories.items():
        print(f"正在处理分类: {category_name}")
        
        # 获取该分类下的所有频道
        channels = get_channels_from_category(category_url)
        
        if channels:
            print(f"  从 {category_name} 获取到 {len(channels)} 个频道")
            # 合并到总结果中
            all_channels.update(channels)
        else:
            print(f"  从 {category_name} 未获取到频道")
        
        # 添加延时避免请求过快
        time.sleep(1)
    
    return all_channels

if __name__ == "__main__":
    # 获取所有频道数据
    all_channels = get_all_channels()
    
    path = Path(__file__).parent 

    # 打印结果
    print("\n所有频道数据:")
    for name, url in all_channels.items():
        print(f"{name}: {url}")
    
    # 保存为JSON文件
    with open(path / 'channels.json', 'w', encoding='utf-8') as f:
        json.dump(all_channels, f, ensure_ascii=False, indent=2)
    
    print(f"\n共获取到 {len(all_channels)} 个频道")
    print("数据已保存到 channels.json")

"""
匹配到的详情页，获取节目单，节目单结构
{
    date:[time1:name1,time2:name2,...],
    date2:[time1:name1,time2:name2,...],
    ...
}
//ul[@class="mw"]/li[@class="subheader devicepadding"]/text()获取日期

"""