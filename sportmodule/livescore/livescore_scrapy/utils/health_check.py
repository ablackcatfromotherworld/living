#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康检查工具模块
用于监控系统健康状态
"""

import os
import sys
import logging
import psutil
import requests
from datetime import datetime
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self.logger = self._setup_logging()
    
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
    
    def check_system_resources(self):
        """检查系统资源"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            self.logger.info(f"系统资源检查 - CPU: {cpu_percent}%, 内存: {memory_percent}%, 磁盘: {disk_percent:.1f}%")
            
            # 检查资源是否超限
            warnings = []
            if cpu_percent > 80:
                warnings.append(f"CPU使用率过高: {cpu_percent}%")
            if memory_percent > 80:
                warnings.append(f"内存使用率过高: {memory_percent}%")
            if disk_percent > 80:
                warnings.append(f"磁盘使用率过高: {disk_percent:.1f}%")
            
            if warnings:
                for warning in warnings:
                    self.logger.warning(warning)
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"系统资源检查失败: {e}")
            return False
    
    def check_network_connectivity(self):
        """检查网络连接"""
        test_urls = [
            'https://www.google.com',
            'https://www.livescore.com',
            'https://httpbin.org/get'
        ]
        
        success_count = 0
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    success_count += 1
                    self.logger.info(f"网络连接检查成功: {url}")
                else:
                    self.logger.warning(f"网络连接异常: {url}, 状态码: {response.status_code}")
            except Exception as e:
                self.logger.error(f"网络连接失败: {url}, 错误: {e}")
        
        success_rate = success_count / len(test_urls)
        if success_rate >= 0.5:  # 至少50%的连接成功
            self.logger.info(f"网络连接检查通过，成功率: {success_rate:.1%}")
            return True
        else:
            self.logger.error(f"网络连接检查失败，成功率: {success_rate:.1%}")
            return False
    
    def check_log_files(self):
        """检查日志文件"""
        try:
            logs_dir = Path('logs')
            if not logs_dir.exists():
                self.logger.warning("日志目录不存在")
                return False
            
            # 检查日志文件大小
            large_files = []
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_size > 100 * 1024 * 1024:  # 100MB
                    large_files.append(log_file.name)
            
            if large_files:
                self.logger.warning(f"发现大型日志文件: {', '.join(large_files)}")
            
            self.logger.info("日志文件检查完成")
            return True
            
        except Exception as e:
            self.logger.error(f"日志文件检查失败: {e}")
            return False
    
    def check_process_status(self):
        """检查进程状态"""
        try:
            current_process = psutil.Process()
            
            # 检查进程信息
            process_info = {
                'pid': current_process.pid,
                'name': current_process.name(),
                'status': current_process.status(),
                'cpu_percent': current_process.cpu_percent(),
                'memory_percent': current_process.memory_percent(),
                'create_time': datetime.fromtimestamp(current_process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.logger.info(f"进程状态检查: PID={process_info['pid']}, "
                           f"状态={process_info['status']}, "
                           f"CPU={process_info['cpu_percent']:.1f}%, "
                           f"内存={process_info['memory_percent']:.1f}%")
            
            return True
            
        except Exception as e:
            self.logger.error(f"进程状态检查失败: {e}")
            return False
    
    def perform_full_health_check(self):
        """执行完整的健康检查"""
        self.logger.info("开始执行健康检查...")
        
        checks = [
            ('系统资源', self.check_system_resources),
            ('网络连接', self.check_network_connectivity),
            ('日志文件', self.check_log_files),
            ('进程状态', self.check_process_status)
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                result = check_func()
                results[check_name] = result
                status = "通过" if result else "失败"
                self.logger.info(f"{check_name}检查: {status}")
            except Exception as e:
                results[check_name] = False
                self.logger.error(f"{check_name}检查异常: {e}")
        
        # 统计结果
        passed_checks = sum(results.values())
        total_checks = len(results)
        success_rate = passed_checks / total_checks
        
        if success_rate >= 0.8:  # 80%以上检查通过
            self.logger.info(f"健康检查完成，通过率: {success_rate:.1%} ({passed_checks}/{total_checks})")
            return True
        else:
            self.logger.error(f"健康检查失败，通过率: {success_rate:.1%} ({passed_checks}/{total_checks})")
            return False


# 创建全局实例
_health_checker = HealthChecker()

# 导出函数
def perform_health_check():
    """执行健康检查"""
    return _health_checker.perform_full_health_check()

def check_system_resources():
    """检查系统资源"""
    return _health_checker.check_system_resources()

def check_network_connectivity():
    """检查网络连接"""
    return _health_checker.check_network_connectivity()


if __name__ == '__main__':
    # 测试健康检查
    result = perform_health_check()
    print(f"健康检查结果: {'通过' if result else '失败'}")