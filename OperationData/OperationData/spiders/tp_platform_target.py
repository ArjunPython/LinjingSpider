# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy
import scrapy
from ..tools.connet_mysql import Search
from ..items import PlatformTargetItem


class TpPlatformTargetSpider(scrapy.Spider):
    name = 'tp_platform_target'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://www.wdzj.com/dangan/search?filter=e1&show=1']

    custom_settings = {"ITEM_PIPELINES": {
        'OperationData.pipelines.MysqlTwistedPipline': 250, }
    }

    def parse(self, response):
        li_list = response.xpath("//div[@class='terraceCon']/ul/li")
        # city = "杭州"
        for li in li_list:
            item = PlatformTargetItem()
            # city_info = li.xpath(".//div[@class='itemCon clearfix']/a/div[3]/text()").extract_first()
            # if city in city_info:
            item["b_href"] = li.xpath("./div/h2/a/@href").extract_first()
            if item["b_href"] is not None:
                href = "https://www.wdzj.com" + item["b_href"] + "gongshang/"
                yield scrapy.Request(href, callback=self.parse_detail, meta={"item": deepcopy(item)})

        for i in range(2, 67):
            next_url = "https://www.wdzj.com/dangan/search?filter=e1&show=1&currentPage={}".format(i)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):

        item = deepcopy(response.meta["item"])

        plat_id = response.xpath("//div[@class='container']/input/@value").extract_first()

        company_name = response.xpath(
            "//div[@class='lcen']/table//tr[1]/td[2]/text()").extract_first()
        try:
            item["pid"] = Search().search_id_sql(company_name)
        except Exception as e:
            print("数据库无此公司信息")

        shujue_href = "https://shuju.wdzj.com/plat-info-initialize.html"
        yield scrapy.FormRequest(shujue_href,
                                 formdata={"wdzjPlatId": plat_id},
                                 callback=self.shujue_detail,
                                 meta={"item": deepcopy(item)})

    def shujue_detail(self, response):

        item = deepcopy(response.meta["item"])
        # dict_response = json.loads(response.body.decode("utf-8"))
        try:
            dict_response = json.loads(response.body.decode("utf-8"))
            time_info = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            now = int(time.mktime(time.strptime(time_info, '%Y-%m-%d')))
            item["createtime"] = now

            """日成交量"""
            item["volume"] = dict_response["phValue"]["data"]["y1"][0]

            """资金净流入"""
            item["inflow"] = dict_response["phValue"]["data"]["y1"][1]

            """待还余额"""
            item["remaining_balance"] = dict_response["phValue"]["data"]["y1"][2]

            """平均预期收益率"""
            item["rate"] = dict_response["phValue"]["data"]["y1"][3]

            item["loan_sign"] = dict_response["phValue"]["data"]["y1"][10]

            """平均借款期限"""
            item["average_loan_term"] = dict_response["phValue"]["data"]["y1"][4]

            """投资人数"""
            item["investment_number"] = dict_response["phValue"]["data"]["y1"][5]

            """人均投资金额"""
            item["per_capita_investment"] = dict_response["phValue"]["data"]["y1"][6]

            """借款人数"""
            item["number_of_borrowers"] = dict_response["phValue"]["data"]["y1"][8]

            """人均借款金额"""
            item["per_capita_loan_amount"] = dict_response["phValue"]["data"]["y1"][9]

            item["r_invest_person"] = dict_response["phValue"]["data"]["y1"][7]
            item["r_loan_person"] = dict_response["phValue"]["data"]["y1"][10]
        except Exception as e:
            print("无数据显示")
        # print(item)
        yield item
