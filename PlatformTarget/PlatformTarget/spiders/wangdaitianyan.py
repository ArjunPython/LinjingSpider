# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime
from copy import deepcopy
from scrapy import signals
from tools.get_score import get_score
from scrapy_splash import SplashRequest
from items import WangDaiTieItem
from tools.connet_mysql import Search
from tools.BloomCheck import BloomCheckFunction
from scrapy.xlib.pydispatch import dispatcher
from emailSender import emailSender


class WangdaitianyanSpider(scrapy.Spider):
    name = 'wangdaitianyan'
    allowed_domains = ['p2peye.com']
    start_urls = []

    def __init__(self):
        super(WangdaitianyanSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.bof = BloomCheckFunction()

    def spider_closed(self, spider, reason):
        print("*" * 100)
        self.bof.save_bloom_file()


    def start_requests(self):
        t_url = "https://www.p2peye.com/platform/_{}/"
        # platform_list = Search().search_net_name()
        platform_list = ["微贷网", "优先贷", "人众金服"]
        for i in platform_list:
            item = {}
            item['platform_name'] = i
            item["pid"] = Search().search_id_sql(item['platform_name'])
            yield scrapy.Request(t_url.format(i),
                                 callback=self.parse,
                                 meta={"item": item},
                                 )

    def parse(self, response):
        li_list = response.xpath("//ul[@class='ui-result clearfix']/li[@class='ui-result-item']")
        for li in li_list:
            item = {}
            # 数据更新时间
            item["update_date"] = str(datetime.date.today())
            # 平台名称
            item["platform_name"] = li.xpath(".//div[@class='qt-gl clearfix']/a/@title").extract_first()
            item["pid"] = Search().search_id_sql(item["platform_name"])
            # 评论来源
            item["comm_resource"] = "网贷天眼"
            # 详情页对应url
            b_href = li.xpath(".//div[@class='qt-gl clearfix']/a/@href").extract_first()
            if b_href is not None:
                detail_url = "https:" + b_href + "/comment/"
                item["current_page"] = 1
                yield scrapy.Request(
                    detail_url,
                    callback=self.parse_review_detail,
                    meta={"item": deepcopy(item)},
                )
        # 下一页
        next_url = response.xpath("//div[@class='c-page']//a[contains(@title,'下一页')]/@href").extract_first()
        if next_url is not None:
            next_url = "https://www.p2peye.com" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    """请求每个公司的评论页面"""
    def parse_review_detail(self, response):
        item = deepcopy(response.meta["item"])

        li_list = response.xpath("//ul[@class='comment-inner']/li[@class='feed-detail clearfix']")
        if not li_list:
            print("%s无评论内容........." % item['platform_name'])
            return None
        for li in li_list:
            # 评论人
            item["comm_name"] = li.xpath(".//div[@class='face']/a/@title").extract_first()
            # 评论时间
            item["comm_time"] = li.xpath(".//div[@class='qt-gl time']/text()").extract_first()
            if item["comm_time"] is not None:
                item["comm_time"] = item["comm_time"].split(' ')[0]
                timeArray = time.strptime(item["comm_time"], "%Y-%m-%d")
                # 转换为时间戳:
                item["comm_time"] = int(time.mktime(timeArray))
            # 评论内容
            item["comm_info"] = li.xpath(".//div[@class='link']/a/text()").extract_first()
            if item["comm_info"] is not None:
                item["comm_info"] = "".join(item["comm_info"].split())
                if self.bof.process_item(item["comm_info"]):
                # 评论打分
                    item['comm_score'], item['comm_score_n'] = get_score(item['comm_info'])
            # if self.bof.process_item(item["comm_info"]):
                    yield item
                # print(item)
                else:
                    print("过滤器过滤..%s.........1" % item['platform_name'])
                    return None
            else:
                return None

            info_url = response.xpath("//div[@class='c-page']/a[1]/text()").extract_first()
            url_head = re.match(r'(.*)\/comment\/.*', response.url).group(1)
            if info_url is not None:
                item['current_page'] += 1
                if item['current_page'] <= 2:
                    next_url = url_head + "/comment/list-0-0-{0}.html".format(item['current_page'])
                    yield scrapy.Request(
                        next_url,
                        callback=self.parse_review_detail,
                        meta={"item": deepcopy(item)}
                    )




