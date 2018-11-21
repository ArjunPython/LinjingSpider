# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import demjson
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class HexunSpider(scrapy.Spider):
    name = 'hexun'
    allowed_domains = ['hexun.com']
    start_urls = ['http://money.hexun.com/2017/home/js/2moredata.js?t=1526001928089']

    def parse(self, response):
        html_str = response.body.decode('gbk')
        data = re.findall(r'TradeTab_JsonData=(.*)', html_str)[0]
        data_list = demjson.decode(data, encoding='utf-8')
        for news in data_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = news['title']
            item['postive_score'] = handle_tag(item['title'])
            item['update_time'] = news['dateInf']
            if item['update_time'] is not None:
                item['news_time'] = datestamptrans(item['update_time'])
            item['href'] = news['titleLink']
            if item['href'] is not None:
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        item['platform'] = response.xpath("//div[@class='tip fl']/a/text()").extract_first()
        if item['platform'] is None:
            item['platform'] = "和讯网"
        content = response.xpath("string(//div[@class='art_contextBox'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item
