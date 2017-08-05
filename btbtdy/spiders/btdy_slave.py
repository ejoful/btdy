# -*- coding: utf-8 -*-
import scrapy


class BtdySlaveSpider(scrapy.Spider):
    name = 'btdy_slave'
    allowed_domains = ['btbtdy.com']
    start_urls = ['http://btbtdy.com/']

    def parse(self, response):
        pass
