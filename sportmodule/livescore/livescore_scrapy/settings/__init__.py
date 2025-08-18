# Scrapy settings for livescore_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'livescore_scrapy'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.2
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 32

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'livescore_scrapy.middlewares.LivescoreScrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'livescore_scrapy.middlewares.LivescoreScrapyDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pipelines.database_pipeline.DatabasePipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 数据库配置
DATABASE_URL = 'mysql+pymysql://spiderman:ew4%2598fRpe@43.157.134.155:33070/spider'

# 批处理大小
BATCH_SIZE = 100

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = 'livescore_scrapy.log'

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 下载超时
DOWNLOAD_TIMEOUT = 180

# 内存使用限制
MEMORYUSAGE_ENABLED = True
MEMORYUSAGE_LIMIT_MB = 2048

# 统计收集
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'

# 自定义设置已移除 - 不需要生成JSON文件

# 支持的运动类型
SUPPORTED_SPORTS = [
    'football',     # 足球
    'basketball',   # 篮球
    'tennis',       # 网球
    'hockey',       # 曲棍球
    'baseball',     # 棒球
    'volleyball',   # 排球
    'handball',     # 手球
    'rugby',        # 橄榄球
    'cricket',      # 板球
    'soccer',       # 足球(美式称呼)
]

# 支持的语言
SUPPORTED_LANGUAGES = [
    'en',    # 英语
    'zh',    # 中文
    'es',    # 西班牙语
    'fr',    # 法语
    'de',    # 德语
    'it',    # 意大利语
    'pt',    # 葡萄牙语
    'ru',    # 俄语
    'ja',    # 日语
    'ko',    # 韩语
]

# 比赛状态映射
MATCH_STATUS_MAPPING = {
    # 未开始状态
    'scheduled': '已安排',
    'not_started': '未开始',
    'upcoming': '即将开始',
    'postponed': '推迟',
    'cancelled': '取消',
    'delayed': '延迟',
    
    # 进行中状态
    'live': '进行中',
    'in_progress': '进行中',
    'first_half': '上半场',
    'second_half': '下半场',
    'halftime': '中场休息',
    'overtime': '加时赛',
    'penalty': '点球大战',
    'break': '休息',
    
    # 已结束状态
    'finished': '已结束',
    'full_time': '全场结束',
    'completed': '已完成',
    'final': '最终',
    'ended': '已结束',
    
    # 特殊状态
    'suspended': '暂停',
    'interrupted': '中断',
    'abandoned': '放弃',
    'walkover': '弃权',
    'awarded': '判决',
    'unknown': '未知',
}