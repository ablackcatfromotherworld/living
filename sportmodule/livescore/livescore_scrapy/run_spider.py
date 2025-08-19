#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Livescore Scrapy 爬虫运行脚本
"""

import os
import sys
import argparse
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 添加项目路径到Python路径
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from spiders.livescore_spider import LivescoreSpider


def setup_logging(log_level='INFO'):
    """设置日志配置"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('livescore_scrapy.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Livescore Scrapy 数据爬虫',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  python run_spider.py                                    # 运行默认爬虫
  python run_spider.py --sports soccer,basketball         # 指定运动类型
  python run_spider.py --languages pt,es,en               # 指定语言
        """
    )
    
    parser.add_argument(
        '--sports',
        help='运动类型，逗号分隔，如: soccer,basketball,tennis'
    )
    
    parser.add_argument(
        '--languages',
        help='语言，逗号分隔，如: pt,es,en'
    )
    
    parser.add_argument(
        '--days-back',
        type=int,
        default=10,
        help='向前获取多少天的数据（默认10天）'
    )
    
    parser.add_argument(
        '--days-forward',
        type=int,
        default=30,
        help='向后获取多少天的数据（默认30天）'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='批处理大小 (默认: 100)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='日志级别 (默认: INFO)'
    )
    
    parser.add_argument(
        '--database-url',
        default='mysql+pymysql://spider_0818:3IQ6fgAQVad0PylSEg.@43.157.134.155:33070/spider',
        help='数据库连接URL'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.log_level)
    
    # 获取Scrapy设置
    settings = get_project_settings()
    
    # 更新设置
    settings.set('DATABASE_URL', args.database_url)
    settings.set('BATCH_SIZE', args.batch_size)
    settings.set('LOG_LEVEL', args.log_level)
    
    # 使用重构后的管道
    settings.set('ITEM_PIPELINES', {
        'pipelines.refactored_database_pipeline.RefactoredDatabasePipeline': 400,
    })
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 添加爬虫
    process.crawl(
        LivescoreSpider,
        sports=args.sports,
        languages=args.languages,
        days_back=args.days_back,
        days_forward=args.days_forward
    )
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 开始运行爬虫...")
    logger.info(f"🌐 数据库: {args.database_url.split('@')[1] if '@' in args.database_url else 'localhost'}")
    
    # 运行爬虫
    try:
        process.start()
        logger.info("✅ 爬虫运行完成")
    except Exception as e:
        logger.error(f"❌ 爬虫运行失败: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())