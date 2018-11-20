# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-5-30 上午9:10

import requests
import json
import time

def handle_address(add):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    url = "http://api.map.baidu.com/geocoder/v2/?" \
          "address={}&output=json&ak=xxxxxx".format(add)
    response = requests.get(url,headers=headers)
    dict_res = json.loads(response.content.decode())
    time.sleep(1)
    try:
        address_one = dict_res["result"]["location"]["lng"]
        address_two = dict_res["result"]["location"]["lat"]
        return address_one,address_two
    except:
        pass

class Address(object):

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        self.url = "http://api.map.baidu.com/geocoder/v2/?" \
          "address={}&output=json&ak=xxxxxx"

    def handle_address(self,add):
        response = requests.get(self.url.format(add), headers=self.headers)
        dict_res = json.loads(response.content.decode())
        if dict_res["status"] == 0:
            address_one = dict_res["result"]["location"]["lng"]
            address_two = dict_res["result"]["location"]["lat"]
            return address_one, address_two
        else:
            return 0

if __name__ == '__main__':
    ad = Address()
    a = ad.handle_address("成都市锦江区通宝街360号（2#一层）（自编号251号）")
    print(a)