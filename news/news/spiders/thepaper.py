# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class ThepaperSpider(scrapy.Spider):
    name = 'thepaper'
    allowed_domains = ['thepaper.cn']
    start_urls = [
        'https://www.thepaper.cn/load_index.jsp?nodeids=25434,25436,25433,25438,25435,25437,27234,25485,25432,&topCids=2152029,2151555,2151205&pageidx={}']

    def start_requests(self):
        for i in range(1, 3):
            yield scrapy.Request(
                self.start_urls[0].format(i),
                callback=self.parse
            )

    def parse(self, response):
        div_list = response.xpath("//div[@class='news_li']")
        for div in div_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = div.xpath("./h2/a/text()").extract_first()
            item['postive_score'] = handle_tag(item['title'])
            detail_url = div.xpath("./h2/a/@href").extract_first()
            if detail_url is not None:
                item['href'] = "https://www.thepaper.cn/" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        item['platform'] = response.xpath("//div[@class='news_about']/p[2]/span/text()").extract_first().strip()
        if len(item['platform']) > 0:
            item['platform'] = item['platform'].split("：")[1]
        else:
            item['platform'] = "澎湃新闻"
        update_time = response.xpath("//div[@class='news_about']/p[2]/text()").extract_first()
        if update_time is not None:
            item['update_time'] = update_time.replace('\r', '').replace('\t', '').replace('\n', '')
            item['news_time'] = datestamptrans(item['update_time'])
        content = response.xpath("string(//div[@class='news_txt'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            yield item

