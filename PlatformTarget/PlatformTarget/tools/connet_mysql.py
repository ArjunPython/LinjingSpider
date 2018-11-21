# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-4-25 上午10:36

import pymysql
from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME


class Search(object):
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()

    def search_id_sql(self,name):
        try:
            sql = """select id from com_info where net_name='%s'""" % name
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            print(e)
    def search_net_name(self):
        try:
            name_list = []
            sql = """SELECT net_name FROM com_info WHERE status not in('警方介入','跑路平台','平台清盘','平台诈骗','')"""
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for r in results:
                name_list.append(r[0])
            return name_list
        except Exception as e:
            print(e)
if __name__ == '__main__':
    s = Search().search_net_name()
    print(s)


