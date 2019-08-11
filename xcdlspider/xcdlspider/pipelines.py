# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class XcdlspiderPipeline(object):

    def __init__(self):
        self.json_file = open("job_positions.json", "wb+")
        self.json_file.write('[\n'.encode("utf-8"))
    def close_spider(self, spider):
        print('----------关闭文件-----------')
        self.json_file.seek(-2, 1)
        self.json_file.write('\n]'.encode("utf-8"))
        self.json_file.close()

    def process_item(self, item, spider):
        print('ip地址:\t',item['IP_address'])
        text = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.json_file.write(text.encode("utf-8"))