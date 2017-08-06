# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from btbtdy.utils.InsertRedis import insert

class BtdyMasterSpider(RedisSpider):
    name = 'btdy_master'
    # redis_key = 'btbtdy:start_urls'

    def start_requests(self):
        reqs = []
        for i in range(1,313):
            req = scrapy.Request("http://www.btbtdy.com/screen/0-----time-%s.html"%i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        video_li = response.xpath("//div[@class='list_su']/ul/li")
        for video in video_li[0:]:
            relative_link = video.xpath('div/a[@class="pic_link"]/@href')[
                0].extract().encode('utf-8')
            detail_link = 'http://www.btbtdy.com' + relative_link
            insert("detail_links", detail_link)
            print '[success] the detail link ' + detail_link + ' is insert into the redis queue'

