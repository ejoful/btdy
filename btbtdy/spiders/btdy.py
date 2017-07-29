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

            relative_link = video.xpath('dt/a/@href')[0].extract().encode('utf-8')
            url = 'http://www.btbtdy.com'+relative_link
            btbtdy_item['id'] = re.findall(r"\d+", relative_link)[0]
            btbtdy_item['name'] = video.xpath('dt/a/@title')[0].extract().encode('utf-8')
            des_str = video.xpath("dd/p[@class='des']/text()")[0].extract().encode('utf-8')
            des_arr = des_str.split(' ')
            btbtdy_item['keywords'] = ''
            btbtdy_item['description'] = ''
            btbtdy_item['play_time'] = des_arr[0]
            btbtdy_item['update_time'] = ''
            btbtdy_item['quality'] = ''
            btbtdy_item['type'] = ''
            btbtdy_item['total_count'] = ''
            btbtdy_item['category'] = ''
            btbtdy_item['location'] = ''
            btbtdy_item['language'] = ''
            btbtdy_item['imdb'] = ''
            btbtdy_item['star'] = ''
            btbtdy_item['descr'] = ''
            btbtdy_item['list_pic'] = video.xpath('dt/a/img/@data-src')[0].extract().encode('utf-8')
            btbtdy_item['detail_pic'] = ''
            btbtdy_item['album'] = ''
            btbtdy_item['short_video_url'] = ''
            btbtdy_item['short_video_embed'] = ''
            btbtdy_item['subtitle'] = ''
            btbtdy_item['score'] = video.xpath("dd/p/span/text()")[0].extract().encode('utf-8')
            btbtdy_item['url'] = url
            yield scrapy.Request(url=url, meta={'btbtdy_item': btbtdy_item}, callback=self.parse_detail,
                             dont_filter=True)

    def parse_detail(self, response):
        btbtdy_item = response.meta['btbtdy_item']
        btbtdy_item['keywords'] = response.xpath("//meta[@name='keywords']/@content")[0].extract().encode('utf-8')
        btbtdy_item['description'] = response.xpath("//meta[@name='description']/@content")[0].extract().encode('utf-8')
        detail = response.xpath("//div[@class='vod_intro rt']")
        btbtdy_item['update_time'] = detail.xpath('dl/dd[1]/text()')[0].extract()+':00'
        btbtdy_item['quality'] = detail.xpath('dl/dd[2]/text()')[0].extract().encode('utf-8')
        btbtdy_item['type'] = detail.xpath('dl/dd[3]/a/text()')[0].extract().encode('utf-8')
        if not btbtdy_item['type'].find('电影'):
            total_count_list = btbtdy_item['quality'].split(',')
            btbtdy_item['total_count'] = re.findall(r"\d+", total_count_list[0])[0]
        category_list = detail.xpath('dl/dd[3]/a/text()')[1:].extract()
        btbtdy_item['category'] = ','.join(category_list).encode('utf-8')
        btbtdy_item['location'] = detail.xpath('dl/dd[4]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['language'] = detail.xpath('dl/dd[5]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['imdb'] = detail.xpath('dl/dd[6]/a/text()')[0].extract().encode('utf-8')
        zhuyan_list = detail.xpath('dl/dd[7]/a/text()').extract()
        btbtdy_item['star'] = ','.join(zhuyan_list).encode('utf-8')
        btbtdy_item['descr'] = ''.join(response.xpath("//div[@class='des']/div[@class='c05']/p").extract()).encode('utf-8')
        btbtdy_item['detail_pic'] = response.xpath("//div[@class='vod_img lf']/img/@src")[0].extract()
        bitt_list = response.xpath("//span[@class='bitt']/a")
        if "相关图片" in bitt_list[1].extract().encode('utf-8'):
            btbtdy_item['album'] = bitt_list[1].xpath('@href')[0].extract().encode('utf-8')
        btbtdy_item['short_video_url'] = ''
        btbtdy_item['short_video_embed'] = ''
        if "字幕" in bitt_list[3].extract().encode('utf-8'):
            btbtdy_item['subtitle'] = bitt_list[3].xpath('@href')[0].extract().encode('utf-8')
        btbtdy_item['download'] = []
        tbd = {'trailer': '', 'download_links': []}
        download_list = response.xpath('//div[@class="play"]/div[@class="p_list"]')
        for ditem in download_list[:-2]:
            for uindex, uitem in enumerate(ditem.xpath("ul[@class='p_list_02']/li")):
                dlink = {'film_id': btbtdy_item['id'], 'name': '',
                                 'size': '','format': '', 'number': '',
                                 'type': '', 'position': '', 'url': ''}
                title_list = re.split('\[|\]', uitem.xpath('a/@title')[0].extract().encode('utf-8'))
                format_title = title_list[0].split(' ')
                dlink['name'] = format_title[1]
                dlink['size'] = title_list[1]
                dlink['format'] = format_title[0]
                dlink['number'] = 1
                dlink['type'] = ditem.xpath("h2/text()")[0].extract()[:-4].encode('utf-8')
                dlink['magnet_url'] = ''
                dlink['xiaomi_url'] = ''
                dlink['xunlei_url'] = ''
                dlink['position'] = uindex
                dlink['url'] = 'http://www.btbtdy.com'+uitem.xpath('a/@href')[0].extract().encode('utf-8')
                tbd['download_links'].append(dlink)

        if "预告片" in bitt_list[2].extract().encode('utf-8'):
            link = 'http://www.btbtdy.com'+bitt_list[2].xpath('@href')[0].extract().encode('utf-8')
            tbd['trailer'] = link

        return self.recursive_parse_info(tbd, btbtdy_item)


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
            if len(tbd['download_links']):
                dlink = tbd['download_links'].pop(0)
                yield scrapy.Request(url=dlink['url'],
                                     meta={'tbd':tbd,'dlink':dlink, 'btbtdy_item':btbtdy_item},
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
        btbtdy_item['short_video_url'] = response.xpath("//div[@class='trailer']/span/a/@href")[0].extract().encode('utf-8')
        btbtdy_item['short_video_embed'] = response.xpath("//div[@class='trailer']/embed")[0].extract().encode('utf-8')
        return self.recursive_parse_info(tbd, btbtdy_item)

    def parse_download_link(self, response):
        """
        抓取下载页面
        :param response:
        :return:
        """
        tbd = response.meta['tbd']
        dlink = response.meta['dlink']
        btbtdy_item = response.meta['btbtdy_item']
        dlink['magnet_url'] = response.xpath('//input[@id="text1"]/@value')[0].extract().encode('utf-8')
        dlink['xiaomi_url'] = response.xpath("//td/a[@id='d2r']/@href")[0].extract().encode('utf-8')
        dlink['xunlei_url'] = response.xpath("//td/a[@id='xunlei']/@href")[0].extract().encode('utf-8')
        btbtdy_item['download'].append(dlink)
        return self.recursive_parse_info(tbd, btbtdy_item)




