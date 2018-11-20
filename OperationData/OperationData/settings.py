# -*- coding: utf-8 -*-

# Scrapy settings for OperationData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'OperationData'

SPIDER_MODULES = ['OperationData.spiders']
NEWSPIDER_MODULE = 'OperationData.spiders'


LOG_LEVEL = "DEBUG"
# LOG_LEVEL = "INFO"
# LOG_FILE = "./operation.log"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'OperationData (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.65
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


DOWNLOAD_TIMEOUT = 60

"""禁止重试"""
RETRY_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'OperationData.middlewares.OperationdataSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'OperationData.middlewares.RandomUserAgentMiddlware': 1,
   'OperationData.middlewares.RandomProxyMiddleware': 100
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'OperationData.pipelines.DynamicMysqlPipeline': 300,
   # 'OperationData.pipelines.MysqlPipeline': 300,
}



import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'OperationData'))

RANDOM_UA_TYPE = "random"


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXY = [
"116.149.200.220:6436",
"117.69.230.157:3852",
"118.254.116.143:4283"
]

PROXY_URL = 'http://localhost:7777/random'
# MYSQL_HOST = "47.96.94.94"
# MYSQL_DBNAME = "p2p2"
# MYSQL_USER = "admin"
# MYSQL_PASSWORD = "s@11##!4"

MYSQL_HOST = "xxxxxx"
MYSQL_DBNAME = "xxxxxx"
MYSQL_USER = "xxxxxx"
MYSQL_PASSWORD = "xxxxxx"


MYSQL_HOST_1 = "xxxxxx"
MYSQL_DBNAME_1 = "xxxxxx"
MYSQL_USER_1 = "xxxxxx"
MYSQL_PASSWORD_1 = "xxxxxx"


