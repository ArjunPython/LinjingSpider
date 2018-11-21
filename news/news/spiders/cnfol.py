# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans

class CnfolSpider(scrapy.Spider):
    name = 'cnfol'
    allowed_domains = ['cnfol.com']
    start_urls = ["http://so.cnfol.com/cse/search?q=p2p&p=0&s=12596448179979580087&srt=lds&nsid=1",
                  "http://so.cnfol.com/cse/search?q=%E7%BD%91%E8%B4%B7&p=0&s=12596448179979580087&srt=lds&sti=10080&nsid=0"]

    def parse(self, response):
        div_list = response.xpath("//div[@id='results']/div")

        for div in div_list:
            item = NewsItem()
            item["href"] = div.xpath("./h3/a/@href").extract_first()
            if item["href"] is not None:
                yield scrapy.Request(item["href"],callback=self.parse_detail
                                     ,meta={"item":deepcopy(item)})
        # url_info = response.xpath(
        #         "//div[@id='pageFooter']/a[contains(text(),'下一页')]/@href").extract_first()
        url_info = re.findall(r".*search\?q=(.*)&p=.*",response.url)[0]
        if url_info:
            for i in range(2,11):
                next_url = "http://so.cnfol.com/cse/search?q={0}&p={1}&s=12596448179979580087"\
                    .format(url_info,i)

        # if url_info is not None:
        #     next_url = "http://so.cnfol.com/cse/" + url_info
                yield scrapy.Request(next_url,callback=self.parse)

    def parse_detail(self,response):
        item = response.meta["item"]
        if "2018" in item["href"]:
            item["update_date"] = str(datetime.date.today())
            item["title"] = response.xpath(
                "//div[@class='artMain mBlock']/h3[@class='artTitle']/text()").extract_first()
            if item["title"] is not None:
                item["title"] = "".join(item["title"].split())
                item["postive_score"] = handle_tag(item["title"])

            item["update_time"] = response.xpath(
                "//div[@class='artDes']/span[1]/text()").extract_first()
            item["news_time"] = datestamptrans(item["update_time"])
            platform = response.xpath(
                "//div[@class='artDes']/span[2]/text()").extract_first()
            if platform is not None:
                item["platform"] = re.findall(r"来源:(.*)", platform)[0]

            content = response.xpath("//div[@class='Article']//text()").extract()
            if content is not None and len(content) > 0:
                item["content"] = "".join(("".join(content)).split())
                # print(item)
                yield item
        #
        # else:
        #     item["update_date"] = str(datetime.date.today())
        #     item["title"] = response.xpath(
        #             "//div[contains(@class,'Art')]/h1[@id='Title']/text()").extract_first()
        #     if item["title"] is not None:
        #         item["title"] = "".join(item["title"].split())
        #         item["postive_score"] = handle_tag(item["title"])
        #     item["update_time"] = response.xpath(
        #             "//span[@id='pubtime_baidu']/text()").extract_first()
        #     item["news_time"] = datestamptrans(item["update_time"])
        #     item["platform"] = response.xpath(
        #         "//span[@id='source_baidu']/span/text()").extract_first()
        #     if item["platform"] is None:
        #         item["platform"] = response.xpath(
        #             "//span[@id='source_baidu']/a/text()").extract_first()
        #     content = response.xpath("//div[@id='Content']//text()").extract()
        #     if content is not None and len(content) > 0:
        #         item["content"] = "".join(("".join(content)).split())
        #         # print(item)
        #         yield item