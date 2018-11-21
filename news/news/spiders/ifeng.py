# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem

from news.tools.handle import datestamptrans


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://search.ifeng.com/sofeng/search.action?q=p2p&c=1&p=1',
                  "http://search.ifeng.com/sofeng/search.action?q=%E7%BD%91%E8%B4%B7&c=1&p=1"]

    def parse(self, response):
        div_list = response.xpath("//div[@class='mainM']/div[@class='searchResults']")

        for div in div_list:
            item = NewsItem()
            item["href"] = div.xpath("./p/a/@href").extract_first()
            if item["href"] is not None:
                yield scrapy.Request(item["href"],callback=self.parse_detail
                                     ,meta={"item":deepcopy(item)})

        key = re.findall(r"action\?q=(.*)&c=1",response.url)[0]
        for i in range(2,7):
            next_url = "http://search.ifeng.com/sofeng/search.action?q={0}&c=1&p={1}".format(key,i)
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_detail(self,response):

        item = deepcopy(response.meta["item"])
        item["title"] = response.xpath("//div[@class='yc_tit']/h1/text()").extract_first()
        if item["title"] is not None:
            item["postive_score"] = handle_tag(item["title"])
        # if item["title"] is None:
        #     item["title"] = response.xpath("//div[@id='artical']/h1/text()").extract_first()

            item["update_time"] = response.xpath(
                "//div[@class='yc_tit']/p[@class='clearfix']//span/text()").extract_first()
            item["news_time"] = datestamptrans(item["update_time"])
            item["platform"] = "凤凰新闻"
            item["update_date"] = str(datetime.date.today())

            content = response.xpath("//div[@class='yc_con_txt']//p/text()").extract()
            if content is not None and len(content) > 0:
                item["content"] = "".join(("".join(content)).split())
                # print(item)
                yield item

        if item["title"] is None:
            item["update_date"] = str(datetime.date.today())
            item["title"] = response.xpath("//div[@id='artical']/h1/text()").extract_first()
            item["postive_score"] = handle_tag(item["title"])
            item["update_time"] = response.xpath(
                "//div[@id='artical_sth']/p[@class='p_time']/span[1]/text()").extract_first()
            item["news_time"] = datestamptrans(item["update_time"])
            content = response.xpath("//div[@id='main_content']//p/text()").extract()
            item["content"] = "".join(("".join(content)).split())
            item["platform"] = "凤凰新闻"
            item["update_date"] = str(datetime.date.today())

            yield item

            # print(item)


