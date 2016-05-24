# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
from scrapy.exceptions import DropItem
class checkPipeline(object):
    min_length=10
    def process_item(self, item, spider):
        if item['keywords'] and item['title'] and len(item['content'])>self.min_length:
            return item
        else:
            raise DropItem("Missing value" % item)
'''
