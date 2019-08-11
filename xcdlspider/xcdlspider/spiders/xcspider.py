# -*- coding: utf-8 -*-
import scrapy

from xcdlspider.items import XcdlspiderItem


class XcspiderSpider(scrapy.Spider):
    name = 'xcspider'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']  #

    def parse(self, response):
        item = XcdlspiderItem()
        port_cells = response.xpath('//*[@id="ip_list"]/tr')
        for port_cell in port_cells:
            item['IP_address'] = port_cell.xpath('./td[2]/text()').extract()
            item['port'] = port_cell.xpath('./td[3]/text()').extract()
            item['server_address'] = port_cell.xpath('./td[4]/a/text()').extract()
            item['anonymous_sit'] = port_cell.xpath('./td[5]/text()').extract()
            item['Type'] = port_cell.xpath('./td[6]/text()').extract()
            item['speed'] = port_cell.xpath('./td[7]/div/@title').extract()
            item['conect_time'] = port_cell.xpath('./td[8]/div/@title').extract()
            item['alive_time'] = port_cell.xpath('./td[9]/text()').extract()
            item['Ver_time'] = port_cell.xpath('./td[10]/text()').extract()
            yield item

        new_links = response.xpath('//*[@class="next_page"]/@href').extract()
        if new_links and len(new_links) > 0:
            new_link = new_links[0]
            yield scrapy.Request("https://www.xicidaili.com" + new_link, callback=self.parse)
