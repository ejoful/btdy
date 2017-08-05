# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy

class BtdyMasterSpider(RedisSpider):
    name = 'btdy_master'
    redis_key = 'btbtdy:start_urls'

    def parse(self, response):
        next_links = response.xpath()
