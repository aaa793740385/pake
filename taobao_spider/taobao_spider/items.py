# -*- coding: utf-8 -*-
#items是添加存储容器的对象
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TaobaoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #容器
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    now_price = scrapy.Field()
    address = scrapy.Field()
    task_id = scrapy.Field()
    pass
