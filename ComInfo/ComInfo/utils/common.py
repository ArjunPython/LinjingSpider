# -*- coding: utf-8 -*-

import hashlib

import time
import re

def get_md5(name):
    if isinstance(name, str):
        name = name.encode("utf-8")
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()


def handle_uptime(t):
    try:
        timeArray = time.strptime(t, "%Y-%m-%d")
        return int(time.mktime(timeArray))
    except Exception as e:
        return "无数据显示"


def handle_business_time(s):
    ret = re.match(r"(.*)至(.*)", "".join(s.split()))
    return ret


def handle_regis_money(m):

    """8000.000万人民币"""
    """5000.000000万"""
    ret_1 = re.match(r"(\d+)\.(.*)万(.*)", m)
    if ret_1:
        return int(ret_1.group(1))
    ret_3 = re.match(r"(\d+)万(.*)", m)
    if ret_3:
        return int(ret_3.group(1))
    ret_4 = re.match(r"\(人民币\)(\d+)\.(.*)万元", m)
    if ret_4:
        return int(ret_4.group(1))
    ret_5 = re.match(r"\(人民币\)(\d+)万元", m)
    if ret_5:
        return int(ret_5.group(1))

    # if ret_1:
    #     return int(ret_1.group(1))
    # elif ret_3:
    #     return int(ret_3.group(1))
    # elif ret_4:
    #     return int(ret_4.group(1))
    # elif ret_5:
    #     return int(ret_5.group(1))




def handle_area(m):
    try:
        cc = re.match(r"(.*?)省(.*?)市(.*?)区(.*?)", m)
        dd = re.match(r"(.*?)市(.*?)区(.*?)", m)
        ff = re.match(r"(.*?)市(.*?)", m)
        if cc:
            result = cc.group(2) + "市" + cc.group(3) + "区"
            return result
        elif dd:
            result = dd.group(1) + "市" + dd.group(2) + "区"
            return result
        elif ff:
            result = ff.group(1) + "市"
            return result
    except Exception as e:

        return "杭州市"


def handle_tag(t):
    if t is not None:
        g = "".join(t.split())

        return g
    else:
        return ""


def handle_class_title(title):

    if "txkn" in title:
        return "提现困难"
    elif "ptsl" in title:
        return "平台失联"
    elif "jfjr" in title:
        return "警方介入"
    elif "plpt" in title:
        return "平台跑路"
    elif "ptzp" in title:
        return "平台诈骗"
    elif "ztfb" in title:
        return "暂停发标"
    elif "zzyy" in title:
        return "终止运营"
    elif "lxtc" in title:
        return "良性退出"
    elif "zypt" in title:
        return "争议平台"
    elif "ptqp" in title:
        return "平台清盘"


if __name__ == '__main__':
    handle_business_time("2014-08-15 至 9999-09-09")






