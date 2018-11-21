# -*- coding: utf-8 -*-
import datetime
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans



class WangdaiyujingSpider(scrapy.Spider):
    name = 'wangdaiyujing'
    allowed_domains = ['wangdaiyujing.com']
    start_urls = ['http://www.wangdaiyujing.com/forum-36-{}.html']

    def start_requests(self):
        for i in range(1, 3):
            yield scrapy.Request(
                self.start_urls[0].format(i),
                callback=self.parse,
            )

    def parse(self, response):
        tbody_list = response.xpath("//table[@id='threadlisttableid']/tbody[contains(@id,'normalthread')]")
        for tbody in tbody_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = tbody.xpath("./tr/th/a[@class='s xst']/text()").extract_first()
            item['platform'] = "网贷预警平台曝光"
            item['postive_score'] = 0
            item['update_time'] = tbody.xpath(".//div[@class='foruminfo']/i/span/text()").extract_first()
            if item['update_time'] is not None:
                item['update_time'] = item['update_time'].replace('@', '').strip()
                item['news_time'] = datestamptrans(item['update_time'])
            detail_url = tbody.xpath("./tr/th/a[@class='s xst']/@href").extract_first()
            if detail_url is not None:
                item['href'] = "http://www.wangdaiyujing.com" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        content = response.xpath("string(//td[@class='t_f'])").extract()
        if content is not None:
            item['content'] = ''.join(''.join(content).split())
            yield item

