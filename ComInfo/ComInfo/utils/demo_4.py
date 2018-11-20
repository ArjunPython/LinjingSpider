# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-8-9 上午11:02
import re
import requests

from urllib.parse import quote

lua_script = """
    function main(splash)
        splash:go("https://www.tianyancha.com/login")
        input = splash:select(".modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .pb30.position-rel input")
        input:send_text("xxxxxx")
        input_1 = splash:select(".modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .pb40.position-rel input")
        input_1:send_text("xxxxxx")
        submit = splash:select(".modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .c-white.b-c9.pt8.f18.text-center.login_btn")
        submit:mouse_click()
    end
"""


script = """
    function main(splash)
        assert(splash:go("https://www.tianyancha.com/login"))
        assert(splash:wait(1))
        js = string.format("document.querySelector('.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .pb30.position-rel input').value=13175867481;document.querySelector('.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .pb40.position-rel input').value='wt941206';document.querySelector('.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in .c-white.b-c9.pt8.f18.text-center.login_btn').click()")
        splash:evaljs(js)
        assert(splash:wait(2))

  end
"""


url = "http://127.0.0.1:8050/execute?lua_source" + quote(script)

response = requests.get(url)

print(response.text)

res = """href="https://www.tianyancha.com/usercenter/concern/1" href-new-event="" event-name="导航-用户中心"><span>131 **** 7481</span><i class="tic tic-caret-down nav-icon"></i></a><div class="list-group ">"""

content = "".join(res.split())
print(content)
content = re.findall(r".*(<span>131\*\*\*\*7481</span>).*",content)
print(content)