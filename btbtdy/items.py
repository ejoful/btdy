# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BtbtdyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # start tbl_film
    name = scrapy.Field()
    play_time = scrapy.Field()
    update_time = scrapy.Field()
    status = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    language = scrapy.Field()
    imdb = scrapy.Field()
    star = scrapy.Field()
    descr = scrapy.Field()
    pic = scrapy.Field()
    album = scrapy.Field()
    short_video = scrapy.Field()
    subtitle = scrapy.Field()
    score = scrapy.Field()
    # end tbl_film
