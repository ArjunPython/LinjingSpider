# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-4-25 上午10:36

import pymysql
from ..settings import MYSQL_HOST_1, MYSQL_USER_1, MYSQL_PASSWORD_1, MYSQL_DBNAME_1

class Search(object):
    def __init__(self):
        self.conn = pymysql.connect(MYSQL_HOST_1, MYSQL_USER_1, MYSQL_PASSWORD_1, MYSQL_DBNAME_1, charset="utf8")
        self.cursor = self.conn.cursor()

    def search_id_sql(self,name):
        try:
            sql = """select id from com_info where company_name='%s'""" % name
            self.cursor.execute(sql)
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            print(e)
            # finally:
            #     conn.close()  #关闭连接


