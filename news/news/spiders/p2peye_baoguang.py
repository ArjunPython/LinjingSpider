# -*- coding: utf-8 -*-
import datetime
import time
import json
import re
from copy import deepcopy
import scrapy
from copyheaders import headers_raw_to_dict
from news.tools.handle_time import handle_tag
from ..items import NewsItem
from news.tools.handle import datestamptrans



class P2peyeBaoguangSpider(scrapy.Spider):
    name = 'p2peye_baoguang'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/forum-60-1.html']

    def parse(self, response):
        li_list = response.xpath("//div[@class='fn-listparent ui-listparent active']/ul/li")
        for li in li_list:
            item = NewsItem()
            item["update_date"] = str(datetime.date.today())
            item['title'] = li.xpath(".//div[@class='ui-forumlist-title']/a/text()").extract_first()
            item['platform'] = "网贷天眼平台曝光"
            detail_url = li.xpath(".//div[@class='ui-forumlist-title']/a/@href").extract_first()
            if detail_url is not None:
                item['href'] = "https://www.p2peye.com" + detail_url
                yield scrapy.Request(
                    item['href'],
                    callback=self.detail_parse,
                    meta={"item": deepcopy(item)}
                )
        for i in range(2,3):
            next_url = "https://www.p2peye.com/forum-60-{}.html?type=0".format(i)
            yield scrapy.Request(next_url,callback=self.parse)

    def detail_parse(self, response):
        item = deepcopy(response.meta["item"])
        item['postive_score'] = 0
        update_time = response.xpath("//div[@class='ui-article-hd-info-detail']/ul/li/em/text()").extract_first()
        if update_time is not None:
            # item['update_time'] = re.sub(r'发表于 ', '', update_time)
            item['update_time'] = update_time
            item['news_time'] = datestamptrans(item['update_time'])
        content_str = response.xpath("string(//td[@class='t_f'])").extract()
        if len(content_str) > 0:
            content_str = ''.join(''.join(content_str).split())
            content_str = ''.join(re.findall(r'[\u4e00-\u9fa5|，。、：；！？]+', content_str))
            item['content'] = re.sub(r'本帖最后.*?编辑|下载附件保存到相册|下载次数|图片|上传', '', content_str)
            yield item
