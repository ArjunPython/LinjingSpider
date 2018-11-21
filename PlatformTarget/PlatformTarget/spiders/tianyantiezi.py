# -*- coding: utf-8 -*-
import scrapy
import time
import re
import datetime
from scrapy import signals
from items import WangDaiTieItem
from tools.get_score import get_score
from copy import deepcopy
from scrapy_splash import SplashRequest
from scrapy.xlib.pydispatch import dispatcher
from tools.BloomCheck import BloomCheckFunction
from emailSender import emailSender
from tools.connet_mysql import Search


class TianyantieziSpider(scrapy.Spider):
    name = 'tianyantiezi'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/search.php?mod=forum&srchtxt={}']

    def __init__(self):
        self.bof = BloomCheckFunction()
        super(TianyantieziSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider,reason):
        print("*"*50)
        print("%s spider closed" % spider.name)
        self.bof.save_bloom_file()
        emailSenderClient = emailSender()
        toSendEmailLst = ["xxxxxx"]
        stats_info = self.crawler.stats._stats
        body = "爬虫[%s]已经关闭，原因是: %s.\n以下为运行信息：\n %s" % (spider.name, reason, stats_info)
        subject = "[%s]爬虫关闭提醒" % spider.name
        emailSenderClient.sendEmail(toSendEmailLst, subject, body)

    def start_requests(self):
        t_url = "https://www.p2peye.com/search.php?mod=forum&srchtxt={}"
        # platform_list = Search().search_net_name()
        platform_list = ["微贷网","优先贷","人众金服"]
        for i in platform_list:
            item = {}
            item['platform_name'] = i
            item["pid"] = Search().search_id_sql(item['platform_name'])
            yield scrapy.Request(t_url.format(i),
                                callback=self.parse,
                                meta={"item": item},
                                )

    def parse(self, response):
        item = response.meta["item"]
        div_list = response.xpath("//div[@class='ui-keynews']")
        if not div_list:
            print("%s...无帖子内容........." % item['platform_name'])
            return None
        for div in div_list:
            # 数据更新时间
            item["update_date"] = str(datetime.date.today())
            # 评论时间
            item['comm_time'] = div.xpath(".//div[@class='ui-keynews-tag']/span[@class='ui-keynews-tag-time']/text()").extract_first()
            if item["comm_time"] is not None:
                item["comm_time"] = item["comm_time"].split(' ')[0]
                timeArray = time.strptime(item["comm_time"], "%Y-%m-%d")
                # 转换为时间戳:
                item["comm_time"] = int(time.mktime(timeArray))
            # 评论人
            item['comm_name'] = div.xpath(".//div[@class='ui-keynews-tag']/a[1]/text()").extract_first()
            # 评论来源
            item['comm_resource'] = '网贷天眼'
            # 详情页对应url
            detail_url = div.xpath(".//div[@class='result-t']/a/@href").extract_first()
            if detail_url is not None and self.bof.process_item(detail_url):
                detail_url = "https://www.p2peye.com" + detail_url
                yield scrapy.Request(
                    detail_url,
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)},
                )
            else:
                print("过滤器过滤..%s.........1" % item['platform_name'])
                return None

    def detail_parse(self, response):
        item = response.meta["item"]
        # 评论内容
        item['comm_info'] = response.xpath("string(//td[@class='t_f'])").extract_first()
        if item['comm_info'] is not None:
            item['comm_info'] = ''.join(''.join(item['comm_info']).split())
            item['comm_info'] = ''.join(re.findall(r'[\u4e00-\u9fa5|，。、：；！？]+', item['comm_info']))
            item['comm_info'] = re.sub(r'本帖最后.*?编辑|下载附件保存到相册|下载次数|图片|上传', '', item['comm_info'])
            # 评论打分
            item['comm_score'], item['comm_score_n'] = get_score(item['comm_info'])
        # print(item)
            yield item
