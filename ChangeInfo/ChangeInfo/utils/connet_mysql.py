# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-4-25 上午10:36

import pymysql
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER

class Search(object):
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
        self.cursor = self.conn.cursor()
    def search_sql(self, time):
        try:
            sql = """select company_name from com_info where create_time='%s'""" % time
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            print("查询错误")
        results = self.cursor.fetchall()
        com_list = []
        for result in results:
            li = result[0]
            com_list.append(li)
        return com_list



