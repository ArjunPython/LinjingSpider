# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-4-20 上午9:44
import time

def handle_uptime(t):
    timeArray = time.strptime(t, "%Y-%m-%d")
    return int(time.mktime(timeArray))
