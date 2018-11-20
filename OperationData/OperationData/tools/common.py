# -*- coding: utf-8 -*-

import hashlib
import time

def get_md5(name):
    if isinstance(name, str):
        name = name.encode("utf-8")
    m = hashlib.md5()
    m.update(name)
    return m.hexdigest()

def handle_uptime(t):

    timeArray = time.strptime(t, "%Y-%m-%d")
    return int(time.mktime(timeArray))

def handle_times(t):
    timeStamp = int(time.mktime(time.strptime(t, "%Y-%m-%d %H:%M:%S")))
    Array = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d",Array)
    y = time.strptime(otherStyleTime, "%Y-%m-%d")
    return int(time.mktime(y))






