# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DangdangwPipeline(object):

    def process_item(self, item, spider):
        coon=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='916149',db='dd')
        cursors = coon.cursor()

        for i in range(0,len(item['title'])):
            title=item['title'][i]
            link=item['link'][i]
            comment=item['comment'][i]
            price=item['price'][i]
            sql="insert into goods(title,link,comment,price) values('"+title+"','"+link+"','"+comment+"','"+price+"')"
            try:
                cursors.execute(sql)
            except Exception as err:
                print(err)

        coon.close()
        return item
