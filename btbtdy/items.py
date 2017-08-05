# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Btdy_masterItem(scrapy.Item):
    id = scrapy.Field()




class BtbtdyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # start tbl_film
    id = scrapy.Field()
    name = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    play_time = scrapy.Field()
    update_time = scrapy.Field()
    quality = scrapy.Field()
    type = scrapy.Field()
    total_count = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    language = scrapy.Field()
    imdb = scrapy.Field()
    star = scrapy.Field()
    descr = scrapy.Field()
    list_pic = scrapy.Field()
    detail_pic = scrapy.Field()
    album = scrapy.Field()
    short_video_title = scrapy.Field()
    short_video_url = scrapy.Field()
    short_video_embed = scrapy.Field()
    subtitle = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    # end tbl_film

    # start tbl_download
    download = scrapy.Field()
    """
    BtbtdyItem['download'] = [
    {'film_id':'','name':'','size':'','format':'','number':'','type':'','magnet_url':'','xiaomi_url':'','xunlei_url':'','position':'','url':''},
    {'film_id':'','name':'','size':'','format':'','number':'','type':'','magnet_url':'','xiaomi_url':'','xunlei_url':'','position':'','url':''},
    ...
                             ]
    film_id = film id
    name = film name
    size = film size
    format = film format, hdrip,btray
    number = film number
    type = 720p 1080p
    magnet_url = magnet url
    xiaomi_url = xiaomi route url
    xunlei_url = xunlei url
    position = position
    url = download page link
    """




    # end tbl_download

