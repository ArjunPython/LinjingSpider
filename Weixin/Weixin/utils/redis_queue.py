# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-10-8 下午3:06

from .weixin_request import WeixinRequest
from pickle import dumps,loads
from redis import StrictRedis


class RedisQueue(object):

    def __init__(self):
        self.db = StrictRedis(host="127.0.0.1",port=6379,password="xxxxxx",db=4)

    def add(self,request):
        if isinstance(request,WeixinRequest):
            return self.db.rpush("weixin",dumps(request))
        return False

    def pop(self):
        if self.db.llen("weixin"):
            return loads(self.db.lpop("weixin"))
        else:
            return False

    def empty(self):
        return self.db.llen("weixin") == 0
