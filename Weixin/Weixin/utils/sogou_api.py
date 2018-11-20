# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-10-8 下午4:18

import wechatsogou

we_api = wechatsogou.WechatSogouAPI(captcha_break_time=3)

content_dict = we_api.get_gzh_info("铜板街")
content = we_api.search_gzh("铜板街")
for con in content:
    print(con)
print("*" * 100)
print(content_dict)