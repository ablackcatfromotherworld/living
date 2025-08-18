#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接检查工具模块
用于监控数据库连接状态和性能
"""

import os
import sys
import logging
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import sqlalchemy
    from sqlalchemy import create_engine, text
    from settings import DATABASE_URL
except ImportError as e:
    print(f"导入依赖失败: {e}")
    DATABASE_URL = None


class DatabaseChecker:
    """数据库检查器"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.database_url = DATABASE_URL
        self.engine = None
    
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
    
    def _create_engine(self):
        """创建数据库引擎"""
        if not self.database_url:
            self.logger.error("数据库URL未配置")
            return None
        
        try:
            self.engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                connect_args={"connect_timeout": 10}
            )
            return self.engine
        except Exception as e:
            self.logger.error(f"创建数据库引擎失败: {e}")
            return None
    
    def check_connection(self):
        """检查数据库连接"""
        if not self.engine:
            self.engine = self._create_engine()
            if not self.engine:
                return False
        
        try:
            start_time = time.time()
            
            with self.engine.connect() as connection:
                # 执行简单查询测试连接
                result = connection.execute(text("SELECT 1"))
                result.fetchone()
            
            connection_time = time.time() - start_time
            self.logger.info(f"数据库连接检查成功，耗时: {connection_time:.3f}秒")
            
            # 检查连接时间是否过长
            if connection_time > 5.0:
                self.logger.warning(f"数据库连接时间过长: {connection_time:.3f}秒")
            
            return True
            
        except Exception as e:
            self.logger.error(f"数据库连接检查失败: {e}")
            return False
    
    def check_tables_exist(self):
        """检查必要的表是否存在"""
        if not self.engine:
            self.engine = self._create_engine()
            if not self.engine:
                return False
        
        required_tables = ['matches', 'teams']  # 根据实际情况调整
        
        try:
            with self.engine.connect() as connection:
                # 获取所有表名
                if 'postgresql' in self.database_url:
                    query = text("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """)
                elif 'mysql' in self.database_url:
                    query = text("SHOW TABLES")
                elif 'sqlite' in self.database_url:
                    query = text("""
                        SELECT name FROM sqlite_master 
                        WHERE type='table'
                    """)
                else:
                    self.logger.warning("未知的数据库类型，跳过表检查")
                    return True
                
                result = connection.execute(query)
                existing_tables = [row[0] for row in result.fetchall()]
                
                missing_tables = [table for table in required_tables if table not in existing_tables]
                
                if missing_tables:
                    self.logger.error(f"缺少必要的表: {', '.join(missing_tables)}")
                    return False
                else:
                    self.logger.info(f"所有必要的表都存在: {', '.join(required_tables)}")
                    return True
                    
        except Exception as e:
            self.logger.error(f"检查表存在性失败: {e}")
            return False
    
    def check_database_size(self):
        """检查数据库大小"""
        if not self.engine:
            self.engine = self._create_engine()
            if not self.engine:
                return False
        
        try:
            with self.engine.connect() as connection:
                if 'postgresql' in self.database_url:
                    query = text("""
                        SELECT pg_size_pretty(pg_database_size(current_database())) as size
                    """)
                    result = connection.execute(query)
                    size = result.fetchone()[0]
                    self.logger.info(f"数据库大小: {size}")
                elif 'mysql' in self.database_url:
                    query = text("""
                        SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS size_mb
                        FROM information_schema.tables 
                        WHERE table_schema = DATABASE()
                    """)
                    result = connection.execute(query)
                    size_mb = result.fetchone()[0]
                    self.logger.info(f"数据库大小: {size_mb} MB")
                else:
                    self.logger.info("数据库大小检查跳过（不支持的数据库类型）")
                
                return True
                
        except Exception as e:
            self.logger.error(f"检查数据库大小失败: {e}")
            return False
    
    def check_recent_data(self):
        """检查最近的数据"""
        if not self.engine:
            self.engine = self._create_engine()
            if not self.engine:
                return False
        
        try:
            with self.engine.connect() as connection:
                # 检查matches表的最新数据
                query = text("""
                    SELECT COUNT(*) as count, MAX(created_at) as latest_time
                    FROM matches 
                    WHERE created_at >= NOW() - INTERVAL '24 hours'
                """)
                
                # 根据数据库类型调整查询
                if 'sqlite' in self.database_url:
                    query = text("""
                        SELECT COUNT(*) as count, MAX(created_at) as latest_time
                        FROM matches 
                        WHERE created_at >= datetime('now', '-24 hours')
                    """)
                elif 'mysql' in self.database_url:
                    query = text("""
                        SELECT COUNT(*) as count, MAX(created_at) as latest_time
                        FROM matches 
                        WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    """)
                
                result = connection.execute(query)
                row = result.fetchone()
                
                if row:
                    count, latest_time = row
                    self.logger.info(f"最近24小时内的数据: {count} 条，最新时间: {latest_time}")
                    
                    if count == 0:
                        self.logger.warning("最近24小时内没有新数据")
                        return False
                    
                    return True
                else:
                    self.logger.warning("无法获取最近数据信息")
                    return False
                    
        except Exception as e:
            self.logger.error(f"检查最近数据失败: {e}")
            return False
    
    def check_connection_pool(self):
        """检查连接池状态"""
        if not self.engine:
            self.engine = self._create_engine()
            if not self.engine:
                return False
        
        try:
            pool = self.engine.pool
            pool_status = {
                'size': pool.size(),
                'checked_in': pool.checkedin(),
                'checked_out': pool.checkedout(),
                'overflow': pool.overflow(),
                'invalid': pool.invalid()
            }
            
            self.logger.info(f"连接池状态: {pool_status}")
            
            # 检查是否有异常情况
            if pool_status['invalid'] > 0:
                self.logger.warning(f"发现无效连接: {pool_status['invalid']}")
            
            if pool_status['checked_out'] == pool_status['size'] + pool_status['overflow']:
                self.logger.warning("连接池已满")
            
            return True
            
        except Exception as e:
            self.logger.error(f"检查连接池状态失败: {e}")
            return False
    
    def perform_full_database_check(self):
        """执行完整的数据库检查"""
        self.logger.info("开始执行数据库检查...")
        
        checks = [
            ('数据库连接', self.check_connection),
            ('表存在性', self.check_tables_exist),
            ('数据库大小', self.check_database_size),
            ('最近数据', self.check_recent_data),
            ('连接池状态', self.check_connection_pool)
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
            self.logger.info(f"数据库检查完成，通过率: {success_rate:.1%} ({passed_checks}/{total_checks})")
            return True
        else:
            self.logger.error(f"数据库检查失败，通过率: {success_rate:.1%} ({passed_checks}/{total_checks})")
            return False


# 创建全局实例
_db_checker = DatabaseChecker()

# 导出函数
def check_database_connection():
    """检查数据库连接"""
    return _db_checker.perform_full_database_check()

def check_connection_only():
    """仅检查数据库连接"""
    return _db_checker.check_connection()

def check_tables_exist():
    """检查表是否存在"""
    return _db_checker.check_tables_exist()


if __name__ == '__main__':
    # 测试数据库检查
    result = check_database_connection()
    print(f"数据库检查结果: {'通过' if result else '失败'}")