# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class neteaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    keywords=scrapy.Field()#关键字
    title=scrapy.Field()   #标题
    content=scrapy.Field() #正文
    link=scrapy.Field()    #链接
    pass
