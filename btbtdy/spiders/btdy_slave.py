# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from btbtdy.items import BtbtdyItem
import re

class BtdySlaveSpider(RedisSpider):
    name = 'btdy_slave'
    redis_key = 'btbtdy:detail_links'

    def parse(self, response):
        btbtdy_item = BtbtdyItem()
        btbtdy_item['id'] = re.findall(r"\d+", response.url)[0]
        detail = response.xpath("//div[@class='vod_intro rt']")
        btbtdy_item['name'] = detail.xpath("h1/text()")[0].extract().encode('utf-8')
        btbtdy_item['keywords'] = response.xpath("//meta[@name='keywords']/@content")[0].extract().encode('utf-8')
        btbtdy_item['description'] = response.xpath("//meta[@name='description']/@content")[0].extract().encode('utf-8')
        year_str = detail.xpath("h1/span[@class='year']/text()")[0].extract().encode('utf-8')
        btbtdy_item['play_time'] = re.findall(r"\d+", year_str)[0]
        btbtdy_item['update_time'] = detail.xpath('dl/dd[1]/text()')[0].extract()+':00'
        btbtdy_item['quality'] = detail.xpath('dl/dd[2]/text()')[0].extract().encode('utf-8')
        btbtdy_item['type'] = detail.xpath('dl/dd[3]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['total_count'] = 1
        if '电视剧' in btbtdy_item['type']:
            total_count_list = btbtdy_item['quality'].split(',')
            btbtdy_item['total_count'] = re.findall(r"\d+", total_count_list[1])[0]
        category_list = detail.xpath('dl/dd[3]/a/text()')[1:].extract()
        btbtdy_item['category'] = ','.join(category_list).encode('utf-8')
        btbtdy_item['location'] = detail.xpath('dl/dd[4]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['language'] = detail.xpath('dl/dd[5]/a/text()')[0].extract().encode('utf-8')
        btbtdy_item['imdb'] = ''
        if detail.xpath('dl/dd[6]/a/text()'):
            btbtdy_item['imdb'] = detail.xpath('dl/dd[6]/a/text()')[0].extract().encode('utf-8')
        zhuyan_list = detail.xpath('dl/dd[7]/a/text()').extract()
        btbtdy_item['star'] = ','.join(zhuyan_list).encode('utf-8')
        btbtdy_item['descr'] = ''.join(response.xpath("//div[@class='des']/div[@class='c05']/p").extract()).encode('utf-8')
        detail_pic = response.xpath("//div[@class='vod_img lf']/img/@src")[0].extract().encode('utf-8')
        btbtdy_item['list_pic'] = detail_pic.split('?')[0]+'?h=190'
        btbtdy_item['detail_pic'] = response.xpath("//div[@class='vod_img lf']/img/@src")[0].extract().encode('utf-8')
        bitt_list = response.xpath("//span[@class='bitt']/a")
        btbtdy_item['album'] = ''
        if "相关图片" in bitt_list[1].extract().encode('utf-8'):
            btbtdy_item['album'] = bitt_list[1].xpath('@href')[0].extract().encode('utf-8')
        btbtdy_item['short_video_url'] = ''
        btbtdy_item['short_video_embed'] = ''
        btbtdy_item['subtitle'] = ''
        if "字幕" in bitt_list[3].extract().encode('utf-8'):
            btbtdy_item['subtitle'] = bitt_list[3].xpath('@href')[0].extract().encode('utf-8')
        btbtdy_item['score'] = 1.0
        btbtdy_item['url'] = response.url
        btbtdy_item['download'] = []
        tbd = {'download_links':[]}

        download_list = response.xpath('//div[@id="nucms_downlist"]/div[@class="p_list"]')
        testditem = download_list[0]
        testuitem = testditem.xpath("ul[@class='p_list_02']/li")
        for dindex, ditem in enumerate(download_list):
            for uindex, uitem in enumerate(ditem.xpath("ul[@class='p_list_02']/li")):
                dlink = {'film_id': btbtdy_item['id'], 'name': '',
                                 'size': '','format': '', 'number': '',
                                 'type': '', 'position': '', 'url': ''}
                title_list = re.split('\[|\]', uitem.xpath('a/@title')[0].extract().encode('utf-8'))
                format_title = title_list[0].split(' ')
                if len(title_list) == 3:
                    dlink['size'] = title_list[1]
                if len(format_title) >= 2:
                    dlink['name'] = ' '.join(format_title[1:])
                    dlink['format'] = format_title[0]
                else:
                    dlink['name'] = format_title[0]
                dlink['number'] = 1
                dlink['type'] = ditem.xpath("h2/text()")[0].extract()[:-4].encode('utf-8')
                dlink['ed2k_url'] = ''
                dlink['magnet_url'] = ''
                dlink['xiaomi_url'] = ''
                dlink['xunlei_url'] = ''
                dlink['position'] = uindex
                # print(btbtdy_item['url'])
                # print(uitem.xpath('a/@href')[0].extract().encode('utf-8'))
                dlink['url'] = 'http://www.btbtdy.com/down/'+str(btbtdy_item['id'])+'-'+str(dindex)+'-'+str(uindex)+'.html'
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
        # if not tbd:
        #     print(btbtdy_item)
        #     yield btbtdy_item
        # else:
        if tbd.has_key('trailer'):
            link = tbd.pop('trailer')
            yield scrapy.Request(url=link, meta={'tbd':tbd,'btbtdy_item':btbtdy_item},
                                 callback=self.parse_trailer,
                                 dont_filter=True)
        if len(tbd['download_links']) == 0:
            tbd.pop('download_links')
            # print(btbtdy_item['url'])
        else:
            dlink = tbd['download_links'].pop(0)
            yield scrapy.Request(url=dlink['url'],
                                 meta={'tbd':tbd,'dlink':dlink, 'btbtdy_item':btbtdy_item},
                                 callback=self.parse_download_link,
                                 dont_filter=True)
        yield btbtdy_item

    def parse_trailer(self, response):
        """
        抓取预告片
        :param response:
        :return:
        """
        tbd = response.meta['tbd']
        btbtdy_item = response.meta['btbtdy_item']
        btbtdy_item['short_video_title'] = response.xpath("//div[@class='trailer']/span/a/text()")[0].extract().encode('utf-8')
        btbtdy_item['short_video_url'] = response.xpath("//div[@class='trailer']/span/a/@href")[0].extract().encode('utf-8')
        if response.xpath("//div[@class='topur']/embed"):
            btbtdy_item['short_video_embed'] = response.xpath("//div[@class='topur']/embed")[0].extract().encode('utf-8')
        elif response.xpath("//div[@class='topur']/iframe"):
            btbtdy_item['short_video_embed'] = response.xpath("//div[@class='topur']/iframe")[0].extract().encode('utf-8')
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
        if response.xpath('//input[@id="text1"]/@value'):
            # 磁力 link
            dlink['magnet_url'] = response.xpath('//input[@id="text1"]/@value')[0].extract().encode('utf-8')
        if response.xpath("//td/a[@id='d2r']/@href"):
            dlink['xiaomi_url'] = response.xpath("//td/a[@id='d2r']/@href")[0].extract().encode('utf-8')
        if response.xpath("//td/a[@id='xunlei']/@href"):
            dlink['xunlei_url'] = response.xpath("//td/a[@id='xunlei']/@href")[0].extract().encode('utf-8')
        for tditem in response.xpath("//forum[@id='form2']/table/tr/td"):
            item = tditem.xpath("a/@href")
            if item and item[0].extract().encode('utf-8').find('ed2k:') != -1:
                dlink['ed2k_url'] = item[0].extract().encode('utf-8')
        btbtdy_item['download'].append(dlink)
        return self.recursive_parse_info(tbd, btbtdy_item)
