# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-6-22 下午1:47
import time
import re

def datestamptrans(date_time):
    year = ""
    month = ""
    day = ""
    str_date = str(date_time)
    timelist = re.split(r'[^0-9]', str_date)
    if len(timelist[0]) == 4:
        year = timelist[0]
        month = timelist[1] if len(timelist[1]) == 2 else '0' + timelist[1]
        day = timelist[2]
    elif len(timelist[0]) == 2:
        year = 2018
        month = timelist[0] if len(timelist[0])==2 else '0' + timelist[1]
        day = timelist[1] if len(timelist[1])==2 else '0' + timelist[1]
    return int(time.mktime(time.strptime(str(year)+'-'+str(month)+'-'+str(day), "%Y-%m-%d")))


import sys
sys.path.append(r"/home/jun/Desktop/yun_spider")
from emotionAlynasis import mainparser
def handle_tag(title):
    score_data = mainparser.news_alynasis(sentence=title)
    return score_data

if __name__ == '__main__':
    # tag = handle_tag("整个3月份，又雷了37家P2P网贷平台，22家卷钱跑路了！")
    # print(tag)
    t = datestamptrans("2018年10月9日")
    print(t)
