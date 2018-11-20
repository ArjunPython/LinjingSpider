# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER


class OperationdataPipeline(object):
    def process_item(self, item, spider):
        return item


class DynamicMysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == "tp_operation_data":
            data = {
                "platName":item["platName"],
                "endDate":item["endDate"],
                "amount":item["amount"],
                "incomeRate":item["incomeRate"],
                "loanPeriod":item["loanPeriod"],
                "bidderNum":item["bidderNum"],
                "borrowerNum":item["borrowerNum"],
                "netInflowOfThirty":item["netInflowOfThirty"],
                "stayStillOfTotal":item["stayStillOfTotal"],
                "avgBidMoney":item["avgBidMoney"],
                "avgBorrowMoney":item["avgBorrowMoney"],
                "totalLoanNum":item["totalLoanNum"],
                "fullloanTime":item["fullloanTime"],
                "top10DueInProportion" :item["top10DueInProportion"],
                "top10StayStillProportion" :item["top10StayStillProportion"],
                "timeOperation" :item["timeOperation"],
                "regCapital" :item["regCapital"]
            }
            table = "tp_operation_data"
            self.do_insert(data,table)

        elif spider.name == "tp_experience_analysis":
            data = {
              "name":item["name"],
              "comments_num":item["comments_num"],
              "withdrawal_speed":item["withdrawal_speed"],
              "funds_idle":item["funds_idle"],
              "customer_service":item["customer_service"],
              "experience":item["experience"],
              "recommend":item["recommend"],
              "creat_date":item["creat_date"],
            }

            table = "tp_experience_analysis"
            self.do_insert(data, table)

        elif spider.name == "tp_platform_background":
            data = {
                "name": item["name"],
                "company_name": item["company_name"],
                "tag": item["tag"],
                "province": item["province"],
                "city": item["city"],
                "time_online": item["time_online"],
                "registered_capital": item["registered_capital"],
                "paid_capital": item["paid_capital"],
                "equity_listing": item["equity_listing"],
                "bank": item["bank"],
                "financing": item["financing"],
                "regulatory_association": item["regulatory_association"],
                "icp_num": item["icp_num"],
                "claims": item["claims"],
                "guarantee_institution": item["guarantee_institution"],
                "status": item["status"],
                "creat_date": item["creat_date"],
            }

            table = "tp_platform_background"
            self.do_insert(data, table)


        elif spider.name == "tp_executives_costs":
            data = {
              "name":item["name"],
              "person_name":item["person_name"],
              "introduction":item["introduction"],
              "management_fee":item["management_fee"],
              "withdraw_fee":item["withdraw_fee"],
              "vip_fee":item["vip_fee"],
              "creat_date":item["creat_date"],
            }

            table = "tp_executives_costs"
            self.do_insert(data, table)
        elif spider.name == "tp_operations_ratings":
            data = {
                "name": item["name"],
                "rat_num": item["rat_num"],
                "creat_date": item["creat_date"],
            }

            table = "tp_operations_ratings"
            self.do_insert(data, table)


    def do_insert(self,data,table):

        keys = ",".join(data.keys())
        values = ",".join(['%s']*len(data))

        insert_sql = """
            insert into {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE """\
            .format(table=table,keys=keys,values=values)

        update = ",".join(["{key}= %s".format(key=key) for key in data])
        insert_sql += update
        try:
            if self.cursor.execute(insert_sql, tuple(data.values())*2):
                print("successful")
                self.conn.commit()
        except Exception as e:
            print(e)
            print("Failed")
            self.conn.rollback()



class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect("xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx", charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == "tp_data_yun":
            data = {
                "plat_name":item["platName"],
                "uptime":item["uptime"],
                # "amount":item["amount"],
                # "incomeRate":item["incomeRate"],
                # "loanPeriod":item["loanPeriod"],
                # "bidderNum":item["bidderNum"],
                # "borrowerNum":item["borrowerNum"],
                # "netInflowOfThirty":item["netInflowOfThirty"],
                # "stayStillOfTotal":item["stayStillOfTotal"],
                # "avgBidMoney":item["avgBidMoney"],
                # "avgBorrowMoney":item["avgBorrowMoney"],
                # "totalLoanNum":item["totalLoanNum"],
                "fullloanTime":item["fullloanTime"],
                "top10DueInProportion" :item["top10DueInProportion"],
                "top10StayStillProportion" :item["top10StayStillProportion"],
                # "timeOperation" :item["timeOperation"],
                # "regCapital" :item["regCapital"]
            }
            table = "tp_operation_data"
            self.do_insert(data,table)

    def do_insert(self, data, table):

        keys = ",".join(data.keys())
        values = ",".join(['%s'] * len(data))

        insert_sql = """
              insert into {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE """ \
            .format(table=table, keys=keys, values=values)

        update = ",".join(["{key}= %s".format(key=key) for key in data])
        insert_sql += update
        try:
            if self.cursor.execute(insert_sql, tuple(data.values()) * 2):
                print("successful")
                self.conn.commit()
        except Exception as e:
            print(e)
            print("Failed")
            self.conn.rollback()


class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST_1"],
            db=settings["MYSQL_DBNAME_1"],
            user=settings["MYSQL_USER_1"],
            passwd=settings["MYSQL_PASSWORD_1"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


