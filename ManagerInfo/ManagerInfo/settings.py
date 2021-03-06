# -*- coding: utf-8 -*-

# Scrapy settings for ManagerInfo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ManagerInfo'

SPIDER_MODULES = ['ManagerInfo.spiders']
NEWSPIDER_MODULE = 'ManagerInfo.spiders'


LOG_LEVEL = "DEBUG"
# LOG_LEVEL = "INFO"
# LOG_LEVEL = "WARNING"
# LOG_FILE = "./manager.log"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ManagerInfo (+http://www.yourdomain.com)'
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.80
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

COOKIES_ENABLED = False

DOWNLOAD_TIMEOUT = 60

"""禁止重试"""
RETRY_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# SPLASH_URL = 'http://127.0.0.1:8050'

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'ManagerInfo.middlewares.ManagerinfoSpiderMiddleware': 543,
   # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'ManagerInfo.middlewares.RandomUserAgentMiddlware': 1,
   # 'ManagerInfo.middlewares.RandomProxyMiddleware': 100,
   'ManagerInfo.middlewares.ProxyMiddleware': 100,
   # 'scrapy_splash.SplashCookiesMiddleware': 723,
   # 'scrapy_splash.SplashMiddleware': 725,
   # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
#
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    '.scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ManagerInfo.pipelines.DynamicMysqlPipeline': 300,
}


import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'ManagerInfo'))
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
#HTTPCACHE_STORAGE = '.scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXY_URL = "http://172.16.20.242:7777/random"


PROXY = [
"182.113.51.207:4242",
"180.120.166.231:5612",
"115.59.183.42:1246",
"1.28.0.247:4226",
"61.190.160.60:4276"
]

MYSQL_HOST = "xxxxxx"
MYSQL_DBNAME = "xxxxxx"
MYSQL_USER = "xxxxxx"
MYSQL_PASSWORD = "xxxxxx"