#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体育数据爬虫运行脚本
支持单一爬虫模式和并行爬虫模式
"""

import os
import sys
import time
import signal
import logging
import subprocess
import argparse
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/spider_runner.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 全局变量控制连续运行
running = True

def signal_handler(signum, frame):
    """信号处理函数 - 优雅停止"""
    global running
    logger.info(f"接收到信号 {signum}，正在停止爬虫...")
    running = False

def run_spider_process():
    """在独立进程中运行爬虫"""
    try:
        # 获取项目设置
        settings = get_project_settings()
        
        # 设置Pipeline
        settings.set('ITEM_PIPELINES', {
            'sports_scrapy.pipelines.MySQLPipeline': 100,
        })
        
        # 创建爬虫进程
        process = CrawlerProcess(settings)
        process.crawl('sports_spider')
        process.start()
        
    except Exception as e:
        logger.error(f"爬虫运行出错: {e}")
        raise

def run_single_crawl():
    """运行单次爬虫（原有模式）"""
    spider_process = Process(target=run_spider_process)
    spider_process.start()
    spider_process.join()
    return spider_process.exitcode == 0

def run_parallel_spiders(test_mode=False, selected_sports=None, workers=None):
    """运行并行爬虫"""
    try:
        logger.info("开始运行体育数据爬虫（并行模式）...")
        start_time = time.time()
        
        # 构建并行调度器命令
        cmd = ['python', 'parallel_scheduler.py']
        
        if test_mode:
            cmd.append('--test')
        
        if selected_sports:
            cmd.extend(['--sports', ','.join(map(str, selected_sports))])
        
        if workers:
            cmd.extend(['--workers', str(workers)])
        
        # 运行并行调度器
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            logger.info(f"并行爬虫运行成功，耗时: {duration:.2f}秒")
        else:
            logger.error(f"并行爬虫运行失败: {result.stderr}")
            
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"运行并行爬虫时发生错误: {e}")
        return False

def run_continuous_single(interval_minutes=30):
    """连续运行单一爬虫（原有模式）"""
    global running
    
    logger.info(f"启动连续运行模式（单一爬虫），刷新间隔: {interval_minutes}分钟")
    
    crawl_count = 0
    
    try:
        while running:
            crawl_count += 1
            start_time = datetime.now()
            logger.info(f"开始第 {crawl_count} 次爬取 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 运行爬虫
            success = run_single_crawl()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            if success:
                logger.info(f"第 {crawl_count} 次爬取完成 - 耗时: {duration}")
            else:
                logger.warning(f"第 {crawl_count} 次爬取失败，但将继续下次尝试")
            
            if not running:
                break
                
            # 等待下次运行
            next_run_time = datetime.now() + timedelta(minutes=interval_minutes)
            logger.info(f"下次运行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')} (间隔 {interval_minutes} 分钟)")
            
            # 分段等待，以便能够响应停止信号
            wait_seconds = interval_minutes * 60
            check_interval = 10  # 每10秒检查一次停止信号
            
            while wait_seconds > 0 and running:
                sleep_time = min(check_interval, wait_seconds)
                time.sleep(sleep_time)
                wait_seconds -= sleep_time
                
    except KeyboardInterrupt:
        logger.info("接收到键盘中断信号")
    except Exception as e:
        logger.error(f"运行异常: {e}")
    finally:
        logger.info("爬虫已停止")
        logger.info(f"总共完成 {crawl_count} 次爬取")

def run_continuous_parallel(interval_minutes=30, test_mode=False, selected_sports=None, workers=None):
    """连续运行并行爬虫"""
    global running
    
    logger.info(f"启动连续运行模式（并行爬虫），刷新间隔: {interval_minutes}分钟")
    
    crawl_count = 0
    
    try:
        while running:
            crawl_count += 1
            start_time = datetime.now()
            logger.info(f"开始第 {crawl_count} 次并行爬取 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 运行并行爬虫
            success = run_parallel_spiders(test_mode, selected_sports, workers)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            if success:
                logger.info(f"第 {crawl_count} 次并行爬取完成 - 耗时: {duration}")
            else:
                logger.warning(f"第 {crawl_count} 次并行爬取失败，但将继续下次尝试")
            
            if not running:
                break
                
            # 等待下次运行
            next_run_time = datetime.now() + timedelta(minutes=interval_minutes)
            logger.info(f"下次运行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')} (间隔 {interval_minutes} 分钟)")
            
            # 分段等待，以便能够响应停止信号
            wait_seconds = interval_minutes * 60
            check_interval = 10  # 每10秒检查一次停止信号
            
            while wait_seconds > 0 and running:
                sleep_time = min(check_interval, wait_seconds)
                time.sleep(sleep_time)
                wait_seconds -= sleep_time
                
    except KeyboardInterrupt:
        logger.info("接收到键盘中断信号")
    except Exception as e:
        logger.error(f"运行异常: {e}")
    finally:
        logger.info("并行爬虫已停止")
        logger.info(f"总共完成 {crawl_count} 次爬取")

def main():
    """主函数 - 支持单一和并行模式"""
    global running
    
    parser = argparse.ArgumentParser(description='体育数据爬虫运行脚本')
    parser.add_argument('--mode', choices=['single', 'parallel'], default='single', 
                       help='运行模式：single（单一爬虫）或 parallel（并行爬虫）')
    parser.add_argument('--continuous', action='store_true', help='连续运行模式')
    parser.add_argument('--interval', type=int, default=30, help='连续模式刷新间隔（分钟）')
    parser.add_argument('--test', action='store_true', help='测试模式（仅并行模式有效）')
    parser.add_argument('--sports', type=str, help='指定运动ID，用逗号分隔（仅并行模式有效）')
    parser.add_argument('--workers', type=int, help='最大并行进程数（仅并行模式有效）')
    
    args = parser.parse_args()
    
    # 设置信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 确保日志目录存在
    os.makedirs('logs', exist_ok=True)
    
    # 解析指定的运动ID
    selected_sports = []
    if args.sports:
        try:
            selected_sports = [int(x.strip()) for x in args.sports.split(',')]
        except ValueError:
            logger.error("运动ID格式错误，请使用逗号分隔的数字")
            return
    
    logger.info(f"体育数据爬虫启动 - 模式: {args.mode}")
    logger.info("按 Ctrl+C 停止运行")
    
    try:
        if args.continuous:
            if args.mode == 'parallel':
                run_continuous_parallel(args.interval, args.test, selected_sports, args.workers)
            else:
                run_continuous_single(args.interval)
        else:
            if args.mode == 'parallel':
                run_parallel_spiders(args.test, selected_sports, args.workers)
            else:
                success = run_single_crawl()
                if success:
                    logger.info("单次爬取完成")
                else:
                    logger.error("单次爬取失败")
    
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")

if __name__ == '__main__':
    main()