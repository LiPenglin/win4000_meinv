# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid

import pymongo
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class Win4000MeinvPipeline(ImagesPipeline):

    #重写ImagesPipeline   get_media_requests方法
    def get_media_requests(self, item, info):
        # 得到图片的URL并从项目中下载
        yield scrapy.Request(item['image_urls'], meta={'item' : item})
    #重写ImagesPipeline   item_completed方法
    def item_completed(self, results, item, info):
        # 一个单独项目中的所有图片请求完成时,该方法被调用
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
    # 重写ImagesPipeline   file_path方法
    def file_path(self, request, response=None, info=None):
        # 设置自己的path
        item = request.meta['item']
        image_uuid = str(uuid.uuid1()).replace('-','')
        image_name = 'full/{0[classify_name]}/{0[meinv_name]}/{1}'.format(item, image_uuid)
        item['image_path'] = image_name
        return image_name

class MongoPipeline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    # 从settings里面拿出来一些配置信息
    @classmethod
    def from_crawler(cls, crawler):
        # cls是type的实例, self是cls的实例
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    # 爬虫刚要启动的时候进行的一些操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    # 插入
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    # close
    def close_spider(self, spider):
        self.client.close()



