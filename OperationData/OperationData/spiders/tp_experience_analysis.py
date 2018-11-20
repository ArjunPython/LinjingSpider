# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from copy import deepcopy


class TpExperienceAnalysisSpider(scrapy.Spider):
    name = 'tp_experience_analysis'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://www.wdzj.com/dangan/search']

    def parse(self, response):
        li_list = response.xpath("//div[@class='terraceCon']/ul/li")
        for li in li_list:
            item = {}
            item["name"] = li.xpath("./div[@class='itemTitle']/h2/a/text()").extract_first()
            if item["name"] == "微银金服":
                item["name"] = "微银理财"
            if item["name"] == "米袋子理财":
                item["name"] = "米袋子"
            href = li.xpath("./div[@class='itemTitle']/h2/a/@href").extract_first()
            if href is not None:
                comment_href = "https://www.wdzj.com" + href + "dianping/"
                yield scrapy.Request(comment_href,callback=self.parse_comm_detail
                                     ,meta={"item":deepcopy(item)})

        pages = response.xpath(
            "//div[@class='pageList']/a[contains(text(),'尾页')]/@currentnum").extract_first()
        for page in range(2,int(pages)):
            next_url = "https://www.wdzj.com/dangan/search?filter&currentPage={}".format(page)
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_comm_detail(self,response):
        item = deepcopy(response.meta["item"])
        com_num_info = response.xpath(
            "//div[@class='dianpBox']/div[@class='dianpinbox']/span/text()").extract_first()
        try:
            if com_num_info is not None:
                com_num_info = "".join(com_num_info.split())
                item["comments_num"] = re.match(r"已有(\d+)人点评", com_num_info).group(1)
        except Exception as e:
            item["comments_num"] = 0
        item["withdrawal_speed"] = response.xpath(
            "//div[@class='dianpBox']/div[@class='pf-box']/dl[1]/dd[1]/em/text()").extract_first()
        if item["withdrawal_speed"] is None:
            item["withdrawal_speed"] = 0
        item["funds_idle"] = response.xpath(
            "//div[@class='dianpBox']/div[@class='pf-box']/dl[1]/dd[2]/em/text()").extract_first()
        if item["funds_idle"] is None:
            item["funds_idle"] = 0
        item["customer_service"] = response.xpath(
            "//div[@class='dianpBox']/div[@class='pf-box']/dl[1]/dd[3]/em/text()").extract_first()
        if item["customer_service"] is None:
            item["customer_service"] = 0
        item["experience"] = response.xpath(
            "//div[@class='dianpBox']/div[@class='pf-box']/dl[1]/dd[4]/em/text()").extract_first()
        if item["experience"] is None:
            item["experience"] = 0

        recom = response.xpath(
            "//div[@class='pl-titnavbox']/div[@class='lba']/a[2]/text()").extract_first()
        if recom is not None:
            item["recommend"] = re.match(r"推荐\((\d+)\)",recom).group(1)

        item["creat_date"] = str(datetime.date.today())

        # print(item)
        yield item