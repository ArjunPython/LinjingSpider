# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



from twisted.enterprise import adbapi
import pymysql
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER


conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
cursor = conn.cursor()

class ManagerinfoPipeline(object):
    def process_item(self, item, spider):
        return item



class DynamicMysqlPipeline(object):

    # def clear_sql(self):
    #     try:
    #         sql_1 = """select pid,position_job,manager_name,intro,is_hz from tp_manager_info WHERE is_hz=2;"""
    #         cursor.execute(sql_1)
    #         results = cursor.fetchall()
    #         sql_2 = """truncate table tp_manager_info;"""
    #         cursor.execute(sql_2)
    #         for i in results:
    #             sql_3 = """INSERT INTO tp_manager_info (pid,position_job,manager_name,intro,is_hz) VALUES (%s,%s,%s,%s,%s)"""
    #             cursor.execute(sql_3, (i[0], i[1], i[2], i[3], i[4]))
    #             conn.commit()
    #     except Exception as e:
    #         pass

    def __init__(self):
        self.conn =pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        data = {
            "pid": item["pid"],
            "mi_info": item["comment"],
        }
        table = "tp_manager_info"
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
