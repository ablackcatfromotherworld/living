#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多进程并行爬虫调度器
用于同时运行15个独立的运动爬虫，大幅提升数据采集速度
"""

import os
import sys
import time
import signal
import logging
import multiprocessing
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('logs/parallel_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 15个运动爬虫配置（与sports_spider.py中sport_priorities保持一致）
SPIDERS_CONFIG = [
    {"name": "football_spider", "sport_name": "Football", "sport_id": 1},
    {"name": "volleyball_spider", "sport_name": "Volleyball", "sport_id": 23},
    {"name": "beachvolleyball_spider", "sport_name": "Beach Volleyball", "sport_id": 34},
    {"name": "futsal_spider", "sport_name": "Futsal", "sport_id": 29},
    {"name": "basketball_spider", "sport_name": "Basketball", "sport_id": 2},
    {"name": "mma_spider", "sport_name": "MMA", "sport_id": 117},
    {"name": "tennis_spider", "sport_name": "Tennis", "sport_id": 5},
    {"name": "americanfootball_spider", "sport_name": "American Football", "sport_id": 16},
    {"name": "formula1_spider", "sport_name": "Formula 1", "sport_id": 40},
    {"name": "rally_spider", "sport_name": "Rally", "sport_id": 101},
    {"name": "handball_spider", "sport_name": "Handball", "sport_id": 6},
    {"name": "tabletennis_spider", "sport_name": "Table Tennis", "sport_id": 20},
    {"name": "badminton_spider", "sport_name": "Badminton", "sport_id": 31},
    {"name": "snooker_spider", "sport_name": "Snooker", "sport_id": 19},
    {"name": "beachhandball_spider", "sport_name": "Beach Handball", "sport_id": 157}
]

class ParallelSpiderScheduler:
    def __init__(self, max_workers=None, test_mode=False, selected_sports=None):
        """
        初始化并行爬虫调度器
        
        Args:
            max_workers: 最大并行进程数，默认为CPU核心数
            test_mode: 测试模式，只运行少量爬虫
            selected_sports: 指定运行的运动ID列表
        """
        self.max_workers = max_workers or min(len(SPIDERS_CONFIG), multiprocessing.cpu_count())
        self.test_mode = test_mode
        self.selected_sports = selected_sports or []
        self.running = True
        self.processes = []
        
        # 确保日志目录存在
        os.makedirs('logs', exist_ok=True)
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info(f"并行爬虫调度器初始化完成，最大并行数: {self.max_workers}")
    
    def signal_handler(self, signum, frame):
        """信号处理器 - 优雅停止"""
        logger.info(f"接收到信号 {signum}，正在停止所有爬虫...")
        self.running = False
        self.stop_all_processes()
        sys.exit(0)
    
    def stop_all_processes(self):
        """停止所有运行中的进程"""
        for process in self.processes:
            if process.poll() is None:  # 进程仍在运行
                try:
                    process.terminate()
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    logger.error(f"停止进程失败: {e}")
    
    def run_single_spider(self, spider_config):
        """
        运行单个爬虫
        
        Args:
            spider_config: 爬虫配置字典
            
        Returns:
            tuple: (spider_name, success, duration, message)
        """
        spider_name = spider_config['name']
        sport_name = spider_config['sport_name']
        sport_id = spider_config['sport_id']
        
        start_time = time.time()
        
        try:
            logger.info(f"开始运行爬虫: {sport_name} ({spider_name})")
            
            # 构建scrapy命令
            cmd = [
                'scrapy', 'crawl', spider_name,
                # '-s', 'LOG_FILE=logs/{}.log'.format(spider_name),
                '-s', 'LOG_LEVEL=INFO'
            ]
            
            # 运行爬虫 - 让日志直接输出到终端
            process = subprocess.Popen(
                cmd,
                text=True,
                encoding='utf-8'
            )
            
            # 等待进程完成
            return_code = process.wait()
            
            duration = time.time() - start_time
            
            if return_code == 0:
                logger.info(f"爬虫 {sport_name} 运行成功，耗时: {duration:.2f}秒")
                return (spider_name, True, duration, "成功")
            else:
                logger.error(f"爬虫 {sport_name} 运行失败，返回码: {return_code}")
                return (spider_name, False, duration, f"返回码: {return_code}")
                
        except Exception as e:
            duration = time.time() - start_time
            error_msg = str(e)
            logger.error(f"爬虫 {sport_name} 运行异常: {error_msg}")
            return (spider_name, False, duration, error_msg)
    
    def get_spiders_to_run(self):
        """获取需要运行的爬虫列表"""
        spiders = SPIDERS_CONFIG.copy()
        
        # 如果指定了特定运动，只运行这些
        if self.selected_sports:
            spiders = [s for s in spiders if s['sport_id'] in self.selected_sports]
        
        # 测试模式只运行前3个爬虫
        if self.test_mode:
            spiders = spiders[:3]
            logger.info("测试模式：只运行前3个爬虫")
        
        return spiders
    
    def run_parallel(self):
        """并行运行所有爬虫"""
        spiders_to_run = self.get_spiders_to_run()
        
        if not spiders_to_run:
            logger.warning("没有找到需要运行的爬虫")
            return
        
        logger.info(f"准备并行运行 {len(spiders_to_run)} 个爬虫")
        
        start_time = time.time()
        results = []
        
        try:
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                # 提交所有任务
                future_to_spider = {
                    executor.submit(self.run_single_spider, spider): spider
                    for spider in spiders_to_run
                }
                
                # 收集结果
                for future in as_completed(future_to_spider):
                    if not self.running:
                        break
                    
                    spider = future_to_spider[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.error(f"爬虫 {spider['sport_name']} 执行异常: {e}")
                        results.append((spider['name'], False, 0, str(e)))
        
        except KeyboardInterrupt:
            logger.info("用户中断，正在停止所有爬虫...")
            self.running = False
        
        total_duration = time.time() - start_time
        
        # 统计结果
        self.print_summary(results, total_duration)
    
    def print_summary(self, results, total_duration):
        """打印运行总结"""
        successful = [r for r in results if r[1]]
        failed = [r for r in results if not r[1]]
        
        logger.info("\n" + "="*60)
        logger.info("并行爬虫运行总结")
        logger.info("="*60)
        logger.info(f"总运行时间: {total_duration:.2f}秒")
        logger.info(f"成功: {len(successful)} 个")
        logger.info(f"失败: {len(failed)} 个")
        logger.info(f"总计: {len(results)} 个")
        
        if successful:
            logger.info("\n成功的爬虫:")
            for spider_name, _, duration, _ in successful:
                logger.info(f"  - {spider_name}: {duration:.2f}秒")
        
        if failed:
            logger.info("\n失败的爬虫:")
            for spider_name, _, duration, error in failed:
                logger.info(f"  - {spider_name}: {error}")
        
        # 计算性能提升
        if successful:
            avg_duration = sum(r[2] for r in successful) / len(successful)
            estimated_sequential_time = avg_duration * len(results)
            speedup = estimated_sequential_time / total_duration if total_duration > 0 else 1
            logger.info(f"\n性能提升: {speedup:.1f}x (相比顺序执行)")
        
        logger.info("="*60)
    
    def run_continuous(self, interval_minutes=30):
        """连续运行模式"""
        logger.info(f"启动连续运行模式，刷新间隔: {interval_minutes}分钟")
        
        while self.running:
            try:
                logger.info(f"开始新一轮并行爬取 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.run_parallel()
                
                if self.running:
                    logger.info(f"本轮爬取完成，等待 {interval_minutes} 分钟后开始下一轮...")
                    time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("用户中断连续运行")
                break
            except Exception as e:
                logger.error(f"连续运行出错: {e}")
                if self.running:
                    logger.info("5分钟后重试...")
                    time.sleep(300)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='并行体育数据爬虫调度器')
    parser.add_argument('--workers', type=int, help='最大并行进程数')
    parser.add_argument('--test', action='store_true', help='测试模式（只运行前3个爬虫）')
    parser.add_argument('--continuous', action='store_true', help='连续运行模式')
    parser.add_argument('--interval', type=int, default=30, help='连续模式刷新间隔（分钟）')
    parser.add_argument('--sports', type=str, help='指定运动ID，用逗号分隔（如：1,2,5）')
    
    args = parser.parse_args()
    
    # 解析指定的运动ID
    selected_sports = []
    if args.sports:
        try:
            selected_sports = [int(x.strip()) for x in args.sports.split(',')]
        except ValueError:
            logger.error("运动ID格式错误，请使用逗号分隔的数字")
            return
    
    # 创建调度器
    scheduler = ParallelSpiderScheduler(
        max_workers=args.workers,
        test_mode=args.test,
        selected_sports=selected_sports
    )
    
    try:
        if args.continuous:
            scheduler.run_continuous(args.interval)
        else:
            scheduler.run_parallel()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        scheduler.stop_all_processes()

if __name__ == '__main__':
    main()