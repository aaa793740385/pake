# -*- coding: utf-8 -*-

import random
import os
from proxy_util import loadIp

#这是运行scrapy的一个中间键
class ProcyMiddleware():
    ips = []
    def process_request(self,request):
        ips = loadIp()
        #随机拼出ip地址
        try:
            num = random.randint(0, len(ips))
            ress = 'http://' + ips[num]
        except:
            pass
        else:
            request.meta['proxy'] = str(ress)

