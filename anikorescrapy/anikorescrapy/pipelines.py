# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient  # mongoDB との接続
import datetime
from scrapy.conf import settings


class MongoDBPipeline(object):

    def __init__(self):
        # インスタンス生成時に渡された引数で、変数初期化
        connection = MongoClient(
        	settings['MONGODB_SERVER'],
        	settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
