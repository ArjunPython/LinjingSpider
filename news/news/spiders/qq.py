# -*- coding: utf-8 -*-
import datetime
import time
import json
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans



class QqSpider(scrapy.Spider):
    name = 'qq'
    allowed_domains = ['qq.com']
    start_urls = [
        'http://pacaio.match.qq.com/irs/rcd?cid=52&token=8f6b50e1667f130c10f981309e1d8200&ext=3910,3911,3904,3901,3906,3912,3917,3902&page=0']
    #
    # def start_requests(self):
    #     headers = {
    #         'Referer': 'http://new.qq.com/ch2/licai',
    #     }
    #     yield scrapy.Request(
    #         self.start_urls[0],
    #         headers=headers,
    #         callback=self.parse
    #     )

    def parse(self, response):
        pass
    #     res = json.loads(response.body.decode())
    #     revs = res["data"]
    #     for rev in revs:
    #         item = NewsItem()
    #         item["update_date"] = str(datetime.date.today())
    #         item['title'] = rev['title']
    #         item['postive_score'] = handle_tag(item['title'])
    #         update_time = rev['update_time']
    #         if update_time is not None:
    #             item['update_time'] = update_time
    #             item['news_time'] = datestamptrans(item['update_time'])
    #         item['platform'] = rev['source']
    #         item['href'] = rev['vurl']
    #         a_re = re.search(r'\.html', item['href'])
    #         if a_re:
    #             item['href'] = rev['vurl']
    #         else:
    #             item['href'] = rev['vurl'][0:-2] + ".html"
    #         yield scrapy.Request(
    #             item['href'],
    #             callback=self.detail_parse,
    #             meta={"item": deepcopy(item)}
    #         )
    #
    # def detail_parse(self, response):
    #     item = deepcopy(response.meta["item"])
    #     content = response.xpath("string(//div[@class='content-article'])").extract()
    #     if len(content) > 0:
    #         item['content'] = ''.join(''.join(content).split())
    #         yield item
    #
