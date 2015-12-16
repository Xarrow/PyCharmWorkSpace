__author__ = 'zhangjian5'
import scrapy
import logging

logging.basicConfig(filename="log.md",format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)

class DmozSpider(scrapy.spiders.Spider):
    name = 'run'
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            logging.info(title)
            logging.info(link)
            logging.info(desc)
