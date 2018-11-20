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
            sql = """select company_name from tp_com_info where create_time='%s'""" % time
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

    def search_id_sql(self,name):
        try:
            sql = """select id from tp_com_info where net_name='%s'""" % name
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            print(e)
            # finally:
            #     conn.close()  #关闭连接

if __name__ == '__main__':
    pass
    # caojun = Search()
    # a = caojun.search_sql("2018-07-11")
    # print(a)



