# -*- coding: utf-8 -*-
import scrapy
import datetime
from items import PlatformTargetItem
import time
from tools.connet_mysql import Search


class DailuopanSpider(scrapy.Spider):
    name = 'dailuopan'
    allowed_domains = ['']
    start_urls = ['http://127.0.0.1']

    custom_settings = {'DOWNLOAD_DELAY': 2,
                       'ITEM_PIPELINES': {
                        'PlatformTarget.pipelines.MysqlTwistedPipline': 250,
                       }
                       }

    def parse(self, response):
        print(response.text)
        tr_list = response.xpath("//table[@id='shujuList_table']/tbody/tr")
        for tr in tr_list:
            item = PlatformTargetItem()
            item["name"] = tr.xpath(".//td[2]/a/text()").extract_first()
            item["pid"] = Search().search_id_sql(item["name"])
            item["score"] = tr.xpath("./td[3]/text()").extract_first()
            timeArray = time.strptime(str(datetime.date.today()), "%Y-%m-%d")
            item["create_time"] = int(time.mktime(timeArray))
            yield item
