# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-6-15 上午11:36



import pymysql
conn = pymysql.connect('xxxxxx', 'xxxxxx', 'xxxxxx', 'xxxxxx', charset="utf8")
cursor = conn.cursor()

def clear_sql():

    try:
        sql_1 = """select pid,position_job,manager_name,intro,is_hz from manager_info_copy WHERE is_hz=2;"""
        cursor.execute(sql_1)
        results = cursor.fetchall()
        sql_2 = """truncate table tp_manager_info_copy;"""
        cursor.execute(sql_2)
        print(results[0])
        for i in results:
            sql_3 = """INSERT INTO manager_info_copy (pid,position_job,manager_name,intro,is_hz) VALUES (%s,%s,%s,%s,%s)"""
            cursor.execute(sql_3,(i[0],i[1],i[2],i[3],i[4]))
            conn.commit()
    except Exception as e:
        pass

if __name__ == '__main__':
    clear_sql()


