#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Livescore爬虫任务函数模块
为APScheduler调度器提供具体的任务执行函数
"""

import os
import sys
import logging
import subprocess
from datetime import datetime
from pathlib import Path

# 添加项目路径到sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class LivescoreSpiderTasks:
    """Livescore爬虫任务类"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.spider_dir = Path(__file__).parent.parent
        
    def _setup_logging(self):
        """设置日志"""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _run_spider_command(self, days_back=0, days_forward=0, task_name=""):
        """执行爬虫命令"""
        try:
            # 构建命令
            cmd = [
                sys.executable,
                'run_spider.py',
                '--spider', 'livescore',
                '--days-back', str(days_back),
                '--days-forward', str(days_forward)
            ]
            
            self.logger.info(f"开始执行{task_name}任务: {' '.join(cmd)}")
            
            # 执行命令
            result = subprocess.run(
                cmd,
                cwd=self.spider_dir,
                capture_output=True,
                text=True,
                timeout=1800  # 30分钟超时
            )
            
            if result.returncode == 0:
                self.logger.info(f"{task_name}任务执行成功")
                if result.stdout:
                    self.logger.info(f"输出: {result.stdout[-500:]}")  # 只显示最后500字符
            else:
                self.logger.error(f"{task_name}任务执行失败，返回码: {result.returncode}")
                if result.stderr:
                    self.logger.error(f"错误信息: {result.stderr[-500:]}")
                    
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"{task_name}任务执行超时")
            return False
        except Exception as e:
            self.logger.error(f"{task_name}任务执行异常: {e}")
            return False
    
    def run_current_day_spider(self, days_back=0, days_forward=0):
        """执行当天比赛数据爬取任务"""
        return self._run_spider_command(
            days_back=days_back,
            days_forward=days_forward,
            task_name="当天比赛数据爬取"
        )
    
    def run_historical_spider(self, days_back=7, days_forward=0):
        """执行历史比赛数据爬取任务"""
        return self._run_spider_command(
            days_back=days_back,
            days_forward=days_forward,
            task_name="历史比赛数据爬取"
        )
    
    def run_future_spider(self, days_back=0, days_forward=7):
        """执行未来赛程数据爬取任务"""
        return self._run_spider_command(
            days_back=days_back,
            days_forward=days_forward,
            task_name="未来赛程数据爬取"
        )


# 创建全局实例
_spider_tasks = LivescoreSpiderTasks()

# 导出任务函数
def run_current_day_spider(days_back=0, days_forward=0):
    """当天比赛数据爬取任务"""
    return _spider_tasks.run_current_day_spider(days_back, days_forward)

def run_historical_spider(days_back=7, days_forward=0):
    """历史比赛数据爬取任务"""
    return _spider_tasks.run_historical_spider(days_back, days_forward)

def run_future_spider(days_back=0, days_forward=7):
    """未来赛程数据爬取任务"""
    return _spider_tasks.run_future_spider(days_back, days_forward)


if __name__ == '__main__':
    # 测试任务函数
    import argparse
    
    parser = argparse.ArgumentParser(description='测试爬虫任务函数')
    parser.add_argument('--task', choices=['current', 'historical', 'future'], 
                       required=True, help='要测试的任务类型')
    parser.add_argument('--days-back', type=int, default=0, help='向前天数')
    parser.add_argument('--days-forward', type=int, default=0, help='向后天数')
    
    args = parser.parse_args()
    
    if args.task == 'current':
        result = run_current_day_spider(args.days_back, args.days_forward)
    elif args.task == 'historical':
        result = run_historical_spider(args.days_back, args.days_forward)
    elif args.task == 'future':
        result = run_future_spider(args.days_back, args.days_forward)
    
    print(f"任务执行结果: {'成功' if result else '失败'}")