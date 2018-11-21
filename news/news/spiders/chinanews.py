# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans


class ChinanewsSpider(scrapy.Spider):
    name = 'chinanews'
    allowed_domains = ['chinanews.com']
    # start_urls = ['http://chinanews.com/']
    keys = ["p2p", "网贷"]

    def start_requests(self):
        url = "http://sou.chinanews.com/search.do"
        for key in self.keys:
            # for page in range(20):
            #     data = dict(
            #         q=key,
            #         ps="10",
            #         start=str(page *10),
            #         type="",
            #         sort="pubtime",
            #         time_scope="0",
            #         channel="all",
            #         adv="1",
            #         day1="",
            #         day2="",
            #         field="",
            #         creator=""
            #     )

            data = dict(
                field="content",
                q=key,
                ps="10",
                adv="1",
                time_scope="7",
                day1="",
                day2="",
                channel="all",
                creator="",
                sort="pubtime"
            )
            yield scrapy.FormRequest(url,formdata=data,callback=self.parse)

    def parse(self, response):

        table_list = response.xpath("//div[@id='news_list']/table")

        for table in table_list:
            item = NewsItem()
            item["title"] = table.xpath("./tr[1]//li[@class='news_title']/a/text()").extract_first()
            item["postive_score"] = handle_tag(item["title"])
            item["href"] = table.xpath("./tr[1]//li[@class='news_title']/a/@href").extract_first()
            yield scrapy.Request(item["href"],callback=self.parse_detail,
                                        meta={"item": deepcopy(item)})

    def parse_detail(self,response):
        item = deepcopy(response.meta["item"])
        item["update_date"] = str(datetime.date.today())
        update_time = response.xpath("//div[@class='left-t']/text()").extract_first()
        if update_time is not None:
            update_time = "".join(update_time.split())
            item["update_time"] = re.findall(r"(.*)来源", update_time)[0]
            item["news_time"] = datestamptrans(item["update_time"])
            item["platform"] = re.findall(r"来源：(.*)", update_time)[0]
            if len(item["platform"]) == 0:
                item["platform"] = "中国新闻网"
            # print(item["platform"])
        content = response.xpath("//div[@class='left_zw']//p/text()").extract()
        if content is not None and len(content) > 0:
            item["content"] = "".join(("".join(content)).split())
            yield item
            # print(item)

