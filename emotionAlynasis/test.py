from emotionAlynasis import dynamic
import pymysql
import time
import numpy as np
import math

# thedate = int(time.time())-3600*24
# def singlescore_exeute(company_id=0, thedate=0, company_name='', isall=False):
#     timelist = []
#     total = 0
#     company_count = 0
#     connection = pymysql.connect(host='xxxxxx',
#                              user='xxxxxx',
#                              password='xxxxxx',
#                              db='xxxxxx',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#     try:
#         with connection.cursor() as cursor:
#             # if isall:
#             #     timelist_sql = 'SELECT `comm_time` FROM `tp_comment_info` WHERE `comm_score` = 0 AND `comm_time` > %s-3600*20*60'
#             #     cursor.execute(timelist_sql, thedate)
#             # else:
#             timelist_sql = 'SELECT `comm_time` FROM `tp_comment_info` WHERE `comm_score` = 0 AND `comm_time` > %s-3600*24*180 AND `comm_time` < %s AND pid = %s'
#             cursor.execute(timelist_sql, (thedate, thedate+100, company_id))
#             timedict = cursor.fetchall()
#             for _t in timedict:
#                 timelist.append(_t['comm_time'])
#             companycount_sql = 'SELECT COUNT(`id`) AS c FROM `tp_com_info`'
#             cursor.execute(companycount_sql)
#             company_count = cursor.fetchall()[0]['c']
#             total_sql = 'SELECT COUNT(`id`) AS c FROM `tp_comment_info` WHERE `comm_score` = 0 AND `comm_time` > %s-3600*24*180 AND `comm_time` < %s '
#             cursor.execute(total_sql, (thedate, thedate+100))
#             total = cursor.fetchall()[0]['c']
#             news_staticrisk_sql = 'SELECT COUNT(`id`) as n FROM `tp_news` WHERE `news_time` < %s AND `content` LIKE %s AND (`content` LIKE %s OR `content` LIKE %s OR `content` LIKE %s OR `content` LIKE %s)'
#             cursor.execute(news_staticrisk_sql, (thedate+100, '%'+company_name+'%', '%自融%', '%非吸%', '%伪国资%', '%假国资%'))
#             staticrisk_num = cursor.fetchall()[0]['n'] * 2
#             comment_staticrisk_sql = 'SELECT COUNT(`id`) as n FROM `tp_comment_info` WHERE pid = %s AND `comm_resource` = "网贷天眼" AND `comm_time` < %s AND `comm_score` = 0 AND (`comm_info` LIKE %s OR `comm_info` LIKE %s OR `comm_info` LIKE %s OR `comm_info` LIKE %s)'
#             cursor.execute(comment_staticrisk_sql, (company_id, thedate+100, '%自融%', '%非吸%', '%伪国资%', '%假国资%'))
#             staticrisk_num += cursor.fetchall()[0]['n'] * 10       
#             amount_sql = 'SELECT `net_name`, SUM(`amount`)/COUNT(`net_name`) as m FROM `tp_com_info` LEFT JOIN `tp_operation_data` ON `net_name` = `platName` WHERE `net_name` = %s'
#             cursor.execute(amount_sql, company_name)
#             amount = str(cursor.fetchall()[0]['m'])
#             if amount.isdecimal():
#                 pass
#             else:
#                 amount = 10
#         connection.commit()
#     finally:
#         connection.close()

#     timecount_dict = dynamic.timecountlist_gen(timelist)
#     all_average = dynamic.allaverage_gen(company_count, total)
#     score = dynamic.dynamicopinion_score(thedate, timecount_dict, all_average, amount, staticrisk_num)
#     return score


def singlescore_exeute_2(company_id=0, thedate=0, company_name='', isall=False):
    total = 0
    percent = 0
    timedict = dict()
    connection = pymysql.connect(host='xxxxxx',
                                      user='xxxxxx',
                                      password='xxxxxx',
                                      db='xxxxxx',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # if isall:
            #     timelist_sql = 'SELECT `comm_time` FROM `tp_comment_info` WHERE `comm_score` = 0 AND `comm_time` > %s-3600*20*60'
            #     cursor.execute(timelist_sql, thedate)
            # else:
            ps_count_sql = 'SELECT COUNT(`id`) as c FROM `tp_comment_info`' \
                           ' WHERE `pid` = %s AND `comm_score` = 0 ' \
                           'AND `comm_time` < %s AND `comm_time` > %s' if not isall else  \
                              'SELECT COUNT(`id`) as c FROM `tp_comment_info`' \
                              ' WHERE `comm_score` = 0 ' \
                              'AND `comm_time` < %s AND `comm_time` > %s'
            if not isall:
                cursor.execute(ps_count_sql, (company_id, thedate+100, thedate-3600*24*30))
            else:
                cursor.execute(ps_count_sql, (thedate + 100, thedate - 3600 * 24 * 30))
            ps = cursor.fetchall()[0]['c']
            total_count_sql = 'SELECT COUNT(`id`) as c FROM `tp_comment_info`' \
                              ' WHERE `pid` = %s AND `comm_time` < %s AND `comm_time` > %s' if not isall else  \
                              'SELECT COUNT(`id`) as c FROM `tp_comment_info`' \
                              ' WHERE `comm_time` < %s AND `comm_time` > %s'
            if not isall:
                cursor.execute(total_count_sql, (company_id, thedate+100, thedate-3600*24*30))
            else:
                cursor.execute(total_count_sql, (thedate + 100, thedate - 3600 * 24 * 30))
            total = cursor.fetchall()[0]['c']
            timedict_sql = 'SELECT COUNT(`id`) as c, `comm_time` FROM `tp_comment_info` ' \
                           'WHERE `pid` = %s AND `comm_score` = 0 AND `comm_time` < %s AND `comm_time` > %s ' \
                           'GROUP BY `comm_time`' if not isall else 'SELECT COUNT(`id`) as c, `comm_time` FROM `tp_comment_info` ' \
                           'WHERE `comm_score` = 0 AND `comm_time` < %s AND `comm_time` > %s ' \
                           'GROUP BY `comm_time`'
            if not isall:
                cursor.execute(timedict_sql, (company_id, thedate+100, thedate-3600*24*365))
            else:
                cursor.execute(timedict_sql, (thedate + 100, thedate - 3600 * 24 * 365))
            result = cursor.fetchall()
            for _r in result:
                timedict[_r['comm_time']] = _r['c']
            timelist = dynamic.timecountlist_gen(thedate, timedict)
            std_average, average = dynamic.average_cal(timelist)
            if ps == 0:
                percent = 0
            else:
                percent = ps/total
        connection.commit()
    finally:
        connection.close()
    # print(percent, std_average, average)
    score = dynamic.dynamicopinion_score_2(percent=percent, std_average=std_average, average=average)
    # print(percent, std_average, average, score)
    return score


def getscorelist(company_id=0, company_name='unknown'):
    datelist = []
    scorelist = []
    nowtime = time.localtime()
    year = nowtime.tm_year
    month = nowtime.tm_mon
    day = nowtime.tm_mday
    dt = str(year) + '-' + str(month) + '-' + str(day)
    nowdate = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))-180*3600*24
    for i in range(180):
        score = 0.0
        datelist.append(nowdate)
        if company_id != '0' and company_id != 0:
            score = singlescore_exeute_2(company_id, thedate=nowdate, company_name=company_name)
        else:
            print('大盘数据处理')
            score = singlescore_exeute_2(company_id, thedate=nowdate, company_name=company_name, isall=True)
            # print(score)
        if type(eval(str(score))) == float:
            pass
        else:
            score = 0
            # print('notdecimal')
        scorelist.append(score)
        nowdate += 3600*24
    # print(scorelist)
    return scorelist, datelist


def getscorelist_mysql(company_id=0, company_name='unknown'):
    datelist = []
    scorelist = []
    nowtime = time.localtime()
    year = nowtime.tm_year
    month = nowtime.tm_mon
    day = nowtime.tm_mday
    dt = str(year) + '-' + str(month) + '-' + str(day)
    nowdate = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))-180*3600*24
    connection = pymysql.connect(host='xxxxxx',
                                      user='xxxxxx',
                                      password='xxxxxx',
                                      db='xxxxxx',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
                sql ='SELECT `score`, `createtime` FROM `tp_opinion_score` WHERE `pid` = %s AND `createtime` < %s ORDER BY `createtime` ASC'
                cursor.execute(sql, (company_id, nowdate+180*3600*24))
                result = cursor.fetchall()
                for _r in result:
                    datelist.append(time.strftime("%Y-%m-%d", time.localtime(int(_r['createtime']))))
                    scorelist.append(float(_r['score']))
        connection.commit()
    finally:
        connection.close()
    return scorelist, datelist



def getcomdata():
    com_list = []
    id_list = []
    connection = pymysql.connect(host='xxxxxx',
                                      user='xxxxxx',
                                      password='xxxxxx',
                                      db='xxxxxx',
                                      charset='xxxxxx',
                                      cursorclass=pymysql.cursors.DictCursor)
    comdata_sql = 'SELECT `id`, `net_name` FROM `tp_com_info` WHERE `net_name` IS NOT NULL ORDER BY `net_name`'
    try:
        with connection.cursor() as cursor:
            cursor.execute(comdata_sql)
            data_result = cursor.fetchall()
            for _d in data_result:
                com_list.append(_d['net_name'])
                id_list.append(_d['id'])
    finally:
        connection.close()
    return com_list, id_list


def getscorelist_perday(company_id=0, company_name='unknown', thedate = 0):
    if thedate == 0:
        nowtime = time.localtime()
        year = nowtime.tm_year
        month = nowtime.tm_mon
        day = nowtime.tm_mday
        dt = str(year) + '-' + str(month) + '-' + str(day)
        nowdate = int(time.mktime(time.strptime(dt, "%Y-%m-%d")))
    else:
        nowdate = thedate
    score = 0.0
    if company_id != '0' and company_id != 0:
        score = singlescore_exeute_2(company_id, thedate=nowdate, company_name=company_name)
    else:
        print('大盘数据处理')
        score = singlescore_exeute_2(company_id, thedate=nowdate, company_name=company_name, isall=True)
        # print(score)
    if type(eval(str(score))) == float:
        pass
    else:
        score = 0
        # print('notdecimal')
    # print(scorelist)
    return score
