# Scrapy settings for scraperr project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os, sys
import django

DJANGO_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(''), '..', '..', '..'))
sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

BOT_NAME = 'scraperr'

SPIDER_MODULES = ['scraperr.spiders']
NEWSPIDER_MODULE = 'scraperr.spiders'

LOG_LEVEL = 'DEBUG'
# LOG_FILE = 'scrapy.log'


ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# SCRAPEOPS_API_KEY = '17ac39eb-1278-4af9-9205-73eeab7112e1'
# EXTENSIONS = {
#     'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
# }
# DOWNLOADER_MIDDLEWARES = {
#     'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
# }

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16



# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'accept': '*/*',
  'accept-encoding': 'gzip, deflate, br', 
  'accept-language': 'en-US,en;q=0.9',
  'cookie': 'session-id=260-4273701-4308428; i18n-prefs=EGP; ubid-acbeg=259-8093131-7307554; lc-acbeg=en_AE; session-id-time=2082787201l; session-token=xQcA5bPfPljgDC5khwGaiWa5a+EeM1UUOg+8TSNPcmugbiUVV89YYg7q4gCisw9XtylPsBOMEl9K9Alb+pVvF4ZqXzuKnJSNSeJIQX63T/B9Cpujx9JMd3V/u3xpHzRiCs8i3+U8c/XKlvW36L/0G5KRhDMF6wk6N3jwH0thgClUhweGiO3gPyJ/9NWnfY+7UWaptuyUe3eLZo3juBzgHgjjc7TN07KT6yiDejt/jKo=; csm-hit=tb:s-ACEMZVGHTGZKW120BE3Z|1683569795324&t:1683569796353&adb:adblk_yes',
  'rtt': '50',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
  'x-requested-with':' XMLHttpRequest'
}

# PROXY_POOL_ENABLED = True
# DOWNLOADER_MIDDLEWARES = {
#     # ...
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 630,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
#     # ...
# }

# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 543,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
# })

# PROXY_POOL_ENABLED = True
# PROXY_POOL_RETRY_TIMES = 10


# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#     'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
# })
# specify the list of user agents to choose from
# USER_AGENT_LIST = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
# ]   

## settings.py

USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

# set the user agent to a random value from the list for each request
RANDOM_UA_PER_REQUEST = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'prisewise.middlewares.PrisewiseDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scraperr.pipelines.ProductPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 15
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
