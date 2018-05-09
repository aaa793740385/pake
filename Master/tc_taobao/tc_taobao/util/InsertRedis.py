# -*- coding: utf-8 -*-

import redis
#from tc_taobao.spiders.tc_taobao_detail import TaobaoSpider
#redis的连接池

def inserinttota(str,type,id):
    try:
        r = redis.Redis(host='127.0.0.1',port=6379,db=0)
    except:
        print  '连接redis失败'
    else:
        if type == 2:
            r.lpush('Taobao:start_urls',str)#向redis输入url
            r.set(str, id)
