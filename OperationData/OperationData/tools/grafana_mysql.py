# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-9-18 上午11:57


import pymysql
import time

class Search(object):
    def __init__(self):
        # self.conn = pymysql.connect("xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx", charset="utf8")
        self.conn = pymysql.connect("xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx", charset="utf8")
        self.cursor = self.conn.cursor()
    def search_sql(self):
        # before_item = 0
        sql_1 = """select count(*) from tp_comment_info"""
        self.cursor.execute(sql_1)
        res = self.cursor.fetchone()
        before_item = res[0]
        while True:
            try:
                sql = """select count(*) from tp_comment_info"""
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                current_item = result[0]
                print(current_item)
                self.cursor.execute("insert into tp_item_per_min VALUES (now(), %s)" % (current_item-before_item))
                self.cursor.execute("insert into tp_item_total VALUES (now(), %s)" % current_item)
                self.conn.commit()
                before_item = current_item

            except Exception as e:
                print(e)
                print("查询错误")
            time.sleep(60)


if __name__ == '__main__':
    gra = Search()
    gra.search_sql()