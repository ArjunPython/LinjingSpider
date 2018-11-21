# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
import scrapy
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans


class JrjSpider(scrapy.Spider):
    name = 'jrj'
    allowed_domains = ['finance.jrj.com.cn']
    start_urls = ['http://finance.jrj.com.cn/it-finance/xwk/{0}/{1}_1.shtml']

    def start_requests(self):
        today = datetime.date.today()
        a_data = '20' + today.strftime('%y%m')
        b_data = '20' + today.strftime('%y%m%d')
        yield scrapy.Request(
            self.start_urls[0].format(a_data, b_data),
            callback=self.parse
        )

    def parse(self, response):
        li_list = response.xpath("//div[@class='main']/ul/li")
        for li in li_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            title = li.xpath("./a/text()").extract_first()
            if title is not None:
                item['title'] = title
                item['postive_score'] = handle_tag(item['title'])
            update_time = li.xpath("./span/text()").extract_first()
            if update_time is not None:
                item['update_time'] = update_time
                item['news_time'] = datestamptrans(item['update_time'])
            item['href'] = li.xpath("./a/@href").extract_first()
            if item['href'] is not None:
                yield scrapy.Request(
                    item['href'],
                    callback=self.parse_content,
                    meta={"item": deepcopy(item)}
                )
    def parse_content(self, response):
        item = deepcopy(response.meta["item"])
        item['platform'] = response.xpath("//div[@class='titmain']/p[@class='inftop']/span[2]/text()").extract()
        try:
            item['platform'] = ''.join(item['platform']).replace('\r', '').replace('\t', '').replace('\n', '').split('：')[1]
            a_str = re.findall(r'零壹', item['platform'])
            if len(item['platform']) == 0:
                item['platform'] = "金融界财经"
            elif a_str:
                item['platform'] = "零壹财经"
        except:
            item['platform'] = "金融界财经"
        content = response.xpath("string(//div[@class='texttit_m1'])").extract()
        if len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            # print(item)
            yield item
