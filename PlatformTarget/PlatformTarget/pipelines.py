# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import signals
from twisted.enterprise import adbapi
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER
from settings import MYSQL_DBNAME_1,MYSQL_HOST_1,MYSQL_PASSWORD_1,MYSQL_USER_1
from tools.BloomCheck import BloomCheckFunction
from emailSender import emailSender

# bof = BloomCheckFunction()


class PlatformtargetPipeline(object):
    def process_item(self, item, spider):
        return item



class MysqlTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
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



class DynamicMysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        data = {

        }
        table = ""

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
                # return item
        except Exception as e:
            print(e)
            print("Failed")
            self.conn.rollback()


class MysqlPipeline(object):

    def __init__(self):
        # self.conn = pymysql.connect(MYSQL_HOST_1, MYSQL_USER_1, MYSQL_PASSWORD_1, MYSQL_DBNAME_1, charset="utf8")
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()
        self.bof = BloomCheckFunction()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def process_item(self, item, spider):

        if self.bof.process_item(item["comm_info"]):
            insert_sql = """
                insert into tp_comment_info(comm_name, comm_resource, comm_info, comm_time, pid, comm_score, comm_score_n, update_date
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            """
            try:
                if self.cursor.execute(insert_sql, (item["comm_name"], item["comm_resource"], item["comm_info"],item["comm_time"]
                                        ,item["pid"],item["comm_score"],item["comm_score_n"]
                                        ,item["update_date"])):
                    print("successful")
                    self.conn.commit()
            except Exception as e:
                print("*"*100)
                print(e)
                print("*" * 100)
                print("Failed")
                self.conn.rollback()
        else:
            print("过滤器过滤.........2")

    def spider_closed(self, spider,reason):
        self.bof.save_bloom_file()
        print("%s爬虫完成，数据保存成功" % spider.name)

