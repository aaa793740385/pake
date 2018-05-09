# -*- coding: utf-8 -*-
import redis
import re
import urllib
import json
import random
from pymongo import MongoClient

from taobao_spider.items import TaobaoSpiderItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
class TaobaoSpider(RedisSpider):
    name = 'taobao'
    redis_key = 'Taobao:start_urls'
    defaultencoding = 'utf-8'
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
    ]

    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.save_cookie
    cookies = db.taobao_cookies
    list = []
    for i in cookies.find({}, {'cookie': 1, "_id": 0}):
        a = json.dumps(i)
        b = json.loads(a)['cookie']
        list.append(b)
    cookie = eval(list[random.randrange(0, int(len(list)))])
    print cookie

    def parse(self, response):
        #body这里用utf-8进行解码，否则就会出现乱码
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'Connection': 'Keep-Alive',
            'Referer': response.url,
            'User-Agent': random.choice(self.USER_AGENTS)
        }
        task_id="none"
        body = response.body.decode('utf-8', 'ignore')
        try:
            r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        except:
            print  '连接redis失败'
        else:
            url=urllib.unquote_plus(response.url)
            task_id=r.get(url)
            r.delete(url)
        #点评的名称
        pat_id = '"nid":"(.*?)"'
        pat_now_price = '"view_price":"(.*?)"' #匹配出来的是商品的当前价格
        pat_address = '"item_loc":"(.*?)"'      #匹配出来的是商家的地址

        all_id = re.compile(pat_id).findall(body) #匹配出来的是商品id
        all_now_price = re.compile(pat_now_price).findall(body)
        all_address = re.compile(pat_address).findall(body)
        for i in range(0,len(all_id)):
            this_id = all_id[i]
            now_price = all_now_price[i]
            address = all_address[i]
            if address == u'北京' or address == u'上海' or address == u'重庆' or address == u'天津' or address == u'日本':
                address = address
            else:
                address = address.split(' ')[1]

            #得到改id的店铺的url，然后再回调，进入该店铺进行爬取信息
            url = "https://item.taobao.com/item.htm?id=" + str(this_id)
            if r.sismember('url' + task_id, this_id) == 0:
                r.sadd('url' + task_id, this_id)
            else:
                continue
            #回调Request访问该url，并且进入next的这个函数
            yield Request(url=url, callback=self.next, meta={'now_price': now_price, 'address': address, 'task_id':task_id},headers=header,cookies=self.cookie,dont_filter = True)
            pass
        pass

    def next(self, response):
        #items中定义过一些结构性的语句，items相当于容易储存这些数据
        item = TaobaoSpiderItem()
        url = response.url
        pat_url = "https://(.*?).com"
        #找出匹进行配出来这个url的信息，进行判断是天猫的还是淘宝的
        web = re.compile(pat_url).findall(url)

        if web[0] != 'item.taobao':     #xiao bug
            #用xpath的方法进行匹配
            title = response.xpath("//meta[@name='keywords']/@content").extract()[0]  # 获取商品名称
            price =  response.meta['now_price']    #获取商品的当前价格
            pat_id = 'id=(.*?)$'
            this_id = re.compile(pat_id).findall(url)[0]
            pass
        else:
            title = response.xpath("//h3[@class='tb-main-title']/@data-title").extract()[0]  # 获取商品名称
            price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract()[0]  # 获取商品原价格
            pat_id = 'id=(.*?)$'
            this_id = re.compile(pat_id).findall(url)[0]
            pass

        #因为评论是Ajax异步加载，通过抓包分析
        #抓取评论总数
        #print price
        comment_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=' + str(this_id)
        comment_data = urllib.urlopen(comment_url).read()
        each_comment = '"rateTotal":(.*?)}'
        comment = re.compile(each_comment).findall(comment_data)

        #print comment       #得出评论数
        item['title'] = title
        item['link'] = url
        item['price'] = price
        item['now_price'] = response.meta['now_price']
        item['comment'] = comment
        item['address'] = response.meta['address']
        item['task_id'] = response.meta['task_id']
        #回调
        yield item

