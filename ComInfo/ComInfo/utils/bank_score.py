# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-7-18 下午4:24


import pymysql
import pandas as pd


def review_score():
    bank_data = pd.read_excel('./ComInfo/utils/bank.xlsx', names=['bank', 'score'])
    bank_data.index = bank_data['bank']
    all_dict = bank_data.to_dict()
    cnx = pymysql.connect(user='admin', password='xxxxxx',
                                  host='xxxxxx',
                                  database='xxxxxx',charset="utf8")
    cursor = cnx.cursor()
    query = 'SELECT a.id,a.bank from tp_com_info a where a.is_third_custody=50'
    cursor.execute(query)
    result = cursor.fetchall()
    for value in result:
        name = value[0]
        bank1 = value[1]
        bank = 50
        if bank1 != None:
            bank_score = all_dict['score'].get(bank1)
            if bank_score != None:
                bank = bank_score
        update_score = 'UPDATE tp_com_info  SET is_third_custody =\'' + str(bank) + '\' WHERE id =' + str(name)

        cursor.execute(update_score)
    cursor.close()

if __name__ == '__main__':
    # bank_score_up()
    review_score()
