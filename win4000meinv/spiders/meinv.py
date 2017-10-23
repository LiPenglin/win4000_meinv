# -*- coding: utf-8 -*-
import scrapy

from win4000meinv.items import Win4000MeinvItem

class MeinvSpider(scrapy.Spider):
    name = "meinv"  # spider的名字
    allowed_domains = ["www.win4000.com"] # 首页
    start_urls = ['http://www.win4000.com/tags_meinv.html'] #包含了Spider在启动时进行爬取的url列表
    # 爬取start_urls中的url
    def parse(self, response):
        for dl in response.css('dl'):
            for dd in dl.css('dd'):
                # item = Win4000MeinvItem()
                # [href*=meinv] -> css3伪选择器
                classify_name = dd.css('a[href*=meinv]::text').extract_first() # 提取第一个
                # item['classify_name'] = classify_name
                classify_url = dd.css('a[href*=meinv]::attr(href)').extract_first() # [一个分类]
                yield scrapy.Request(response.urljoin(classify_url),
                                     callback=self.get_tag,
                                     meta={'classify_name' : classify_name})
    # 爬取tag
    def get_tag(self, response):
        classify_name = response.meta['classify_name']
        for li in response.css('.pic-list>li')[1:-1]:
            meinv_name = li.css('div[class=detail]>p::text').extract_first()
            # [一个美女]
            meinv_url = li.css('span>a[href*=meinv]::attr(href)').extract_first()
            yield scrapy.Request(meinv_url,
                                 callback=self.get_meinv,
                                 meta={'classify_name' : classify_name,
                                       'meinv_name' : meinv_name})
        next_page = response.css('.after::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(next_page,
                                 callback=self.get_tag,
                                 meta={'classify_name' : classify_name})
    # 图片展示页
    def get_meinv(self, response):
        classify_name = response.meta['classify_name']
        meinv_name = response.meta['meinv_name']
        total = int(response.css('.current-num>strong::text').extract_first()[1:].strip())
        for url in [response.url[0:-5]+'_'+str(i)+'.html' for i in range(1,total+1)]:
            yield scrapy.Request(url,
                                 callback=self.parse_img,
                                 meta={'classify_name' : classify_name,
                                       'meinv_name' : meinv_name}) # [一个美女的多张img]
    # 抓取图片src,返回item
    def parse_img(self, response):
        item = Win4000MeinvItem()
        item['classify_name'] = response.meta['classify_name']
        item['meinv_name'] = response.meta['meinv_name']
        item['image_urls'] = response.css('img[class=pic-large]::attr(src)').extract_first()
        return item


