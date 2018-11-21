# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy

import scrapy

from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['people.com.cn']
    start_urls = ['http://money.people.com.cn/GB/392426/index1.html']

    def parse(self, response):

        ul_list = response.xpath("//div[@class='p2j_list fl']/ul")

        for ul in ul_list:
            li_list = ul.xpath("./li")
            for li in li_list:
                item = NewsItem()
                item["title"] = li.xpath("./a/text()").extract_first()
                item["postive_score"] = handle_tag(item["title"])
                item["update_date"] = str(datetime.date.today())
                item["href"] = li.xpath("./a/@href").extract_first()
                if item["href"] is not None:
                    item["href"] = "http://money.people.com.cn" + item["href"]
                    yield scrapy.Request(item["href"],callback=self.parse_detail
                                     ,meta={"item":deepcopy(item)})

        url_info = response.xpath(
            "//div[@class='page_n clearfix']/a[contains(text(),'下一页')]/@href").extract_first()
        if url_info is not None:
            next_url = "http://money.people.com.cn/GB/392426/" + url_info
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_detail(self,response):
        item = deepcopy(response.meta["item"])
        update_time = response.xpath(
            "//div[@class='box01']/div[1]/text()").extract_first()
        item["platform"] = response.xpath("//div[@class='box01']/div[1]/a/text()").extract_first()
        if update_time is not None:
            update_time = "".join(update_time.split())
            item["update_time"] =re.findall(r"(.*)来源", update_time)[0]
            item["news_time"] = datestamptrans(item["update_time"])
        content = response.xpath("//div[@class='box_con']//p/text()").extract()
        if content is not None and len(content) > 0:
            item["content"] = "".join(("".join(content)).split())
            yield item
            # print(item)

