# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter

import logging
from twisted.enterprise import adbapi
import MySQLdb.cursors

class BtbtdyPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.first_item = True

    def process_item(self, item, spider):
        if self.first_item:
            self.first_item = False
            file = open('%s_items.json' % spider.name, 'wb')
            # scrapy 使用item export输出中文到json文件，内容为unicode码，如何输出为中文？
            # http://stackoverflow.com/questions/18337407/saving-utf-8-texts-in-json-dumps-as-utf8-not-as-u-escape-sequence
            # 里面有提到，将 JSONEncoder 的 ensure_ascii 参数设为 False 即可。
            # 因此就在调用 scrapy.contrib.exporter.JsonItemExporter 的时候额外指定 ensure_ascii=False 就可以啦。
            self.exporters = JsonItemExporter(file, ensure_ascii=False)
            self.exporters.start_exporting()
        self.exporters.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporters.finish_exporting()
        self.file.close()


class MysqlPipeline(object):

    def __init__(self):

        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb',
            db='new_btbtdy1',
            host='10.1.194.229',
            user='root',
            passwd='',
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
            use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        # create recode if doesn't exist.
        # all this block run on it's own thread

        tx.execute("select * from `tbl_film` where `id` = %s" % (item['id']))
        result = tx.fetchone()
        if result:
            logging.log(logging.DEBUG, "Item already stored in db: %s" % (item['id']))
        else:
            sql = """INSERT INTO `tbl_film` (
`id`,`name`,`keywords`, `description`,`play_time`,`update_time`,
`quality`,`type`,`total_count`,`category`,`location`,`language`,
`imdb`,`star`,`descr`,`list_pic`,`detail_pic`,`album`,
`short_video_url`, `short_video_embed`, `subtitle`,`score`,`url`) VALUES (
 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
 %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            lis = (
                    item['id'],item['name'], item['keywords'], item['description'],item['play_time'],item['update_time'],
                    item['quality'], item['type'], item['total_count'], item['category'],item['location'], item['language'],
                    item['imdb'], item['star'], item['descr'],item['list_pic'], item['detail_pic'], item['album'],
                    item['short_video_url'], item['short_video_embed'],item['subtitle'], item['score'], item['url'])
            tx.execute(sql,lis)

        for le in item['download']:
            tx.execute("select * from `tbl_download` where `url` = '%s'" % (le['url']))
            result = tx.fetchone()
            if result:
                logging.log(logging.DEBUG, "Item already stored in db: %s" % (le['url']))
            else:
                sql = """INSERT INTO `tbl_download` (
`film_id`,`name`,`size`,`format`,`number`,`type`,
`magnet_url`,`xiaomi_url`,`xunlei_url`,`position`,`url`) 
VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s)"""
                download = (le['film_id'], le['name'], le['size'], le['format'],
                            le['number'], le['type'],
                            le['magnet_url'], le['xiaomi_url'],
                            le['xunlei_url'], le['position'], le['url'])
                tx.execute(sql, download)

    def handle_error(self, e):
        logging.log(logging.WARNING, e)
