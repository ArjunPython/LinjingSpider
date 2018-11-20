# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-8-1 下午3:03

import requests
import re
import os
import execjs
import json

# os.environ["EXECJS_RUNTIME"] = "Node"
os.environ["NODE_PATH"] = os.getcwd()+"/node_modules"
print(execjs.get().name)


def get_521_content():
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
    }
    req=requests.get('https://www.seebug.org/vuldb/ssvid-92666',headers=headers)
    cookies=req.cookies

    cookies = '; '.join(['='.join(item) for item in cookies.items()])
    txt_521 = req.text
    txt_521 = ''.join(re.findall('<script>(.*?)</script>',txt_521))
    return (txt_521,cookies)

def fixed_fun(function):
    func_return=function.replace('eval','return')
    print(func_return)
    content=execjs.compile(func_return)
    print(content)
    evaled_func=content.call("f")
    print(evaled_func)
    mode_func=evaled_func.replace('while(window._phantom||window.__phantomas){};','').\
        replace('document.cookie=','return').replace(r';if((function(){try{return !!window.addEventListener;}','').\
        replace(r"catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',l,false);}",'').\
        replace(r"else{document.attachEvent('onreadystatechange',l);}",'').replace(r"setTimeout('location.href=location.href.replace(/[\?|&]captcha-challenge/,\'\')',1500);",'')
    print(mode_func)
    # content = execjs.compile(mode_func)
    # cookies=content.call("l")
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