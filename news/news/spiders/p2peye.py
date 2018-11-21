# -*- coding: utf-8 -*-
import datetime
import time
import json
import re
from copy import deepcopy
import scrapy
from copyheaders import headers_raw_to_dict
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class P2peyeSpider(scrapy.Spider):
    name = 'p2peye'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://news.p2peye.com/wdxw/']

    def parse(self, response):
        div_list = response.xpath("//div[@class='mod-listbox active']/div[@class='mod-leftfixed mod-news clearfix']")
        for div in div_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = div.xpath(".//div[@class='hd']/a/text()").extract_first()
            item['postive_score'] = handle_tag(item['title'])
            item['platform'] = div.xpath(".//div[@class='fd-left']/span[1]/a/text()").extract_first()
            item['update_time'] = div.xpath(".//div[@class='fd-left']/span[3]/text()").extract_first()
            if item['update_time'] is not None:
                item['news_time'] = datestamptrans(item['update_time'])
            detail_url = div.xpath(".//div[@class='hd']/a/@href").extract_first()
            if detail_url is not None:
                item['href'] = "https:" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )
        for i in range(2,4):
            next_url = "https://news.p2peye.com/wdxw/{}.html".format(i)
            yield scrapy.Request(next_url,callback=self.parse)


    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        content = response.xpath("string(//td[@id='article_content'])").extract()
        if content is not None:
            item['content'] = ''.join(''.join(content).split())
            yield item
