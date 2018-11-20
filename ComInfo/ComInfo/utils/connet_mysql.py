# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-4-25 上午10:36

import pymysql
from settings import MYSQL_DBNAME,MYSQL_HOST,MYSQL_PASSWORD,MYSQL_USER
conn = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DBNAME, charset="utf8")
cursor = conn.cursor()

def seach_sql(name):
    sql = """select name from new_areas where code='%s'""" % name
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        return results[0]
    except Exception as e:
        sql = """select name from old_areas where code='%s'""" % name
        cursor.execute(sql)
        results = cursor.fetchone()
        return results[0]


if __name__ == '__main__':
    seach_sql("xxx")



