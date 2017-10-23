# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 处理spider从网页提取的item
class Win4000MeinvItem(scrapy.Item):
    image_urls = scrapy.Field()
    # images = scrapy.Field()
    classify_name = scrapy.Field()
    meinv_name = scrapy.Field()
    # image_path = scrapy.Field()

