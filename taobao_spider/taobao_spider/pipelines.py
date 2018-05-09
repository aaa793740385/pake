# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import pymongo
from scrapy.conf import settings

class TaobaoSpiderPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])     #如果有账户密码
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self, item, spider):
        task_id = item['task_id']
        title = item['title']
        link = item['link']
        price = item['price']
        now_price = item['now_price']
        comment = item['comment'][0]
        address = item['address']

        type = sys.getfilesystemencoding()
        taskId = "任务Id"
        commodityTitle = "商品介绍"
        commodityLink = "商品链接"
        commodityPrice = "商品原价"
        commodityNowPrice = "商品现价"
        commodityAddress = "商品地址"
        commodityComment = "商品数量"

        print taskId.decode('utf-8').encode(type), task_id
        print commodityTitle.decode('utf-8').encode(type), title
        print commodityLink.decode('utf-8').encode(type), link
        print commodityPrice.decode('utf-8').encode(type), price
        print commodityNowPrice.decode('utf-8').encode(type), now_price
        print commodityAddress.decode('utf-8').encode(type), address
        print commodityComment.decode('utf-8').encode(type), comment
        print '------------------------------\n'
        postItem = dict = {'task_id': task_id,'title': title, 'link': link, 'price': price , 'now_price': now_price, 'address': address, 'comment': comment}
        self.coll.insert(postItem)
        return item
