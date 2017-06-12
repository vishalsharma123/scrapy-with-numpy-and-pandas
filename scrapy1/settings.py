# -*- coding: utf-8 -*-

# Scrapy settings for directional_bottomhole project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import datetime
import os
import glob
import getpass
import sys
import configparser
BOT_NAME = 'directional_bottomhole'
current_user = getpass.getuser()
SPIDER_MODULES = ['directional_bottomhole.spiders']
NEWSPIDER_MODULE = 'directional_bottomhole.spiders'





FILES_STORE = '/home/'+current_user+'/foldername/'+str(datetime.date.today())

directory_to_extract_to = '/home/'+current_user+'/foldername/'+str(datetime.date.today())
path_to_zip_file = '/home/'+current_user+'/foldername/'+str(datetime.date.today()) +'/full/'



ITEM_PIPELINES = {
    'directional_bottomhole.pipelines.BottomholePipeline': 10,


     'scrapy.pipelines.files.FilesPipeline': 1
    }


direction_bottomline_url=''
tank_batteries_url = ''

ROBOTSTXT_OBEY = True

directional_bottom_data_array = [
                    'api_10',
                    'api_full',
                    'operator',
                    'well_name',
                    'bh_status',
                    'max_md',
                    'max_tvd',
                    'deviation',
                    'field_code',
                    'field_name',
                    'lattitude',
                    'longitude',
                    'utm_x',
                    'utm_y'
                    ]
tank_batteries_data_array = [
                    'fac_id',
                    'fac_status',
                    'fac_name',
                    'fac_num',
                    'loc_id',
                    'oper_name',
                    'oper_num',
                    'utm_x',
                    'utm_y',
                    'county',
                    'county_API'

                    ]





def filename():

    for filename in glob.glob(os.path.join(directory_to_extract_to, '*.shp')):
        return(filename)


filename()

def filename1():

    for filename1 in glob.glob(os.path.join(directory_to_extract_to, '*.dbf')):
        return(filename1)


filename1()


def filename2():

    for filename1 in glob.glob(os.path.join(directory_to_extract_to, '*.prj')):
        return(filename1)


filename2()

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'directional_bottomhole (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True




# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

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
#    'directional_bottomhole.middlewares.DirectionalBottomholeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'directional_bottomhole.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'directional_bottomhole.pipelines.DirectionalBottomholePipeline': 300,
#}

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
