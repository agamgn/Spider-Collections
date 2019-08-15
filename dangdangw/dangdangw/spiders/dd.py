# -*- coding: utf-8 -*-
import scrapy
from dangdangw.items import DangdangwItem
from scrapy.http import Request

class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://category.dangdang.com/pg1-cid4008154.html']

    def parse(self, response):
        # 自动爬取，response中是爬取的类容
        item=DangdangwItem()
        
        item['title']=response.xpath("//a[@name='itemlist-title']/text()").extract()
        item['link']=response.xpath("//a[@name='itemlist-title']/@href").extract()
        item['comment']=response.xpath("//a[@name='itemlist-review']/text()").extract()
        item['price']=response.xpath("//span[@class='price_n']/text()").extract()
        # 自动将爬取的数据提交到pipelines中
        print(item['price'])
        yield item

        # for i in range(2,81):
        #     url='http://category.dangdang.com/pg'+str(i)+'-cid4008154.html'
        #     # 依次爬取这个网址，就是使用Request
        #     yield Request(url,self.parse)


