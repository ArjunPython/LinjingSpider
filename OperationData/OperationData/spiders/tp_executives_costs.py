# -*- coding: utf-8 -*-
import datetime

import scrapy
from copy import deepcopy


class TpExecutivesCostsSpider(scrapy.Spider):
    name = 'tp_executives_costs'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://www.wdzj.com/dangan/search']

    def parse(self, response):
        li_list = response.xpath("//div[@class='terraceCon']/ul/li")
        for li in li_list:
            item = {}
            item["name"] = li.xpath("./div[@class='itemTitle']/h2/a/text()").extract_first()
            href = li.xpath("./div[@class='itemTitle']/h2/a/@href").extract_first()
            if href is not None:
                comment_href = "https://www.wdzj.com" + href
                yield scrapy.Request(comment_href, callback=self.parse_detail
                                     , meta={"item": deepcopy(item)})
        pages = response.xpath(
            "//div[@class='pageList']/a[contains(text(),'尾页')]/@currentnum").extract_first()
        for page in range(2, int(pages)):
            next_url = "https://www.wdzj.com/dangan/search?filter&currentPage={}".format(page)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = deepcopy(response.meta["item"])
        div_list = response.xpath("//div[@class='da-ggjj']/div")[1:]
        if div_list:
            for div in div_list:
                item["person_name"] = div.xpath("./div/b/text()").extract_first()
                introduction = div.xpath("./div/p/text()").extract_first()
                if introduction is not None:
                    item["introduction"] = "".join(introduction.split())
                item["management_fee"] = response.xpath("//div[@class='da-ptfy']/dl[1]//em/text()").extract_first()
                item["withdraw_fee"] = response.xpath("//div[@class='da-ptfy']/dl[2]//em/text()").extract_first()
                item["vip_fee"] = response.xpath("//div[@class='da-ptfy']/dl[5]//em/text()").extract_first()
                if item["vip_fee"] is not None:
                    item["vip_fee"] = "".join(item["vip_fee"].split())
                item["creat_date"] = str(datetime.date.today())
                # print(item)
                yield item
        else:
            item["person_name"] = None
            item["introduction"] = None
            item["management_fee"] = None
            item["withdraw_fee"] = None
            item["vip_fee"] = None
            item["creat_date"] = str(datetime.date.today())
            yield item
            # print(item)