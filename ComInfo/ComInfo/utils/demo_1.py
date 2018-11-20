# -*- coding: utf-8 -*-
# author: arjun
# @Time: 18-5-17 下午4:55

import re

import requests

srt = ";if((function(){try{return!!window.addEventListener;}catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',_3c,false)}else{document.attachEvent('onreadystatechange',_3c)}"

res = "".join(srt.split())

response = re.sub(r";if\(\(function\(\)\{try\{return!!window\.addEventListener;}catch\(e\)\{returnfalse;}}\)\(\)\)(.*)else\{document\.attachEvent\('onreadystatechange',(.*)\)}","",res)
# respo = re.sub(r"(.*)","123",res)

# print(response)
ee = "document.addEventListener('DOMContentLoaded',_3c,false)"

rr= re.match(r".*\{document\.addEventListener\('DOMContentLoaded',(.*),false\)}.*",res).group(1)
# print(rr)

ss = ee.replace(r"document.addEventListener('DOMContentLoaded',{},false)".format(rr),"")
# print(ss)

"""8000.000万人民币"""
"""2000.000000万"""
"""11111.11万元"""
"""2500.000000万元人民币"""
ret_1 = re.match(r"(\d+)\.(.*)万(.*)", "1001.000000万").group(1)
# print(ret_1)

"""83667万人民币"""
"""10000万元人民币"""
# ret_2 = re.match(r"(\d+)万(.*)", "1001.000000万").group(1)
# print(ret_2)

"""(人民币)20000.00万元"""
ret_5 = re.match(r"\(人民币\)(\d+)\.(.*)万元", "(人民币)20000.00万元").group(1)
# print(ret_5)

# ip = "122.233.30.165:1246"
# ip_port = re.match(r"(.*):(\d+)",ip).group(1)
# ip_port = ip_port
# print(type(ip_port))
# sss = "91441302597456683E"
# code = sss[2:4] + "0000"
# code_1 = sss[2:6] + "00"
# code_2 = sss[2:8]
# print(code)
# print(code_1)
# print(code_2)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
# url = "https://www.wdzj.com/dangan/search"
url = "https://www.p2peye.com/platform/_%E7%81%AB%E9%92%B1%E7%90%86%E8%B4%A2/"
# proxies = {"http": "http://59.62.7.171:4218"}
res = requests.get(url,headers=headers)
print(res)
