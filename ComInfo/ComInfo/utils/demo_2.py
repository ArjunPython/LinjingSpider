# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-7-18 下午2:21
import re
import requests
from copyheaders import headers_raw_to_dict
import execjs
import os

os.environ["NODE_PATH"] = os.getcwd()+"/node_modules"
print(execjs.get().name)


def get_521_content():
    headers = headers_raw_to_dict(b"""
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36
    """)
    url = "https://www.p2peye.com/platform/all/"
    response = requests.get(url,headers=headers)
    cookies = response.cookies
    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    txt_521 = response.text
    print(txt_521)
    txt_521 = ''.join(re.findall('<script>(.*?)</script>', txt_521))
    return (txt_521,cookies)


def fixed_fun(function):

    func_return = function.replace('eval','return')
    print(func_return)
    content = execjs.compile(func_return)
    evaled_func = content.call('x')
    print(evaled_func)
    evaled = "".join(evaled_func.split())
    rr = re.match(r"var(.*)=function\(\).*", evaled).group(1)
    print(rr)
    mode_func=evaled_func.replace('while(window._phantom||window.__phantomas){};','').replace('document.cookie=','return')\
        .replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);","")\
        .replace(";if((function(){try{return !!window.addEventListener;}catch(e){return false;}})())","")

    ss = mode_func.replace("{document.addEventListener('DOMContentLoaded',"+rr+",false)}else{document.attachEvent('onreadystatechange',"+rr+")}", "")
    print(ss)
    content = execjs.compile(ss)
    # print(content)
    # cookies = content.call(rr)
    # print(cookies)

    # __jsl_clearance=cookies.split(';')[0]
    # return __jsl_clearance


if __name__ == '__main__':
    func = get_521_content()
    content_1 = func[0]
    print(content_1)
    cookie_id = func[1]
    # print(cookie_id)
    # cookie_js = fixed_fun(func[0])
    fixed_fun(func[0])
    # print(cookie_js)