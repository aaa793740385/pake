# -*- coding: utf-8 -*-

import random
import os
from util.GetProxyIp import GetIps

#这是运行scrapy的一个中间键
class ProcyMiddleware():
    global count
    count = 1
    global ellipsis
    ips = []

    def process_request(self,request):
        global count
        global ips
        if count == 1:
            ips = GetIps() #将list类型的ip地址存进来
        elif count % 100 == 0:
            ips = []
            ips = GetIps()
        #随机拼出ip地址
        try:
            num = random.randint(0, len(ips))
            ress = 'http://' + ips[num]
        except:
            pass
        else:
            request.meta['proxy'] = str(ress)
            count += 1
