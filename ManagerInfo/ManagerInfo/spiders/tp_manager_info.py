# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
from copy import deepcopy
from ManagerInfo.utils.connet_mysql import Search
from scrapy_splash import SplashRequest

class TpManagerInfoSpider(scrapy.Spider):
    name = 'tp_manager_info'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/platform/all/']

    # def start_requests(self):
    #
    #     for i in range(121, 219):
    #         start_urls = "https://www.p2peye.com/platform/all/p{}/".format(i)
    #         yield SplashRequest(start_urls,
    #                             callback=self.parse,
    #                             args={'wait': 10})

    def parse(self, response):
        li_list = response.xpath("//ul[@class='ui-result clearfix']/li[@class='ui-result-item']")
        for li in li_list:
            item = {}
            item["net_name"] = li.xpath(".//div[@class='qt-gl clearfix']/a/@title").extract_first()
            item["net_name"] = "".join(item["net_name"].split())
            b_href = li.xpath(".//div[@class='qt-gl clearfix']/a/@href").extract_first()
            if b_href is not None:
                url = "https:" + b_href
                yield scrapy.Request(url,
                                     callback=self.parse_detail,
                                     meta={"item": deepcopy(item)})
                # yield SplashRequest(url,
                #                     callback=self.parse_detail,
                #                     meta={"item": deepcopy(item)},
                #                     args={'wait': 12})

        next_url = response.xpath("//div[@class='c-page']//a[contains(@title,'下一页')]/@href").extract_first()
        if next_url is not None:
            next_url = "https://www.p2peye.com" + next_url
            yield scrapy.Request(next_url,
                                 callback=self.parse)

    def parse_detail(self, response):

        item = deepcopy(response.meta["item"])
        item["pid"] = Search().search_id_sql(item["net_name"])
        item["comment"] = []
        dls = response.xpath("//div[@id='pingtaigaoguan']/dl")
        for dl in dls:
            item_1 = {}
            try:
                name = dl.xpath("./dd[@class='describe']/p[@class='name']/text()").extract_first()
                if name is not None and len(name) > 0:
                    item_1["name"] = "".join(name.split())
                    shortcut = dl.xpath("./dd[@class='describe']/p[@class='shortcut']/text()").extract_first()
                    if shortcut is not None and len(shortcut) > 0:
                        item_1["shortcut"] = "".join(shortcut.split())
                    else:
                        item_1["shortcut"] = None
                    job = dl.xpath("./dd[@class='describe']/p[@class='job']/text()").extract_first()
                    if job is not None and len(job) > 0:
                        item_1["job"] = "".join(job.split())
                    else:
                        item_1["job"] = None
                    item["comment"].append(item_1)
            except Exception as e:
                pass

        if len(item["comment"]) > 0:
            item["comment"] = json.dumps(item["comment"])
            # print(item)
            yield item
