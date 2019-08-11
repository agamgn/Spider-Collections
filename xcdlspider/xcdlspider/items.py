# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XcdlspiderItem(scrapy.Item):
    #IP节点
    IP_address = scrapy.Field()
    #端口
    port = scrapy.Field()
    #服务器地址
    server_address = scrapy.Field()
    #是否匿名
    anonymous_sit = scrapy.Field()
    #类型
    Type = scrapy.Field()
    #速度
    speed = scrapy.Field()
    #连接时间
    conect_time = scrapy.Field()
    #存活时间
    alive_time = scrapy.Field()
    #验证时间
    Ver_time = scrapy.Field()
