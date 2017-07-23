# -*- coding: utf-8 -*-
import scrapy
from btbtdy.items import BtbtdyItem


class BtdySpider(scrapy.Spider):
    name = 'btdy'
    allowed_domains = ['btbtdy.com']
    start_urls = ['http://btbtdy.com/']

    def start_requests(self):
        reqs = []
        for i in range(1,260):
            req = scrapy.Request("http://www.btbtdy.com/screen/1-----time-%s.html"%i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        video_list = response.xpath("//div[@class='list_su']")
        video_urls = video_list[0].xpath('dl')

        for video in video_urls[0:]:
            btbtdy_item = BtbtdyItem()

            url =  'http://www.btbtdy.com'+video.xpath('dt/a/@href')[0].extract()
            btbtdy_item['name'] = video.xpath('dt/a/@title')[0].extract()
            des_str = video.xpath("dd/p[@class='des']/text()")[0].extract().encode('utf-8')
            des_arr = des_str.split(' ')
            btbtdy_item['play_time'] = des_arr[0]
            btbtdy_item['update_time'] = ''
            btbtdy_item['quality'] = video.xpath("dt/a/span/text()")[0].extract().encode('utf-8')
            btbtdy_item['type'] = ''
            btbtdy_item['category'] = ''
            btbtdy_item['location'] = ''
            btbtdy_item['language'] = ''
            btbtdy_item['imdb'] = ''
            btbtdy_item['star'] = ''
            btbtdy_item['descr'] = ''
            btbtdy_item['list_pic'] = video.xpath('dt/a/img/@data-src')[0].extract()
            btbtdy_item['detail_pic'] = ''
            btbtdy_item['album'] = ''
            btbtdy_item['short_video'] = ''
            btbtdy_item['subtitle'] = ''
            btbtdy_item['score'] = video.xpath("dd/p/span/text()")[0].extract()
            btbtdy_item['url'] = url
            yield scrapy.Request(url=url, meta={'btbtdy_item': btbtdy_item}, callback=self.parse_detail,
                             dont_filter=True)

    def parse_detail(self, response):
        btbtdy_item = response.meta['btbtdy_item']
        detail =  response.xpath("//div[@class='vod_intro rt']")
        btbtdy_item['update_time'] = detail.xpath('dl/dd[1]/text()')[0].extract()+':00'
        btbtdy_item['type'] = detail.xpath('dl/dd[3]/a/text()')[0].extract().encode('utf-8')
        category_list = detail.xpath('dl/dd[3]/a/text()')[1:].extract()
        btbtdy_item['category'] = ','.join(category_list).encode('utf-8')
        btbtdy_item['location'] = detail.xpath('dl/dd[4]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['language'] = detail.xpath('dl/dd[5]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['imdb'] = detail.xpath('dl/dd[6]/a/text()')[0].extract().encode('utf-8')
        zhuyan_list = detail.xpath('dl/dd[7]/a/text()').extract()
        btbtdy_item['star'] = ','.join(zhuyan_list).encode('utf-8')
        btbtdy_item['descr'] = response.xpath("//div[@class='des']/div[@class='c05']/text()")[0].extract().encode('utf-8')
        btbtdy_item['detail_pic'] = response.xpath("//div[@class='vod_img lf']/img/@src")[0].extract()
        btbtdy_item['album'] = ''
        btbtdy_item['short_video'] = ''
        btbtdy_item['subtitle'] = ''
        bitt_list = response.xpath("//span[@class='bitt']/a")
        if "相关图片" in bitt_list[1].extract().encode('utf-8'):
            btbtdy_item['album'] = bitt_list[1].xpath('@href')[0].extract().encode('utf-8')
        if "字幕" in bitt_list[3].extract().encode('utf-8'):
            btbtdy_item['subtitle'] = bitt_list[3].xpath('@href')[0].extract().encode('utf-8')




        if "预告片" in bitt_list[2].extract().encode('utf-8'):
            link = 'http://www.btbtdy.com'+bitt_list[2].xpath('@href')[0].extract()
            yield scrapy.Request(url=link, meta={'btbtdy_item':btbtdy_item}, callback=self.parse_short_video, dont_filter=True)

    def parse_short_video(self, response):
        btbtdy_item = response.meta['btbtdy_item']
        btbtdy_item['short_video_url'] = response.xpath("//div[@class='trailer']/span/a/@href")[0].extract()
        btbtdy_item['short_video_embed'] = response.xpath("//div[@class='trailer']/embed")[0].extract()
        yield btbtdy_item




