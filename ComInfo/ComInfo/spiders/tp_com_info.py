# -*- coding: utf-8 -*-
import csv
import datetime
import json
import re
import scrapy
from copy import deepcopy
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from ComInfo.utils.common import handle_uptime,handle_business_time
from ComInfo.utils.common import handle_regis_money,handle_area,handle_tag,handle_class_title
from ComInfo.utils.address import handle_address,Address
from copyheaders import headers_raw_to_dict
from scrapy_splash import SplashRequest
from ComInfo.utils.connet_mysql import seach_sql
from ComInfo.utils.proxymid import ProxyMiddleware
from ComInfo.emailSender import EmailSender



class TpComInfoSpider(scrapy.Spider):
    name = 'tp_com_info'
    allowed_domains = ['p2peye.com']
    start_urls = ['https://www.p2peye.com/platform/all/']
    # start_urls = ['https://www.p2peye.com/platform/c12/']
    # start_urls = ['https://www.p2peye.com/platform/_%E5%89%8D%E6%B5%B7%E9%93%B6%E7%AE%A1%E5%AE%B6(%E9%93%B6%E7%AE%A1%E5%AE%B6)/']

    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    # def __init__(self):
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--disable-gpu')
    #     self.browser = webdriver.Chrome(chrome_options=chrome_options)
    #     super(TpComInfoSpider, self).__init__()
    #
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self, spider):
    #     print("spider closed")
    #     self.browser.quit()

    # ip = ProxyMiddleware()
    # ip_port = ip.get_random_proxy()
    #
    # lua_script = """
    #        function main(splash,args)
    #             splash:on_request(function(request)
    #                request:set_proxy{
    #                    host = '%s',
    #                    port = %d,
    #                    type = "http"
    #                  }
    #                 end)
    #            splash:wait(8)
    #            splash:go(splash.args.url)
    #            return splash:html()
    #        end
    #    """ % (ip_port[0],ip_port[1])

    # lua_script = """
    #            function main(splash,args)
    #                 splash:on_request(function(request)
    #                    request:set_proxy{
    #                        host = '183.161.240.248',
    #                        port = 6458,
    #                        type = "https"
    #                      }
    #                     end)
    #                splash:wait(8)
    #                splash:go(splash.args.url)
    #                return splash:html()
    #            end
    #        """

    # def start_requests(self):

    #     # PROXY = """
    #     #        splash:on_request(function(request)
    #     #        request:set_proxy{
    #     #            host = 49.72.80.39,
    #     #            port = 2589,
    #     #        }
    #     #        return splash:html()
    #     #        end)
    #     #    """
    #     reader = csv.reader(open('add.csv', 'r'))
    #     for line in reader:
    #         i = line[0]
    #         urls = "https://www.p2peye.com/platform/_{0}/".format(i)
    #         yield scrapy.Request(urls,
    #                              callback=self.parse)
    #     for i in range(1,51):
    #         start_urls = "https://www.p2peye.com/platform/all/p{}/".format(i)
    #         # start_urls = "https://www.p2peye.com/platform/c12/p{}/".format(i)
    #         # start_urls = "https://www.p2peye.com/platform/_%E9%91%AB%E5%90%88%E6%B1%87/"
    #         yield SplashRequest(start_urls,
    #                             callback=self.parse,
    #                             endpoint="execute",
    #                             args={"wait": 15,
    #                                     "lua_source": self.lua_script}
    #
    #
    #                            )

    def __init__(self):
        super(TpComInfoSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def spider_closed(self, spider,reason):
        print("spider closed")
        emailSenderClient = EmailSender()
        toSendEmailLst = ["xxxxxx"]
        stats_info = self.crawler.stats._stats
        body = "爬虫[%s]已经关闭，原因是: %s.\n以下为运行信息：\n %s" % (spider.name, reason, stats_info)
        subject = "[%s]爬虫关闭提醒" % spider.name
        emailSenderClient.sendEmail(toSendEmailLst,subject,body)


    def parse(self, response):
        li_list = response.xpath("//ul[@class='ui-result clearfix']/li[@class='ui-result-item']")
        for li in li_list:
            item = {}
            item["net_name"] = li.xpath(".//div[@class='qt-gl clearfix']/a/@title").extract_first()
            item["net_name"] = "".join(item["net_name"].split())
            title_info = li.xpath(".//div[@class='ui-result-box']/div[2]/@class").extract_first()
            class_title = "".join(title_info.split())
            s_info = li.xpath(".//div[@class='ui-result-left']/p[2]/text()").extract_first()
            state_info = "".join(s_info.split()).split("运营状态：")[1]
            if state_info:
                item["status"] = state_info
            else:
                item["status"] = handle_class_title(class_title)
            b_href = li.xpath(".//div[@class='qt-gl clearfix']/a/@href").extract_first()
            if b_href is not None:
                url = "https:" + b_href
                yield scrapy.Request(url,
                                     callback=self.parse_top_detail,
                                     meta={"item": deepcopy(item)})
                # yield SplashRequest(url,
                #                     callback=self.parse_top_detail,
                #                     endpoint="execute",
                #                     args={"wait": 16,
                #                           "lua_source": self.lua_script},
                #                     meta={"item": deepcopy(item)})
        for i in range(2,61):
            next_url = "https://www.p2peye.com/platform/all/p{}/".format(i)

        # next_url = response.xpath(
        #     "//div[@class='c-page']//a[contains(@title,'下一页')]/@href").extract_first()
        # if next_url is not None:
        #     next_url = "https://www.p2peye.com" + next_url

            yield scrapy.Request(next_url,
                                 callback=self.parse)

    def parse_top_detail(self, response):
        item = deepcopy(response.meta["item"])

        event_time_info = response.xpath("//div[@class='cen']/div[@class='tit']/a/text()").extract()
        if len(event_time_info) > 0:
            event_time = "".join("".join(event_time_info).split())
            """事件发生时间：2018-06-19>>"""
            con = re.match(r"事件发生时间：(.*)>>", event_time).group(1)
            item["event_time"] = handle_uptime(con)
        else:
            item["event_time"] = 0

        icp_num = response.xpath(
            "//div[@class='strength-content clearfix']/div[2]/span[@class='strength-value']/text()").extract_first()
        icp_key = response.xpath(
            "//div[@class='strength-content clearfix']/div[2]/span[@class='strength-key']/text()").extract_first()
        item["icp_number"] = ""
        if icp_num and icp_key is not None:
            icp_num = "".join(icp_num.split())
            icp_key = "".join(icp_key.split())
            if "ICP" in icp_key:
                item["icp_number"] = icp_num
            else:
                item["icp_number"] = ""
        try:


            item["bank_time"] = None
            item["bank"] = ""
            item["association"] = ""

            bank_key_1 = response.xpath(
                "//div[@class='strength-content clearfix']/div[3]/span[@class='strength-key']/text()").extract_first()
            bank_value_1 = response.xpath(
                "//div[@class='strength-content clearfix']/div[3]/span[@class='strength-value']/text()").extract_first()

            bank_key_2 = response.xpath(
                "//div[@class='strength-content clearfix']/div[4]/span[@class='strength-key']/text()").extract_first()
            bank_value_2 = response.xpath(
                "//div[@class='strength-content clearfix']/div[4]/span[@class='strength-value']/text()").extract_first()

            bank_key_3 = response.xpath(
                "//div[@class='strength-content clearfix']/div[5]/span[@class='strength-key']/text()").extract_first()
            bank_value_3 = response.xpath(
                "//div[@class='strength-content clearfix']/div[5]/span[@class='strength-value']/text()").extract_first()

            bank_key_4 = response.xpath(
                "//div[@class='strength-content clearfix']/div[6]/span[@class='strength-key']/text()").extract_first()
            bank_value_4 = response.xpath(
                "//div[@class='strength-content clearfix']/div[6]/span[@class='strength-value']/text()").extract_first()

            bank_key_5 = response.xpath(
                "//div[@class='strength-content clearfix']/div[7]/span[@class='strength-key']/text()").extract_first()
            bank_value_5 = response.xpath(
                "//div[@class='strength-content clearfix']/div[7]/span[@class='strength-value']/text()").extract_first()

            bank_key_6 = response.xpath(
                "//div[@class='strength-content clearfix']/div[2]/span[@class='strength-key']/text()").extract_first()
            bank_value_6 = response.xpath(
                "//div[@class='strength-content clearfix']/div[2]/span[@class='strength-value']/text()").extract_first()

            if bank_key_1:
                if "银行存管" in bank_key_1 and bank_value_1 is not None:
                    bank_info = "".join(bank_value_1.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)
                elif "加入协会" in bank_key_1:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[3]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)


            if bank_key_2:
                if "银行存管" in bank_key_2 and bank_value_2 is not None:
                    bank_info = "".join(bank_value_2.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)
                elif "加入协会" in bank_key_2:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[4]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)

            if bank_key_3:
                if "银行存管" in bank_key_3 and bank_value_3 is not None:
                    bank_info = "".join(bank_value_3.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)
                elif "加入协会" in bank_key_3:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[5]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)

            if bank_key_4:
                if "银行存管" in bank_key_4 and bank_value_4 is not None:
                    bank_info = "".join(bank_value_4.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)

                elif "加入协会" in bank_key_4:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[6]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)

            if bank_key_5:
                if "银行存管" in bank_key_5 and bank_value_5 is not None:
                    bank_info = "".join(bank_value_5.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)
                elif "加入协会" in bank_key_5:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[7]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)

            if bank_key_6:
                if "银行存管" in bank_key_6 and bank_value_6 is not None:
                    bank_info = "".join(bank_value_6.split())
                    item["bank"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(1)
                    item["bank_time"] = re.match(r"(.*)－存管上线时间(.*)", bank_info).group(2)
                elif "加入协会" in bank_key_6:
                    span_list = response.xpath(
                        "//div[@class='strength-content clearfix']/div[2]/span[@class='strength-value']/text()").extract()
                    item["association"] = json.dumps(span_list)

        except Exception as e:
            item["bank"] = ""
            item["bank_time"] = None

        detail_url = response.url + "/beian/"
        yield scrapy.Request(detail_url,
                             callback=self.parse_detail,
                             meta={"item": deepcopy(item)})

        # yield SplashRequest(detail_url,
        #                     callback=self.parse_detail,
        #                     endpoint="execute",
        #                     args={"wait": 18,
        #                           "lua_source": self.lua_script},
        #                     meta={"item": deepcopy(item)})

    def parse_detail(self, response):
        item = deepcopy(response.meta["item"])
        """公司官网"""
        item["url"] = response.xpath("//div[@class='ri']//a/@data-href").extract_first()

        logo = response.xpath("//div[@class='le']/a/img/@src").extract_first()
        if logo is not None:
            """logo图片地址"""
            if logo.startswith('https'):
                item["logo"] = logo
            else:
                item["logo"] = "https:" + logo
        else:
            item["logo"] = ""

        """平均年化收益"""
        item["average_annual_income"] = response.xpath(
            "//ul[@class='head-info-list clearfix']/li//a[@id='indexHeaderZhllBDP']/text()").extract_first()

        """企业名称"""
        company_name = response.xpath(
            "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[1]/div[2]/@title").extract_first()
        if company_name is not None and len(company_name) > 5:
            item["company_name"] = company_name

            """联系手机号"""
            item["tel"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[2]/div[2]/@title").extract_first()
            if not item["tel"]:
                item["tel"] = ""

            """注册号"""
            item["regis_number"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[4]/div[2]/@title").extract_first()

            social_credit_code = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[3]/div[2]/@title").extract_first()
            social_credit_code = "".join(social_credit_code.split())

            if social_credit_code is not None and len(social_credit_code) > 10:
                item["province"] = seach_sql(social_credit_code[2:4] + "0000")
                try:
                    item["city"] = seach_sql(social_credit_code[2:6] + "00")
                except:
                    item["city"] = ""
                if item["province"] == item["city"]:
                    item["city"] = ""
                try:
                    item["area"] = seach_sql(social_credit_code[2:8])
                except:
                    item["area"] = ""

                if item["area"] == item["city"] or item["area"] == item["province"]:
                    item["area"] = ""
            else:
                item["province"] = ""
                item["city"] = ""
                item["area"] = ""

            """法人代表"""
            item["legal_person"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[7]/div[2]/@title").extract_first()

            """注册资金(万)"""
            regis_money = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[8]/div[2]/@title").extract_first()
            if regis_money is not None:
                regis_money = "".join(regis_money.split())
                item["regis_money"] = handle_regis_money(regis_money)

            """公司类别"""
            item["type_one"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[9]/div[2]/text()").extract_first()

            """注册时间"""
            item["uptime"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[10]/div[2]/text()").extract_first()
            if item["uptime"] is not None:
                item["uptime"] = handle_uptime(item["uptime"])

            """登记机关"""
            item["registration_authority"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[12]/div[2]/text()").extract_first()

            # """注册地/地理位置"""
            # item["regis_area"] = response.xpath(
            #     "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[16]/div[2]/text()").extract_first()

            # if item["regis_area"] is not None:
            #     try:
            #         address = Address().handle_address(item["regis_area"])
            #         item["address_one"] = address[0]
            #         item["address_two"] = address[1]
            #     except:
            #         item["address_one"] = "0"
            #         item["address_two"] = "0"


            """经营范围"""
            item["operation"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[17]/div[2]/text()").extract_first()
            if item["operation"] is not None:
                item["operation"] = "".join(item["operation"].split())

            """营业期限"""
            business_time = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[11]/div[2]/text()").extract_first()
            if business_time is not None:
                business_time = "".join(business_time.split())

                if len(business_time) > 10:
                    item["business_start_time"] = handle_uptime(handle_business_time(business_time).group(1))
                    item["business_end_time"] = handle_uptime(handle_business_time(business_time).group(2))
                else:
                    item["business_start_time"] = handle_uptime(business_time)
                    item["business_end_time"] = 0
            try:
                icp = response.xpath(
                    "//div[@class='gsba_data']/div[6]//div[@class='kvs kvs_baxx']/div[5]/div[2]/@title").extract_first()
                if icp is not None:
                    icp = "".join(icp.split())
                    item["icp"] = icp
                else:
                    item["icp"] = ""
            except Exception as e:
                print(e)

            tag_1 = response.xpath(
                "//div[@class='tit']//div[@class='val ui-val-box clearfix']/div[1]/text()").extract_first()
            tag_2 = response.xpath(
                "//div[@class='tit']//div[@class='val ui-val-box clearfix']/div[2]/text()").extract_first()
            tag_3 = response.xpath(
                "//div[@class='tit']//div[@class='val ui-val-box clearfix']/div[3]/text()").extract_first()
            item["tags"] = handle_tag(tag_1) + "," + handle_tag(tag_2) + "," + handle_tag(tag_3)
            item["create_time"] = str(datetime.date.today())

            """注册地/地理位置"""
            item["regis_area"] = response.xpath(
                "//div[@class='gsba_data']/div[3]//div[@class='kvs']/div[16]/div[2]/text()").extract_first()

            if item["regis_area"] is not None:
                address_url = "http://api.map.baidu.com/geocoder/v2/?" \
                        "address={}&output=json&ak=xxxxxx".format(item["regis_area"])
                yield scrapy.Request(address_url,
                                     callback=self.parse_address,
                                     meta={"item": deepcopy(item)},
                                     dont_filter=True)


    def parse_address(self,response):
        item = deepcopy(response.meta["item"])
        dict_res = json.loads(response.text)
        if dict_res["status"] == 0:
            item["address_one"] = dict_res["result"]["location"]["lng"]
            item["address_two"] = dict_res["result"]["location"]["lat"]
            address_component_url = "http://api.map.baidu.com/geocoder/v2/?" \
                                    "callback=renderReverse&location={0},{1}&" \
                                    "output=json&ak=zxxxxxx".format(item["address_two"],
                                                                                             item["address_one"])
            yield scrapy.Request(address_component_url,
                                 callback=self.parse_address_comment,
                                 meta={"item": deepcopy(item)},
                                 dont_filter=True)
        else:
            item["address_one"] = "0"
            item["address_two"] = "0"
            yield item

    def parse_address_comment(self,response):
        item = deepcopy(response.meta["item"])
        response_data = re.match(r"renderReverse&&renderReverse\((.*)\)",response.text).group(1)
        dict_data = json.loads(response_data)
        item["province"] = dict_data["result"]["addressComponent"]["province"]
        item["city"] = dict_data["result"]["addressComponent"]["city"]
        item["area"] = dict_data["result"]["addressComponent"]["district"]
        yield item



