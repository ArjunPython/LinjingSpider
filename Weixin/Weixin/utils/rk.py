#!/usr/bin/env python
# coding:utf-8
import os

import requests
from hashlib import md5
import time
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode("utf-8")).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    # sys.path.append(os.path.dirname(sys.path[0]))
    pass
    # ct = time.time()
    # data_head = time.strftime("%Y%m%d%H%M%S", time.localtime(ct))
    # timestamp = "%s%05d" % (data_head, int(ct))
    # url = "http://mp.weixin.qq.com/mp/verifycode?cert=1539142448102.5093"
    # res = requests.get(url)
    # with open('{}.png'.format(timestamp), 'wb') as file:
    #     file.write(res.content)
    # rc = RClient('xxxxxx', 'xxxxxx', 'xxxxxx', '7ca5e88b449f45c3879a657033eb5ad4')
    # im = open('{}.png'.format(timestamp), 'rb').read()
    # print(rc.rk_create(im, 3040))

