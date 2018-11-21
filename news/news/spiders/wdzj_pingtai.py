# -*- coding: utf-8 -*-
import datetime
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans


class WdzjPingtaiSpider(scrapy.Spider):
    name = 'wdzj_pingtai'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://www.wdzj.com/news/pingtai/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='listbox']/ul/li")
        for li in li_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            title = li.xpath(".//div[@class='text']/h3/a/text()").extract_first()
            if title is not None:
                item['title'] = "".join(title.split())
                item['postive_score'] = handle_tag(item['title'])
            item['platform'] = li.xpath(".//div[@class='lbox']/span[1]/text()").extract_first()
            a_str = re.findall(r'来源', item['platform'])
            if len(a_str) == 0:
                item['platform'] = "网贷之家"
            else:
                item['platform'] = item['platform'].split('：')[1]
            item['update_time'] = li.xpath(".//div[@class='lbox']/span[2]/text()").extract_first()
            if item['update_time'] is None:
                item['update_time'] = li.xpath(".//div[@class='lbox']/span[1]/text()").extract_first()
            item['news_time'] = datestamptrans(item['update_time'])
            detail_url = li.xpath(".//div[@class='text']/h3/a/@href").extract_first()
            if detail_url is not None:
                item['href'] = "https:" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        content = response.xpath("string(//div[@class='c-cen'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item

