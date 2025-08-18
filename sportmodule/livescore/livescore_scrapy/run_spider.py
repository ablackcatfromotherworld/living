#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Livescore Scrapy 爬虫运行脚本
只支持通过网页 API 获取数据
"""

import os
import sys
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 添加项目路径
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)
sys.path.append(os.path.dirname(project_dir))

# 导入爬虫
from spiders.livescore_spider import LivescoreSpider

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('livescore_scrapy.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_api_spider(sports=None, languages=None, days_back=1, days_forward=1):
    """
    运行API爬虫（直接从livescore API获取数据）
    
    Args:
        sports (str): 运动类型，逗号分隔，如'soccer,basketball'
        languages (str): 语言，逗号分隔，如'pt,es,en'
        days_back (int): 向前获取多少天的数据
        days_forward (int): 向后获取多少天的数据
    """
    logger.info("开始运行API爬虫...")
    
    # 获取项目设置
    settings = get_project_settings()
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 添加爬虫
    process.crawl(
        LivescoreSpider, 
        sports=sports, 
        languages=languages, 
        days_back=days_back, 
        days_forward=days_forward
    )
    
    # 启动爬虫
    process.start()
    
    logger.info("API爬虫运行完成")





def run_web_spider(sports=None, languages=None, days_back=10, days_forward=30):
    """
    运行Web API爬虫（与主爬虫相同）
    
    Args:
        sports (str): 运动类型，逗号分隔
        languages (str): 语言，逗号分隔
        days_back (int): 向前获取多少天的数据
        days_forward (int): 向后获取多少天的数据
    """
    logger.info("开始运行Web API爬虫...")
    
    # 获取项目设置
    settings = get_project_settings()
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 添加爬虫
    process.crawl(
        LivescoreWebSpider,
        sports=sports,
        languages=languages,
        days_back=days_back,
        days_forward=days_forward
    )
    
    # 启动爬虫
    process.start()
    
    logger.info("Web API爬虫运行完成")





def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Livescore Scrapy 爬虫运行器 - 只支持从API获取数据')
    parser.add_argument('--spider', '-s', choices=['api', 'web'], 
                       default='api', help='选择要运行的爬虫类型')
    
    # API爬虫参数
    parser.add_argument('--sports', help='运动类型，逗号分隔，如: soccer,basketball,tennis')
    parser.add_argument('--languages', help='语言，逗号分隔，如: pt,es,en')
    parser.add_argument('--days-back', type=int, default=10, help='向前获取多少天的数据（默认10天）')
    parser.add_argument('--days-forward', type=int, default=30, help='向后获取多少天的数据（默认30天）')
    
    # 通用参数
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.spider == 'api':
            run_api_spider(args.sports, args.languages, args.days_back, args.days_forward)
        elif args.spider == 'web':
            run_web_spider(args.sports, args.languages, args.days_back, args.days_forward)
        else:
            logger.error(f"未知的爬虫类型: {args.spider}")
            return 1
        
        logger.info("爬虫运行成功完成")
        return 0
        
    except Exception as e:
        logger.error(f"爬虫运行失败: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())


# -*- coding: utf-8 -*-
"""
Livescore Scrapy 运行脚本

使用方法:
1. 运行API爬虫（默认）:
   python run_spider.py

2. 指定运动类型和语言:
   python run_spider.py --sports soccer,basketball --languages pt,es,en

3. 清空数据库表后再插入:
   python run_spider.py --clear-table

4. 显示数据库统计信息:
   python run_spider.py --show-stats
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

from spiders.livescore_spider import LivescoreSpider, LivescoreFileSpider


def setup_logging(log_level='INFO'):
    """设置日志"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def clear_database_table(database_url):
    """清空数据库表"""
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # 清空表数据
            result = conn.execute(text("DELETE FROM livescore"))
            conn.commit()
            
            print(f"已清空数据库表，删除了 {result.rowcount} 条记录")
        
        engine.dispose()
        
    except Exception as e:
        print(f"清空数据库表失败: {e}")
        return False
    
    return True


def get_table_stats(database_url):
    """获取表统计信息"""
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(database_url)
        with engine.connect() as conn:
            # 总记录数
            result = conn.execute(text("SELECT COUNT(*) as total FROM livescore"))
            total_count = result.fetchone()[0]
            
            # 按运动类型统计
            result = conn.execute(text(
                "SELECT sport, COUNT(*) as count FROM livescore GROUP BY sport ORDER BY count DESC"
            ))
            sport_stats = result.fetchall()
            
            # 按语言统计
            result = conn.execute(text(
                "SELECT language, COUNT(*) as count FROM livescore GROUP BY language ORDER BY count DESC"
            ))
            language_stats = result.fetchall()
            
            # 按状态统计
            result = conn.execute(text(
                "SELECT status, COUNT(*) as count FROM livescore GROUP BY status ORDER BY count DESC LIMIT 10"
            ))
            status_stats = result.fetchall()
        
        engine.dispose()
        
        return {
            'total': total_count,
            'by_sport': sport_stats,
            'by_language': language_stats,
            'by_status': status_stats
        }
        
    except Exception as e:
        print(f"获取表统计信息失败: {e}")
        return None


def print_stats(stats):
    """打印统计信息"""
    if not stats:
        return
    
    print("\n" + "="*50)
    print("数据库统计信息")
    print("="*50)
    
    print(f"总记录数: {stats['total']:,}")
    
    print("\n按运动类型统计:")
    for sport, count in stats['by_sport']:
        print(f"  {sport}: {count:,}")
    
    print("\n按语言统计:")
    for language, count in stats['by_language']:
        print(f"  {language}: {count:,}")
    
    print("\n按状态统计 (前10):")
    for status, count in stats['by_status']:
        print(f"  {status}: {count:,}")
    
    print("="*50)


def explain_match_status():
    """解释比赛状态含义"""
    print("\n" + "="*60)
    print("比赛状态说明")
    print("="*60)
    
    status_explanations = {
        "未开始状态": {
            'scheduled': '已安排 - 比赛已被安排但尚未开始',
            'not_started': '未开始 - 比赛尚未开始',
            'upcoming': '即将开始 - 比赛即将开始',
            'postponed': '推迟 - 比赛被推迟到其他时间',
            'cancelled': '取消 - 比赛被取消',
            'delayed': '延迟 - 比赛开始时间延迟',
        },
        "进行中状态": {
            'live': '进行中 - 比赛正在进行',
            'in_progress': '进行中 - 比赛正在进行',
            'first_half': '上半场 - 比赛处于上半场',
            'second_half': '下半场 - 比赛处于下半场',
            'halftime': '中场休息 - 比赛处于中场休息',
            'overtime': '加时赛 - 比赛进入加时赛',
            'penalty': '点球大战 - 比赛进入点球大战',
            'break': '休息 - 比赛处于休息时间',
        },
        "已结束状态": {
            'finished': '已结束 - 比赛已正常结束',
            'full_time': '全场结束 - 比赛全场时间结束',
            'completed': '已完成 - 比赛已完成',
            'final': '最终 - 比赛最终结果',
            'ended': '已结束 - 比赛已结束',
        },
        "特殊状态": {
            'suspended': '暂停 - 比赛被暂停',
            'interrupted': '中断 - 比赛被中断',
            'abandoned': '放弃 - 比赛被放弃',
            'walkover': '弃权 - 一方弃权',
            'awarded': '判决 - 通过判决决定结果',
            'unknown': '未知 - 状态未知',
        }
    }
    
    for category, statuses in status_explanations.items():
        print(f"\n{category}:")
        for status, explanation in statuses.items():
            print(f"  {status:12} - {explanation}")
    
    print("\n" + "="*60)
    print("注意事项:")
    print("- 不同数据源可能使用不同的状态值")
    print("- 某些状态可能因运动类型而有所不同")
    print("- 建议在数据处理时进行状态标准化")
    print("="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Livescore Scrapy 数据处理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--spider',
        choices=['api', 'web'],
        default='api',
        help='选择要运行的爬虫类型 (默认: api)'
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
        '--clear-table',
        action='store_true',
        help='运行前清空数据库表'
    )
    
    parser.add_argument(
        '--show-stats',
        action='store_true',
        help='显示数据库统计信息'
    )
    
    parser.add_argument(
        '--explain-status',
        action='store_true',
        help='解释比赛状态含义'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='日志级别 (默认: INFO)'
    )
    
    parser.add_argument(
        '--database-url',
        default='mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider',
        help='数据库连接URL'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.log_level)
    
    # 解释比赛状态
    if args.explain_status:
        explain_match_status()
        return
    
    # 显示统计信息
    if args.show_stats:
        stats = get_table_stats(args.database_url)
        print_stats(stats)
        return
    
    # 清空数据库表
    if args.clear_table:
        print("正在清空数据库表...")
        if not clear_database_table(args.database_url):
            print("清空数据库表失败，退出")
            return
    
    # 获取Scrapy设置
    settings = get_project_settings()
    
    # 更新设置
    settings.set('DATABASE_URL', args.database_url)
    settings.set('BATCH_SIZE', args.batch_size)
    settings.set('LOG_LEVEL', args.log_level)
    
    # 创建爬虫进程
    process = CrawlerProcess(settings)
    
    # 根据选择的爬虫添加不同的参数
    if args.spider == 'api':
        process.crawl(
            LivescoreSpider,
            sports=args.sports,
            languages=args.languages,
            days_back=args.days_back,
            days_forward=args.days_forward
        )
    elif args.spider == 'web':
        from spiders.livescore_spider import LivescoreWebSpider
        process.crawl(
            LivescoreWebSpider,
            sports=args.sports,
            languages=args.languages,
            days_back=args.days_back,
            days_forward=args.days_forward
        )
    
    print(f"开始运行 {args.spider} 爬虫...")
    
    # 运行爬虫
    process.start()
    
    print("爬虫运行完成")
    
    # 显示最终统计信息
    print("\n获取最终统计信息...")
    stats = get_table_stats(args.database_url)
    print_stats(stats)


if __name__ == '__main__':
    main()