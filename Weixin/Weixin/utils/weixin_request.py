# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-10-8 下午2:51

from requests import Request


TIMEOUT = 10

class WeixinRequest(Request):

    def __init__(self,url,callback,
                 method='GET',headers=None,
                 need_proxy=False,fail_time=0,timeout=TIMEOUT):
        Request.__init__(self,method,url,headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout