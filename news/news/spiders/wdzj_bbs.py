# -*- coding: utf-8 -*-
import datetime
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class WdzjBbsSpider(scrapy.Spider):
    name = 'wdzj_bbs'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://bbs.wdzj.com/topic-6-1.html?type=1']

    def parse(self, response):
        li_list = response.xpath("//div[@class='list-theme bbs-current']/ul/li")
        for li in li_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = li.xpath(".//div[@class='theme-txt fleft']/a/h3/span/text()").extract_first()
            if item['title'] is not None:
                item['title'] = ''.join(item['title'].split())
                item['postive_score'] = handle_tag(item['title'])
            item['update_time'] = li.xpath(".//div[@class='theme-lf fleft']/span/a/text()").extract_first()
            if item['update_time'] is not None:
                item['update_time'] = ''.join(item['update_time'].split())
                item['news_time'] = datestamptrans(item['update_time'])
            item['platform'] = response.xpath(".//div[@class='theme-lf fleft']/a/text()").extract_first()
            if item['platform'] is not None:
                item['platform'] = ''.join(''.join(item['platform']).split())
            item['href'] = li.xpath(".//div[@class='theme-txt fleft']/a/@href").extract_first()
            if item['href'] is not None:
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        content_str = response.xpath("string(//div[@class='news_con_p'])").extract()
        if len(content_str) > 0:
            content_str = ''.join(''.join(content_str).split())
            a_str = re.sub(r'全网爆雷平台汇总（最新）.*?详细内容点上面链接！', '', content_str)
            item['content'] = re.sub(r'PS：.*?【提前30天预知平台风险】的方法', '', a_str)
            yield item

