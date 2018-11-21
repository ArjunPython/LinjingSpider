# -*- coding: utf-8 -*-
import datetime
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans



class WangyiSpider(scrapy.Spider):
    name = 'wangyi'
    allowed_domains = ['163.com']
    start_urls = ['http://money.163.com/special/00253368/institutions.html']

    def parse(self, response):
        ul_list = response.xpath("//div[@class='colLM']/ul")
        item = NewsItem()
        for ul in ul_list:
            li_list = ul.xpath("./li")
            for li in li_list:
                item["update_date"] = str(datetime.date.today())
                title = li.xpath("./span[@class='article']/a/text()").extract_first()
                if title is not None:
                    item["title"] = title
                    item['postive_score'] = handle_tag(item['title'])
                item['update_time'] = li.xpath("./span[@class='atime f12px']/text()").extract_first()
                if item['update_time'] is not None:
                    item['update_time'] = item['update_time'][1:-1]
                    item['news_time'] = datestamptrans(item['update_time'])
                item['href'] = li.xpath("./span[@class='article']/a/@href").extract_first()
                if item['href'] is not None:
                    yield scrapy.Request(
                        item['href'],
                        callback=self.detail_parse,
                        meta={"item": deepcopy(item)}
                    )
        # next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        # if next_url != "#":
        #     yield scrapy.Request(
        #         next_url,
        #         callback=self.parse,
        #         meta={"item": deepcopy(item)}
        #     )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        item['platform'] = response.xpath(
            "//div[@class='post_time_source']/a[@id='ne_article_source']/text()").extract_first()
        if item['platform'] is None:
            item['platform'] = "网易财经"
        content = response.xpath("string(//div[@id='endText'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item

