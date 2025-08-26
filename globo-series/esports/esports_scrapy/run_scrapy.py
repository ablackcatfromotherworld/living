#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrapy运行脚本
用于测试和运行Globo Sports爬虫
"""

import os
import sys
import logging
import subprocess
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# 导入spider
from esports_scrapy.spiders.globo_sports_spider import GloboSportsSpider

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler('scrapy_run.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_scrapy_settings():
    """获取Scrapy设置"""
    # 使用项目的settings.py中的设置
    return get_project_settings()

def run_sports_spider():
    """运行体育数据爬虫"""
    print("开始运行Globo Sports Spider")
    
    settings = get_scrapy_settings()
    process = CrawlerProcess(settings)
    
    try:
        process.crawl(GloboSportsSpider)
        process.start()
        print("\n体育数据爬取完成！")
    except Exception as e:
        print(f"运行爬虫时出错: {e}")


def main():
    """主函数"""
    setup_logging()
    
    run_sports_spider()

if __name__ == "__main__":
    main()