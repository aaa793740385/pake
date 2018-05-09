# -*- coding: utf-8 -*-
import sys
from scrapy_redis.spiders import RedisSpider
from tc_taobao.util.InsertRedis import inserinttota
import redis

defaultencoding = 'utf-8'


class TaobaoSpider(RedisSpider):
    name = 'taobaoMaster'
    redis_key = 'start_urls'
    def parse(self, response):
        try:
            r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        except:
            print  '连接redis失败'
        else:
            taskId = r.lpop('task_id')
            commodity = r.get('general'+taskId)
            r.delete('general'+taskId)
        type = sys.getfilesystemencoding()
        key = commodity.decode('utf-8').encode(type)
        pages = 30

        #通过分析url可以知道，我们可以通过拼接字符串的方法进行访问改页面
        for i in range(0,int(pages)):
            url = "https://s.taobao.com/search?q=" + str(key) + "&s=" + str(44 * i)
            inserinttota(url, 2, taskId)  # lpush到另外一边进行爬虫
            print '[success] the url ' + url + ' is insert into the redis queue'
            #回调的函数
            #是抓取当前url连接，不断执行page，是个递归。意思是没执行一次url就会回调一次page的方法



    # def page(self,response):
    #     #body这里用utf-8进行解码，否则就会出现乱码
    #     body = response.body.decode('utf-8', 'ignore')
    #     #点评的名称
    #     pat_id = '"nid":"(.*?)"'
    #     all_id = re.compile(pat_id).findall(body) #匹配出来的是商品id
    #
    #     for i in range(0,len(all_id)):
    #         this_id = all_id[i]
    #         #得到改id的店铺的url，然后再回调，进入该店铺进行爬取信息
    #         url = "https://item.taobao.com/item.htm?id=" + str(this_id)
    #         if url:
    #             inserinttota(url,2)#lpush到另外一边进行爬虫
    #             print '[success] the url ' + url + ' is insert into the redis queue'




