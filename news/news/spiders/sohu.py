# -*- coding: utf-8 -*-
import datetime
import time
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans


class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://v2.sohu.com/public-api/feed?scene=TAG&sceneId=57339&page={}&size=20']

    def start_requests(self):
        for i in range(1, 3):
            yield scrapy.Request(
                self.start_urls[0].format(i),
                callback=self.parse
            )

    def parse(self, response):
        res = json.loads(response.body.decode())
        for rev in res:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = rev['title']
            item['postive_score'] = handle_tag(item['title'])
            dt = rev['publicTime'] / 1000
            time_local = time.localtime(dt)
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            if item['update_time'] is not None:
                item['news_time'] = datestamptrans(item['update_time'])
            item['href'] = rev['originalSource']
            if item['href'] == 'null':
                item['href'] = "http://www.sohu.com/a/" + str(rev['id']) + "_" + str(rev['authorId'])
            if item['href'] is not None:
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        item['platform'] = "搜狐新闻"
        content = response.xpath("string(//article[@id='mp-editor'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item

