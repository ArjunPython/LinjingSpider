# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER
import pandas as pd
import redis


class ChangeinfoPipeline(object):
    def process_item(self, item, spider):
        return item


redis_db = redis.Redis(host='127.0.0.1', port=6379, db=8)
# redis_db = redis.Redis(host='127.0.0.1',password="caojun", port=6379, db=8)
redis_data_dict = "f_cha"

class DuplicatesPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()
        """删除全部key，保证key为0，不然多次运行时候hlen不等于0，刚开始这里调试的时候经常出错。"""
        """Redis Flushdb 命令用于清空当前数据库中的所有 key。"""
        redis_db.flushdb()
        """Redis Hlen 命令用于获取哈希表中字段的数量"""
        if redis_db.hlen(redis_data_dict) == 0:
            """从你的MySQL里提数据"""
            sql = "SELECT change_after FROM tp_change_info;"
            """读MySQL数据"""
            df = pd.read_sql(sql, self.conn)
            """#把每一条的值写入key的字段里"""
            for com in df['change_after'].get_values():
                """#把key字段的值都设为0，你要设成什么都可以，因为后面对比的是字段，而不是值"""
                """Redis Hset 命令用于为哈希表中的字段赋值 """
                redis_db.hset(redis_data_dict, com, 0)

    def process_item(self, item, spider):
        """Redis Hexists 命令用于查看哈希表的指定字段是否存在。"""
        if redis_db.hexists(redis_data_dict, item["contentAfter"]):
            """取item里的shuju和key里的字段对比，看是否存在，存在就丢掉这个item。不存在返回item给后面的函数处理"""
            raise DropItem("Duplicate item found: %s" % item)
        return item



class DynamicMysqlPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        data = {
            "company_name":item["company_name"],
            "change_project":item["changeItem"],
            "change_pre":item["contentBefore"],
            "change_after":item["contentAfter"],
            "change_time":item["changeTime"],
            "current_page":item['current_page'],
            "num":item['num']
        }
        table = "tp_change_info"

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

