# -*- coding: utf-8 -*-
import datetime
import json
import re
import scrapy
from copy import deepcopy
from ChangeInfo.utils.handle import handle_uptime
from ChangeInfo.utils.connet_mysql import Search
from scrapy_splash import SplashRequest


class TpChangeInfoSpider(scrapy.Spider):
    name = 'tp_change_info'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/platform/all/']

    # def start_requests(self):
    #     start_url = 'https://www.p2peye.com/platform/all/'
    #     now_date = datetime.date.today()
    #     reader = Search()
    #     company_list = reader.search_sql(now_date)
    #     if len(company_list) > 0:
    #         yield scrapy.Request(start_url,callback=self.parse)
    #     else:
    #         print("%s无新增平台" % now_date)


    def parse(self, response):
        li_list = response.xpath("//ul[@class='ui-result clearfix']/li[@class='ui-result-item']")
        # city = "杭州"
        for li in li_list:
        # city_info = li.xpath(".//div[@class='ui-result-middle']/div/p[2]/text()").extract_first()
        # if city in city_info:
            item = {}
            item["net_name"] = li.xpath(".//div[@class='qt-gl clearfix']/a/@title").extract_first()
            b_href = li.xpath(".//div[@class='qt-gl clearfix']/a/@href").extract_first()
            if b_href is not None:
                url = "https:" + b_href + "/beian/"
                yield scrapy.Request(url,
                                     callback=self.parse_detail,
                                     meta={"item": deepcopy(item)})
                # yield SplashRequest(url,
                #                     callback=self.parse_detail,
                #                     meta={"item": deepcopy(item)},
                #                     args={'wait': 10})

        next_url = response.xpath("//div[@class='c-page']//a[contains(@title,'下一页')]/@href").extract_first()
        if next_url is not None:
            next_url = "https://www.p2peye.com" + next_url
            yield scrapy.Request(next_url,
                                 callback=self.parse)

    """获取pid"""
    def parse_detail(self, response):

        item = deepcopy(response.meta["item"])
        item["company_name"] = response.xpath(
            "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[1]/div[2]//text()").extract_first()
        pid = response.xpath("//div[@class='page_section']"
                             "/input[@id='template-plat-id']/@value").extract_first()
        """组合变更信息的rul"""
        url_h = re.match(r'(.*)\/beian', response.url).group(1)
        change_url = url_h + "/comchanajax/?pid={0}".format(pid)
        item['current_page'] = 0
        item["num"] = None
        yield scrapy.Request(change_url,
                             callback=self.parse_change,
                             meta={"item": deepcopy(item)})

        # yield SplashRequest(change_url,
        #                     callback=self.parse_change,
        #                     meta={"item": deepcopy(item)},
        #                     args={'wait': 12})

    def parse_change(self, response):
        item = deepcopy(response.meta["item"])
        data_content = response.body.decode()
        # re_data = re.match(
        #     r"""<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">(.*)</pre></body></html>""",data_content)
        # dict_data = json.loads(re_data.group(1))
        dict_data = json.loads(data_content)

        """获取变更信息总页数"""
        pagedom = dict_data["data"]["pagedom"]
        if len(pagedom) > 0:
            page_num = re.findall(r"<a href=javascript:void\(0\); pn=(\d*) title='尾页'>", pagedom)
            # page_num = re.findall(r"""&lt;a href=javascript:void\(0\); pn=(\d*) title='尾页'&gt;尾页&lt;/a&gt;""", pagedom)
            if len(page_num) > 0:
                item["num"] = int(page_num[0])

        data_list = dict_data["data"]["data"]
        for data in data_list:
            """变更时间"""
            changeTime = data["changeTime"]
            item["changeTime"] = handle_uptime(changeTime)
            """变更项目"""
            item["changeItem"] = data["changeItem"].replace("\r", "").replace("\n", "")
            """变更前"""
            item["contentBefore"] = data["contentBefore"].replace("<em>", "") \
                .replace("<br>", "").replace("\r", "").replace("\n", "").replace("</em>","").replace("<b>","").replace("</b>","")

            if item["contentBefore"] is not None:
                item["contentBefore"] = "".join(item["contentBefore"].split())
            """变更后"""
            item["contentAfter"] = data["contentAfter"].replace("<em>", "") \
                .replace("<br>", "").replace("\r", "").replace("\n", "").replace("</em>","").replace("<b>","").replace("</b>","")
            if item["contentBefore"] is not None:
                item["contentAfter"] = "".join(item["contentAfter"].split())

            yield item

        url_head = re.findall(r'.*?\?pid=\d+', response.url)[0]
        try:
            """请求下一页"""
            if item["num"] > item['current_page']:
                item['current_page'] += 1
                next_page = url_head + "&pn={0}".format(item['current_page'])
                yield scrapy.Request(next_page,
                                    callback=self.parse_change,
                                    meta={"item": deepcopy(item)})
        except Exception as e:
            print(e)
            print("无下一页")

