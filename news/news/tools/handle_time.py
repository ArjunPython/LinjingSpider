# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-5-10 下午2:18


import datetime
def handle_time():
    start = '20170501'
    end = '20180510'
    datestart = datetime.datetime.strptime(start, '%Y%m%d')
    dateend = datetime.datetime.strptime(end, '%Y%m%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        # print(datestart.strftime('%Y%m%d'))
        return datestart.strftime('%Y%m%d')

# print(handle_time())



import json
import requests
from fake_useragent import UserAgent

# def handle_tag(comment):
#     ua = UserAgent()
#     headers = {"User-Agent":ua.random}
#     # url = "http://172.16.20.249:5010/newsalynasis"
#     data = {"sentence":comment}
#     response = requests.post(url,data=data,headers=headers,verify=False)
#     json_data = response.content.decode()
#     # print(json_data)
#     dict_data = json.loads(json_data)["result"]
#     return dict_data[0]

import sys
sys.path.append(r"/home/arjun/Desktop/yun_spider")
from emotionAlynasis import mainparser
def handle_tag(title):
    score_data = mainparser.news_alynasis(sentence=title)
    return score_data

if __name__ == '__main__':
    tag = handle_tag("整个3月份，又雷了37家P2P网贷平台，22家卷钱跑路了！")
    print(tag)


