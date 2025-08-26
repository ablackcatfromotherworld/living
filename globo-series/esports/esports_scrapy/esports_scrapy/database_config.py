# -*- coding: utf-8 -*-
"""
数据库配置模块
提供数据库连接配置和URL生成功能
"""

class Config:
    """
    数据库配置类
    """
    # MySQL配置
    MYSQL = {
        'host': '43.157.134.155',
        'port': 33070,
        'user': 'spider_0818',
        'password': '3IQ6fgAQVad0PylSEg.',
        'db': 'spider',
        'charset': 'utf8mb4'
    }
    
    @classmethod
    def get_database_url(cls, db_type='mysql'):
        """
        获取数据库URL
        :param db_type: 数据库类型，目前支持mysql
        :return: 数据库连接URL
        """
        if db_type.lower() == 'mysql':
            config = cls.MYSQL
            return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['db']}?charset={config['charset']}"
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")