# -*- coding: utf-8 -*-

# Scrapy settings for esports_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'esports_scrapy'

SPIDER_MODULES = ['esports_scrapy.spiders']
NEWSPIDER_MODULE = 'esports_scrapy.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'esports_scrapy.middlewares.GloboSportsSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'esports_scrapy.middlewares.GloboSportsDownloaderMiddleware': 543,
   'esports_scrapy.middlewares.CustomRetryMiddleware': 550,
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'esports_scrapy.pipelines.GloboSportsPipeline': 300,
    # 'esports_scrapy.pipelines.GloboSportsEpisodePipeline': 400,  # 可选：用于更精细的剧集处理
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 16
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 日志配置
LOG_LEVEL = 'INFO'
# LOG_FILE = 'esports_scrapy.log'
LOG_ENCODING = 'utf-8'

# 数据库配置（从database_config.py导入）
# 这些配置会被pipeline使用
MYSQL_HOST = '43.157.134.155'
MYSQL_PORT = 33070
MYSQL_USER = 'spider_0818'
MYSQL_PASSWORD = '3IQ6fgAQVad0PylSEg.'
MYSQL_DB = 'spider'

# 自定义设置
# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 并发配置
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 超时配置
DOWNLOAD_TIMEOUT = 180

# 内存使用限制
MEMORYUSAGE_ENABLED = True
MEMORYUSAGE_LIMIT_MB = 2048

# 统计收集
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# Feed导出设置（可选）
# FEEDS = {
#     'output.json': {
#         'format': 'json',
#         'encoding': 'utf8',
#         'store_empty': False,
#         'fields': None,
#         'indent': 4,
#     },
# }