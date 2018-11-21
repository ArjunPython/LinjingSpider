# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from copy import deepcopy
from news.tools.connet_mysql import seach_sql_all
from news.tools.handle import datestamptrans
from items import NewsItem
from urllib.parse import unquote
from news.tools.handle_time import handle_tag

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    # allowed_domains = ["baidu.com" '172.16.20.243']
    # allowed_domains = ["baiducontent.com" '172.16.20.243']
    start_urls = ['http://baidu.com/']

    def start_requests(self):
        # name_list = seach_sql_all()
        name_list = ["人众金服"]
        for name in name_list:
            url = 'http://news.baidu.com/ns?word=(%20"{}"%20)&pn=0' \
                  '&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0&rsv_page=1'.format(name)
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        item = NewsItem()
        # item = {}
        div_list = response.xpath("//div[@class='result']")
        for div in div_list:
            item["update_date"] = str(datetime.date.today())
            try:
                name_info = re.findall(r"http:\/\/news\.baidu\.com\/ns\?word=\(%20%22(.*)%22%20\)&pn=.*", response.url)[0]
            except Exception as e:
                name_info = re.match(r"http:\/\/news\.baidu\.com\/ns\?word=%28%20%22(.*)%22%20%29&pn=.*",response.url).group(1)

            text = unquote(name_info, "utf-8")
            title_list = div.xpath("./h3/a/text()|./h3/a/em/text()").extract()
            if len(title_list) > 0:
                title = ''.join(''.join(title_list).split())
                if title.__contains__(text):
                    item['title'] = title
                    # print(title)
                    # item["postive_score"] = handle_tag(item["title"])
                    item["postive_score"] = None

            # 发布信息
            public_str = div.xpath(".//p[@class='c-author']/text()").extract_first()
            # print(public_str)
            if public_str is not None:
                update_time = ''.join(public_str).split()
                if len(update_time) >= 3:
                    item['update_time'] = update_time[1]+update_time[2]
                    item['news_time'] = datestamptrans(item['update_time'])
                    item['platform'] = update_time[0]
                else:
                    item['update_time'] = update_time[0] + update_time[1]
                    item['news_time'] = datestamptrans(item['update_time'])
                    item['platform'] = None
            # print(item['update_time'])
            # 正文内容对应url
            # item['href'] = div.xpath("./h3/a/@href").extract_first()
            # 百度快照url
            detail_url = div.xpath(".//a[@class='c-cache']/@href").extract_first()
            if detail_url is not None:
                url_con = re.match(r"http:\/\/cache\.baidu\.com\/c\?m=(.*)",detail_url).group(1)
                item['href'] = "http://cache.baiducontent.com/c?m=" + url_con
                yield scrapy.Request(
                    item['href'],
                    # detail_url,
                    callback=self.detail_parse,
                    meta={'item': deepcopy(item)}
                    )

        # n = re.findall(r"http:\/\/news\.baidu\.com\/ns\?word=\(%20%22(.*)%22%20\)&pn=.*", response.url)[0]
        # t = unquote(n, "utf-8")
        # for i in range(2,4):
        #     next_url = 'http://news.baidu.com/ns?word=(%20"{0}"%20)&pn={1}' \
        #           '&cl=2&ct=1&tn=news&rn=20&ie=utf-8&bt=0&et=0&rsv_page=1'.format(t,(i-1)*20)
        #     print("*"*100)
        #     print(next_url)
            # yield scrapy.Request(
            #             next_url,
            #             callback=self.parse)
        next_url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if next_url is not None:
            page_num = re.search(r'pn=(\d+)', next_url).group(1)
            if int(page_num) <= 20:
                next_url = "http://news.baidu.com" + next_url
                yield scrapy.Request(
                    next_url,
                    callback=self.parse)

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        content = response.xpath(
            "//p[position()>1]/text()|//p[position()>1]/font/text()|//p[position()>1]/strong/text()").extract()
        if content is not None and len(content) > 0:
            item['content'] = ''.join(''.join(content).split())
            # print(item)
            yield item
