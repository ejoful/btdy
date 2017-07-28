# -*- coding: utf-8 -*-
import re
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
            btbtdy_item['short_video_url'] = ''
            btbtdy_item['short_video_embed'] = ''
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
        btbtdy_item['short_video_url'] = ''
        btbtdy_item['short_video_embed'] = ''
        btbtdy_item['subtitle'] = ''
        bitt_list = response.xpath("//span[@class='bitt']/a")
        if "相关图片" in bitt_list[1].extract().encode('utf-8'):
            btbtdy_item['album'] = bitt_list[1].xpath('@href')[0].extract().encode('utf-8')
        if "字幕" in bitt_list[3].extract().encode('utf-8'):
            btbtdy_item['subtitle'] = bitt_list[3].xpath('@href')[0].extract().encode('utf-8')
        tbd = []
        btbtdy_item['download'] = []
        download_list = response.xpath('//div[@class="play"]/div[@class="p_list"]')
        for ditem in download_list[:-2]:
            download_type = ditem.xpath("h2/text()")[0].extract()[:-4]
            for uitem in ditem.xpath("ul[@class='p_list_02']/li"):
                title_list = re.split('\[|\]', uitem.xpath('a/@title')[0].extract().encode('utf-8'))
                download_name = title_list[0]
                download_size = title_list[1]
                download_type = ''
                download_download_url = ''
                download_position = ''


        if "预告片" in bitt_list[2].extract().encode('utf-8'):
            link = 'http://www.btbtdy.com'+bitt_list[2].xpath('@href')[0].extract()
            yield scrapy.Request(url=link, meta={'btbtdy_item':btbtdy_item}, callback=self.parse_short_video, dont_filter=True)


    def recursive_parse_info(self, tbd, btbtdy_item):
        """
        递归抓取链接
        :param tbd: 字典类型，每个键值对存储了将要被下载的链接
        :param btbtdy_item:
        :return:
        """
        if not tbd:
            yield btbtdy_item
        else:
            if tbd.has_key('trailer'):
                link = tbd.pop('trailer')
                yield scrapy.Request(url=link, meta={'tbd':tbd,'btbtdy_item':btbtdy_item},
                                     callback=self.parse_trailer,
                                     dont_filter=True)
            elif tbd.has_key('download_links'):
                links = tbd.pop('download_links')
                for link in links[0:]:
                    yield scrapy.Request(url=link,
                                     meta={'tbd':tbd,'btbtdy_item': btbtdy_item},
                                     callback=self.parse_download_link,
                                     dont_filter=True)


    def parse_trailer(self, response):
        """
        抓取预告片
        :param response:
        :return:
        """
        tbd = response.meta['tbd']
        btbtdy_item = response.meta['btbtdy_item']
        btbtdy_item['short_video_url'] = response.xpath("//div[@class='trailer']/span/a/@href")[0].extract()
        btbtdy_item['short_video_embed'] = response.xpath("//div[@class='trailer']/embed")[0].extract()
        return self.recursive_parse_info(tbd, btbtdy_item)

    def parse_download_link(self, response):
        """
        抓取下载页面
        :param response:
        :return:
        """
        tbd = response.meta['tbd']
        btbtdy_item = response.meta['btbtdy_item']
        btbtdy_item['short_video_url'] = response.xpath("//div[@class='trailer']/span/a/@href")[0].extract()
        btbtdy_item['short_video_embed'] = response.xpath("//div[@class='trailer']/embed")[0].extract()
        return self.recursive_parse_info(tbd, btbtdy_item)




