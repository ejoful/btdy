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
    keywords = scrapy.Field()
    description = scrapy.Field()
    play_time = scrapy.Field()
    update_time = scrapy.Field()
    quality = scrapy.Field()
    type = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    language = scrapy.Field()
    imdb = scrapy.Field()
    star = scrapy.Field()
    descr = scrapy.Field()
    list_pic = scrapy.Field()
    detail_pic = scrapy.Field()
    album = scrapy.Field()
    short_video_url = scrapy.Field()
    short_video_embed = scrapy.Field()
    subtitle = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field()
    # end tbl_film

    # start tbl_download
    film_id = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    type = scrapy.Field()
    download_url = scrapy.Field()
    position = scrapy.Field()
    url = scrapy.Field()



    # end tbl_download

