import numpy as np
import pandas as pd
import math


def dynamicopinion_score(nowdate, timecountdict, allaverage, amount, staticrisk_num=0):
    '''动态舆论处理方法
    @nowdate: timestamp.当前日期
    @timecountdict: dict,当前日期过去一年的每天评论数量，包含当前日期
    @allaverage: int,过去一年每家平台负面评论个数平均数
    @amount: float,交易量平均数
    @staticrisk_num: int,此前所有静态负面舆论个数
    @return float,当天平台用户体验得分'''
    count = 0
    time_point = nowdate-3600*24*180
    count_today = 0.001
    timecount_list = []
    try:
        count_today = timecountdict[nowdate]
    except KeyError:
        pass
    for _ in timecountdict.index:
        count += timecountdict[_]
        timecount_list.append(timecountdict[_])
        if _ < time_point:
            time_point = _

    # print('count:', count)
    average = count/((nowdate-time_point)/3600/24) if count != 0 else 1
    # return 100/(1+math.exp((1-count_today/average)*(average/(allaverage*2)))) # sigmoid函数变体
    a = 100
    # print(staticrisk_num, allaverage, average)
    b = allaverage/average
    x = count_today*0.8+(staticrisk_num/amount/amount)
    c = average
    # print(a, b, c, x)
    return sigmoid(a,b,c,x)


def timecountlist_gen(endtime, timedict):
    '''计算方差所需参数获取方法
    @endtime int,截止时间，时间戳格式
    @timedict 数据库获取的数据'''
    tc_list = []
    for i in range(0, 365):
        try:
            tmp = timedict[endtime-3600*24*(i+1)]
            tc_list.append(tmp)
        except KeyError:
            tc_list.append(0)
    return tc_list


def allaverage_gen(comapnycount, total):
    '''大盘近一年动态舆论平均数,所有方法的一年设定为360天
    @companycount int,平台个数
    @total int,近一年总动态舆论数
    @return float,大盘近一年动态舆论平均数'''
    # print('cc, total: ', comapnycount, total)
    return total/comapnycount/180


def average_cal(datalist=[]):
    minvar = 99999999
    std_average = 0
    last_average = 0
    # print(datalist)
    for i in range(30, len(datalist)):
        tmp_list = datalist[i-30: i]
        tmp_nparr = np.array(tmp_list)
        tmp_std = np.std(tmp_nparr)
        if tmp_std < minvar and tmp_std > 0.1:
            minvar = tmp_std
            std_average = np.average(tmp_nparr)
        if i == len(datalist)-1:
            last_average = np.average(tmp_nparr)
    # print('std_av, minvar: ', std_average, minvar)
    return std_average, last_average


def dynamicopinion_score_2(percent=0.5, std_average=0, average=0):
    a = 100
    b = [3, 0.1]
    x = [percent, (average+1)/(std_average+1)]
    c = 1.6
    # print('percent, average, std_average: ', percent, average, std_average)
    return sigmoid(a, b, c, x)


def sigmoid(a=100, b=[0], c=0, x=[0]):
    '''sigmoid函数变体
    @a: 振幅
    @b: 缓急
    @c: 偏置
    @x: 当天负评个数与平均水平比值
    @return: 归一化分数'''
    param = np.dot(b, x)-c
    return a/(1+math.exp(-param))