# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-8-13 下午2:25
import re
import requests
from ComInfo.settings import PROXY_URL

class ProxyMiddleware(object):

    def __init__(self):
        self.proxy_url = PROXY_URL
    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                ip_port = re.match(r"(.*):(\d+)", proxy)
                print(proxy)
                return ip_port.group(1),int(ip_port.group(2))
        except requests.ConnectionError:
            return False

if __name__ == '__main__':
    ip = ProxyMiddleware()
    ip_port = ip.get_random_proxy()
    print(ip_port)
