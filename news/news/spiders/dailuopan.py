# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class DailuopanSpider(scrapy.Spider):
    name = 'dailuopan'
    allowed_domains = ['dailuopan.com']
    start_urls = ['http://www.dailuopan.com/MParticle?page=1&id_dlp=0']

    def parse(self, response):
        li_list = response.xpath("//div[@class='consensus-list']/ul/li")
        for li in li_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = li.xpath(".//div[@class='hd']/a/text()").extract_first()
            item['postive_score'] = handle_tag(item['title'])
            # item['postive_score'] = 0

            item['update_time'] = li.xpath(".//div[@class='hd']/span/text()").extract_first()
            if item['update_time'] is not None:
                item['news_time'] = datestamptrans(item['update_time'])
            detail_url = li.xpath(".//div[@class='hd']/a/@href").extract_first()
            if detail_url is not None:
                item['href'] = "http://www.dailuopan.com" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = response.meta["item"]
        platform = response.xpath(".//div[@class='f clearfix']/span[@class='source']//text()").extract()
        if len(platform) > 0:
            item['platform'] = ''.join(''.join(platform).split())
        content = response.xpath("string(//div[@class='bd'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item
            # print(item)

