# -*- coding: utf-8 -*-

import redis
import sys


#redis的连接池
def inserintotc(url,type,task):
    # print type
    try:
        r = redis.Redis(host='127.0.0.1',port=6379,db=0)
    except:
        print  '连接redis失败'
    else:
        if type == 1:
            r.lpush('start_urls',url)
            r.lpush('task_id',task.id )
            r.set('general' + str(task.id), str(task.general))
            pass
        pass
    pass

