# Scrapy settings for sports_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'sports_scrapy'

SPIDER_MODULES = ['sports_scrapy.spiders']
NEWSPIDER_MODULE = 'sports_scrapy.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'sports_scrapy.middlewares.SportsScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'sports_scrapy.middlewares.SportsScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'sports_scrapy.pipelines.MySQLPipeline': 100,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 20
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.httpcache.FilesystemCacheStorage'

# MySQL数据库配置
MYSQL_HOST = '43.157.134.155'
MYSQL_PORT = 33070
MYSQL_USER = 'spider_0818'
MYSQL_PASSWORD = '3IQ6fgAQVad0PylSEg.'
MYSQL_DB = 'spider'

# API配置
API_BASE_URL = 'https://stats.fn.sportradar.com/bet365/pt/Asia:Shanghai/gismo'
API_WEB_BASE_URL = 'https://s5.sir.sportradar.com/bet365/pt'
API_LANGUAGE = 'pt'
API_TIMEZONE = 'Asia:Shanghai'
API_SERVICE_ID = '41'
API_CONFIG_ID = '0'

# 体育项目优先级配置
SPORT_PRIORITY = {
                1: 1,   # 足球
                23: 2,   # 排球
                34: 3,   # 沙滩排球
                29: 4,   # 五人制足球
                2: 5,   # 篮球
                117: 6,   # 综合格斗
                5: 7,   # 网球
                16: 8,   # 美式橄榄球
                40: 9,   # 一级方程式
                101: 10,  # 汽车拉力赛
                6: 11, # 手球
                20: 12, # 乒乓球
                31: 13, # 羽毛球
                19: 14, # 桌球
                157: 15 # 沙滩手球
            }

# 重要国家/地区列表
PRIORITY_COUNTRIES = [
    'Brasil',
    'Argentina', 
    'Portugal',
    'Espanha',
    'Inglaterra',
    'França',
    'Alemanha',
    'Itália',
    'Estados Unidos',
    'México'
]

# 采集配置
COLLECTION_CONFIG = {
    'max_retries': 3,
    'timeout': 30,
    'batch_size': 10,
    'enable_logging': True,
    'save_raw_data': True,
    'save_processed_data': True
}

# 错误处理配置
ERROR_CONFIG = {
    'ignore_404': True,
    'ignore_timeout': False,
    'retry_on_error': True,
    'log_errors': True,
    'continue_on_error': True
}

# 数据验证配置
VALIDATION_CONFIG = {
    'validate_json': True,
    'check_required_fields': True,
    'remove_duplicates': True,
    'normalize_data': True
}

# 日志配置
LOG_LEVEL = 'INFO'
# LOG_FILE = 'scrapy_sports.log'  # 注释掉以在终端显示日志
LOG_ENCODING = 'utf-8'

# 并发配置
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 下载超时配置
DOWNLOAD_TIMEOUT = 30

# 输出配置
FEED_EXPORT_ENCODING = 'utf-8'

# 自定义设置
CUSTOM_SETTINGS = {
    'DUPEFILTER_DEBUG': True,
    'SCHEDULER_DEBUG': True,
}
