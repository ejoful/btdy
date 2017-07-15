# -*- coding: utf-8 -*-
import scrapy


class BtdySpider(scrapy.Spider):
    name = 'btdy'
    allowed_domains = ['btbtdy.com']
    start_urls = ['http://btbtdy.com/']

    def parse(self, response):
        pass
