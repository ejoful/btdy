# -*- coding: utf-8 -*-
import redis


def insert(type, str):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    except:
        print '连接redis失败'
    else:
        if type == 'start_urls':
            r.lpush('btbtdy:start_urls', str)
        elif type == 'detail_links':
            r.lpush('btbtdy:detail_links2', str)