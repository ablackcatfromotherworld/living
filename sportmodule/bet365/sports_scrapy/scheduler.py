#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
体育数据爬虫实时刷新调度器
支持循环运行爬虫，保持数据实时更新
"""

import os
import sys
import time
import signal
import argparse
import logging
from datetime import datetime, timedelta
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from multiprocessing import Process

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SportsCrawlerScheduler:
    """体育数据爬虫调度器"""
    
    def __init__(self, interval_minutes=30, test_mode=False, sport_id=None):
        self.interval_minutes = interval_minutes
        self.test_mode = test_mode
        self.sport_id = sport_id
        self.running = True
        self.setup_logging()
        self.setup_signal_handlers()
        
    def setup_logging(self):
        """设置日志记录"""
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'scheduler_{datetime.now().strftime("%Y%m%d")}.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_signal_handlers(self):
        """设置信号处理器，支持优雅停止"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """信号处理函数"""
        self.logger.info(f"接收到信号 {signum}，准备停止调度器...")
        self.running = False
        
    def run_spider_process(self):
        """在独立进程中运行爬虫"""
        try:
            # 获取项目设置
            settings = get_project_settings()
            
            # 设置Pipeline
            settings.set('ITEM_PIPELINES', {
                'sports_scrapy.pipelines.MySQLPipeline': 100,
            })
            
            if self.test_mode:
                settings.set('DOWNLOAD_DELAY', 2)
                settings.set('CONCURRENT_REQUESTS', 1)
                settings.set('CLOSESPIDER_ITEMCOUNT', 100)
                self.logger.info("运行在测试模式")
            
            # 创建爬虫进程
            process = CrawlerProcess(settings)
            
            spider_kwargs = {}
            if self.sport_id:
                spider_kwargs['sport_id'] = self.sport_id
                self.logger.info(f"指定体育项目ID: {self.sport_id}")
            
            self.logger.info("开始运行爬虫...")
            process.crawl('sports_spider', **spider_kwargs)
            process.start()
            
        except Exception as e:
            self.logger.error(f"爬虫运行出错: {e}")
            raise
            
    def run_single_crawl(self):
        """运行单次爬取"""
        start_time = datetime.now()
        self.logger.info(f"开始第 {self.crawl_count} 次爬取 - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 在独立进程中运行爬虫
            spider_process = Process(target=self.run_spider_process)
            spider_process.start()
            spider_process.join()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            if spider_process.exitcode == 0:
                self.logger.info(f"第 {self.crawl_count} 次爬取完成 - 耗时: {duration}")
                return True
            else:
                self.logger.error(f"第 {self.crawl_count} 次爬取失败 - 退出码: {spider_process.exitcode}")
                return False
                
        except Exception as e:
            self.logger.error(f"第 {self.crawl_count} 次爬取异常: {e}")
            return False
            
    def wait_for_next_run(self):
        """等待下次运行"""
        next_run_time = datetime.now() + timedelta(minutes=self.interval_minutes)
        self.logger.info(f"下次运行时间: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')} (间隔 {self.interval_minutes} 分钟)")
        
        # 分段等待，以便能够响应停止信号
        wait_seconds = self.interval_minutes * 60
        check_interval = 10  # 每10秒检查一次停止信号
        
        while wait_seconds > 0 and self.running:
            sleep_time = min(check_interval, wait_seconds)
            time.sleep(sleep_time)
            wait_seconds -= sleep_time
            
    def start(self):
        """启动调度器"""
        self.logger.info("=" * 60)
        self.logger.info("体育数据爬虫调度器启动")
        self.logger.info(f"刷新间隔: {self.interval_minutes} 分钟")
        self.logger.info(f"测试模式: {'是' if self.test_mode else '否'}")
        if self.sport_id:
            self.logger.info(f"指定体育项目: {self.sport_id}")
        self.logger.info("按 Ctrl+C 停止调度器")
        self.logger.info("=" * 60)
        
        self.crawl_count = 0
        
        try:
            while self.running:
                self.crawl_count += 1
                
                # 运行爬虫
                success = self.run_single_crawl()
                
                if not self.running:
                    break
                    
                if not success:
                    self.logger.warning("爬取失败，但将继续下次尝试")
                
                # 等待下次运行
                if self.running:
                    self.wait_for_next_run()
                    
        except KeyboardInterrupt:
            self.logger.info("接收到键盘中断信号")
        except Exception as e:
            self.logger.error(f"调度器运行异常: {e}")
        finally:
            self.logger.info("调度器已停止")
            self.logger.info(f"总共完成 {self.crawl_count} 次爬取")

def main():
    parser = argparse.ArgumentParser(description='体育数据爬虫实时刷新调度器')
    parser.add_argument('--interval', '-i', type=int, default=30, 
                       help='刷新间隔（分钟），默认30分钟')
    parser.add_argument('--sport', type=int, help='指定体育项目ID')
    parser.add_argument('--test', action='store_true', help='测试模式')
    
    args = parser.parse_args()
    
    # 验证参数
    if args.interval < 1:
        print("错误: 刷新间隔必须大于0分钟")
        sys.exit(1)
        
    try:
        scheduler = SportsCrawlerScheduler(
            interval_minutes=args.interval,
            test_mode=args.test,
            sport_id=args.sport
        )
        scheduler.start()
        
    except Exception as e:
        print(f"调度器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()