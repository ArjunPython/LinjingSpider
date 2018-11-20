# -*- coding: utf-8 -*-
import datetime
import json
import scrapy
import time

class TpDataYunSpider(scrapy.Spider):
    name = 'tp_data_yun'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://shuju.wdzj.com/plat-data-custom.html']

    custom_settings={"ITEM_PIPELINES":{
   'OperationData.pipelines.MysqlPipeline': 200,}
                    }

    def start_requests(self):
        url = "https://shuju.wdzj.com/plat-data-custom.html"
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        ye = str(today - oneday)

        # nowTime = datetime.datetime.now().strftime('%Y%m%d')
        # start = '2018-07-05'
        # end = '2018-07-07'
        # datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
        # dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
        # while datestart < dateend:
        #     datestart += datetime.timedelta(days=1)
        #     ye = datestart.strftime('%Y-%m-%d')
        yield scrapy.FormRequest(
            url=url,
            formdata={"type": "0",
                      "shujuDate": "2018-07-302018-07-30"},
            callback=self.parse)

    def parse(self, response):
        data_list = json.loads(response.body.decode())
        if len(data_list) > 0:
            for data in data_list:
                item = {}
                """网贷名称"""
                item["platName"] = data["platName"]
                """数据更新时间"""
                endDate = data["endDate"]
                timeArray = time.strptime(endDate, "%Y-%m-%d")
                item["uptime"] = int(time.mktime(timeArray))

                # """成交量"""
                # item["amount"] = data["amount"]
                # """平均预期收益率(%)"""
                # item["incomeRate"] = data["incomeRate"]
                # """平均借款期限(月)"""
                # item["loanPeriod"] = data["loanPeriod"]
                # """投资人数(人)"""
                # item["bidderNum"] = data["bidderNum"]
                # """借款人数(人)"""
                # item["borrowerNum"] = data["borrowerNum"]
                # """资金净流入(万元)"""
                # item["netInflowOfThirty"] = data["netInflowOfThirty"]
                # """待还余额(万元)"""
                # item["stayStillOfTotal"] = data["stayStillOfTotal"]
                # """人均投资金额(万元)"""
                # item["avgBidMoney"] = data["avgBidMoney"]
                # """人均借款金额(万元)"""
                # item["avgBorrowMoney"] = data["avgBorrowMoney"]
                # """借款标数(个)"""
                # item["totalLoanNum"] = data["totalLoanNum"]

                """满标用时（分）"""
                item["fullloanTime"] = data["fullloanTime"]

                """前十大投资人待收金额占比"""
                item["top10DueInProportion"] = data["top10DueInProportion"]
                """前十大借款人待收金额占比"""
                item["top10StayStillProportion"] = data["top10StayStillProportion"]

                #
                # """运营时间(月)"""
                # item["timeOperation"] = data["timeOperation"]
                # """注册金额"""
                # item["regCapital"] = data["regCapital"]

                yield item
                # print(item)