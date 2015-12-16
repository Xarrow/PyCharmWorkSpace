__author__ = 'zhangjian5'

import scrapy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class FSpider(scrapy.spiders.Spider):
    name = "run"
    start_urls = []
