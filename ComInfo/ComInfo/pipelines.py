# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import signals
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER
from ComInfo.utils.bank_score import review_score


class CominfoPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def process_item(self, item, spider):

        insert_sql = """
            insert into tp_com_info(net_name,company_name,logo,com_type,uptime,regis_money
                                    ,average_annual_income,url,tel,legal_person,regis_area,address_one
                                    ,address_two,regis_number,province,city,area,operation,business_start_time
                                    ,business_end_time,registration_authority,icp,tags,status,icp_number,bank
                                    ,bank_time,create_time,event_time,association
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            regis_money=VALUES(regis_money),average_annual_income=VALUES(average_annual_income)
            ,tags=VALUES(tags),status=VALUES(status),icp_number=VALUES(icp_number),bank=VALUES(bank)
            ,bank_time=VALUES(bank_time),event_time=VALUES(event_time),association=VALUES(association)
        """
        try:
            if self.cursor.execute(insert_sql, (item["net_name"], item["company_name"], item["logo"],item["type_one"]
                                    ,item["uptime"],item["regis_money"],item["average_annual_income"],item["url"],item["tel"]
                                    ,item["legal_person"],item["regis_area"],item["address_one"],item["address_two"],item["regis_number"]
                                    ,item["province"],item["city"],item["area"],item["operation"],item["business_start_time"]
                                    ,item["business_end_time"],item["registration_authority"],item["icp"],item["tags"],item["status"]
                                    ,item["icp_number"], item["bank"], item["bank_time"]
                                    ,item["create_time"],item["event_time"],item["association"])):
                print("successful")
                self.conn.commit()
        except Exception as e:
            print("*"*100)
            print(e)
            print("*" * 100)
            print("Failed")
            self.conn.rollback()

    def spider_closed(self, spider):
        review_score()
        print("银行打分更新完成")



class DynamicMysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):

        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        data = {
            "net_name":item["net_name"],
            "company_name":item["company_name"],
            "logo":item["logo"],
            "com_type":item["type_one"],
            "uptime":item["uptime"],
            "regis_money":item["regis_money"],
            "average_annual_income":item["average_annual_income"],
            "url":item["url"],
            "tel":item["tel"],
            "legal_person":item["legal_person"],
            "regis_area":item["regis_area"],
            "address_one":item["address_one"],
            "address_two":item["address_two"],
            "regis_number":item["regis_number"],
            "province":item["province"],
            "city":item["city"],
            "area":item["area"],
            "operation":item["operation"],
            "business_start_time":item["business_start_time"],
            "business_end_time":item["business_end_time"],
            "registration_authority":item["registration_authority"],
            "icp":item["icp"],
            "tags":item["tags"],
            "status":item["status"],
            "icp_number":item["icp_number"],
            "bank":item["bank"],
            "bank_time":item["bank_time"],
            "create_time":item["create_time"],

        }
        table = "tp_com_info"
        keys = ",".join(data.keys())
        values = ",".join(['%s']*len(data))

        insert_sql = """
            insert into {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE """\
            .format(table=table, keys=keys, values=values)

        update = ",".join(["{key}= %s".format(key=key) for key in data])
        insert_sql += update
        try:
            if self.cursor.execute(insert_sql, tuple(data.values())*2):
                print("successful")
                self.conn.commit()
        except Exception as e:
            print("Failed")
            self.conn.rollback()

