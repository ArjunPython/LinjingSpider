# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from copy import deepcopy


class TpPlatformBackgroundSpider(scrapy.Spider):
    name = 'tp_platform_background'
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
            item["tag"] = None
            tag = li.xpath("./div[@class='itemTitle']/div/em/text()").extract()
            if tag is not None:
                item["tag"] = "".join("".join(tag).split())
            pro_city = li.xpath("./div[@class='itemCon clearfix']/a/div[3]/text()").extract_first()
            if pro_city is not None:
                item["province"] = re.match(r"注册地：(.*)\|(.*)",pro_city).group(1)
                item["city"] = re.match(r"注册地：(.*)\|(.*)",pro_city).group(2)
            online_time = li.xpath("./div[@class='itemCon clearfix']/a/div[4]/text()").extract_first()
            if online_time is not None:
                item["time_online"] = re.match(r"上线时间：(.*)",online_time).group(1)
            item["status"] = None
            item["status"] = li.xpath("./div[@class='itemTitle']/h2/div/ul/li/text()").extract_first()

            href = li.xpath("./div[@class='itemTitle']/h2/a/@href").extract_first()
            if href is not None:
                item["href"] = "https://www.wdzj.com" + href
                yield scrapy.Request(item["href"], callback=self.parse_detail
                                     , meta={"item": deepcopy(item)})

        pages = response.xpath(
            "//div[@class='pageList']/a[contains(text(),'尾页')]/@currentnum").extract_first()
        for page in range(2, int(pages)):
            next_url = "https://www.wdzj.com/dangan/search?filter&currentPage={}".format(page)
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_detail(self,response):
        item = deepcopy(response.meta["item"])
        funds = response.xpath(
            "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[1]/div[2]/text()").extract_first()
        # item["registered_capital"] = None
        # item["paid_capital"] = None

        if funds is not None:
            item["funds"] = "".join(funds.split())
            re_funds = re.findall(r"(\d+)", item["funds"])
            if len(re_funds) == 2:
                item["registered_capital"] = re_funds[0]
                item["paid_capital"] = re_funds[1]
            elif re_funds and len(re_funds) == 1:
                item["registered_capital"] = re_funds[0]
                item["paid_capital"] = None
            else:
                item["registered_capital"] = None
                item["paid_capital"] = None
        dd_list = response.xpath("//div[@class='bgbox-bt zzfwbox']/dl[1]/dd")
        if len(dd_list) == 6:
            equity_listing = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[2]/div[2]//text()").extract_first()
            if equity_listing is not None:
                item["equity_listing"] = "".join(equity_listing.split())

            bank_depository = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[3]/div[2]//text()").extract_first()
            if bank_depository is not None:
                bank_depository = "".join(bank_depository.split())
                try:
                    item["bank"] = re.match(r"用户资金存管存管机构为(.*)", bank_depository).group(1)
                except Exception as e:
                    item["bank"] = None

            financing = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[4]/div[2]//text()").extract()
            item["financing"] = "".join("".join(financing).split())
            if len(item["financing"]) == 1:
                item["financing"] = None

            regulatory_association = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[5]/div[2]//text()").extract()
            item["regulatory_association"] = "".join("".join(regulatory_association).split())
            if len(item["regulatory_association"]) == 1:
                item["regulatory_association"] = None

            icp_num = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[6]/div[2]//text()").extract_first()
            item["icp_num"] = "".join(icp_num.split())
            if len(item["icp_num"]) == 1:
                item["icp_num"] = None

        elif len(dd_list) == 5:
            item["equity_listing"] = None
            bank_depository = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[2]/div[2]//text()").extract_first()
            if bank_depository is not None:
                bank_depository = "".join(bank_depository.split())
                try:
                    item["bank"] = re.match(r"用户资金存管存管机构为(.*)", bank_depository).group(1)
                except Exception as e:
                    item["bank"] = None
            financing = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[3]/div[2]//text()").extract()
            item["financing"] = "".join("".join(financing).split())
            if len(item["financing"]) == 1:
                item["financing"] = None

            regulatory_association = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[4]/div[2]//text()").extract()
            item["regulatory_association"] = "".join("".join(regulatory_association).split())
            if len(item["regulatory_association"]) == 1:
                item["regulatory_association"] = None

            icp_num = response.xpath(
                "//div[@class='bgbox-bt zzfwbox']/dl[1]/dd[5]/div[2]//text()").extract_first()
            item["icp_num"] = "".join(icp_num.split())
            if len(item["icp_num"]) == 1:
                item["icp_num"] = None

        claims = response.xpath(
            "//div[@class='bgbox-bt zzfwbox']/dl[2]/dd[2]/div[2]//text()").extract_first()
        item["claims"] = "".join(claims.split())
        if len(item["claims"]) == 1:
            item["claims"] = None
        item["guarantee_institution"] = response.xpath(
            "//div[@class='bgbox-bt zzfwbox']/dl[2]/dd[5]/div[2]//text()").extract_first()
        item["creat_date"] = str(datetime.date.today())

        company_url = item["href"] + "gongshang/"
        yield scrapy.Request(company_url,callback=self.pares_company,
                             meta={"item":deepcopy(item)})

    def pares_company(self,response):
        item = deepcopy(response.meta["item"])
        item["company_name"] = response.xpath(
            "//div[@class='lcen']/table//tr[1]/td[2]/text()").extract_first()
        # print(item)
        yield item








