# _*_ encoding:utf-8_*_
from bson import ObjectId
from pymongo import MongoClient
import pymongo
from pyecharts import Bar
import pymongo as pm
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MongoOperator:
    def __init__(self, host, port, db_name, default_collection):
        '''
        设置mongodb的地址，端口以及默认访问的集合，后续访问中如果不指定collection，则访问这个默认的
        :param host: 地址
        :param port: 端口
        :param db_name: 数据库名字
        :param default_collection: 默认的集合
        '''
        #建立数据库连接
        self.client = pm.MongoClient(host=host, port=port)
        #选择相应的数据库名称
        self.db = self.client.get_database(db_name)
        #设置默认的集合
        self.collection = self.db.get_collection(default_collection)

    def insert(self, item, collection_name =None):
        '''
        插入数据，这里的数据可以是一个，也可以是多个
        :param item: 需要插入的数据
        :param collection_name:  可选，需要访问哪个集合
        :return:
        '''
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            collection.insert(item)
        else:
            self.collection.insert(item)

    def find(self, expression =None, collection_name=None):
        '''
        进行简单查询，可以指定条件和集合
        :param expression: 查询条件，可以为空
        :param collection_name: 集合名称
        :return: 所有结果
        '''
        if collection_name != None:
            collection = self.db.get_collection(self.db)
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)

    def get_collection(self, collection_name=None):
        '''
        很多时候单纯的查询不能够通过这个类封装的方法执行，这时候就可以直接获取到对应的collection进行操作
        :param collection_name: 集合名称
        :return: collection
        '''
        if collection_name == None:
            return self.collection
        else:
            return self.get_collection(collection_name)

db = MongoOperator('127.0.0.1',27017,'crawlData','taobao')
item = {}
x = []
count = 0
#print db.find()
#item = {u'\u5546\u54c1\u539f\u4ef7': u'6999.00 - 15899.00', u'\u5546\u54c1\u6807\u9898': u'MSI\u5fae\u661fi7\u5ba2\u5385\u8ff7\u4f60\u7535\u8111\u6d77\u7687\u621fTrident3 GTX1060/1070\u5403\u9e21\u6e38\u620f\u4e3b\u673a', u'\u5546\u54c1\u73b0\u4ef7': u'5699.00', u'\u5546\u5bb6\u5730\u5740': u'\u4e0a\u6d77', u'\u5546\u54c1\u94fe\u63a5': u'https://item.taobao.com/item.htm?id=553111145635', u'_id': ObjectId('5ac5aae9fb6dec0874973ddc'), u'\u8bc4\u8bba\u6570\u91cf': u'209'}
# -----------------定制范围表格
# #print item
# #print item[u'商品原价']
# for item in db.find():#dict类型，key:value类型
#     count += 1
#     #print item
#     #print #到时候直接调用这里的方法即可，可以显示出商品的价格
#     x.append(item[u'商品现价'])
#     if count == 6:
#         break
#
# #print count
# print x
#
# bar = Bar("我的第一个图表", "这里是副标题")
# bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], x,is_more_utils=True)
# bar.show_config()
# bar.render()


