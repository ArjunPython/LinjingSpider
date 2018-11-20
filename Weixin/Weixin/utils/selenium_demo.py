# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-10-11 上午8:59
import time
from PIL import Image
from selenium import webdriver
from rk import RClient
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def demo():
    driver = webdriver.Chrome()

    url = "http://mp.weixin.qq.com/profile?src=3&timestamp=1539219004&ver=1&signature=qgQNBsUuF2qmyljNGm5di7eEI8QfzGhd-KTXpZHBLmr2xseulMEgBDldM9QC2-41lbPaBo1fHS9OkPgGtwjhSQ=="

    driver.get(url)
    try:
        verify_img = driver.find_element_by_id('verify_img')


        if None != verify_img:
            print("Middleware 微信分析填入验证码!")
            ct = time.time()
            data_head = time.strftime("%Y%m%d%H%M%S", time.localtime(ct))
            timestamp = "%s%05d" % (data_head, int(ct))
            # 截图
            driver.get_screenshot_as_file('./im/wescreenshot{0}.png'.format(timestamp))
            # 获取指定元素位置
            element = driver.find_element_by_id('verify_img')
            left = int(element.location['x'])
            top = int(element.location['y'])
            right = int(element.location['x'] + element.size['width'])
            bottom = int(element.location['y'] + element.size['height'])
            # 通过Image处理图像
            im = Image.open('./im/wescreenshot{0}.png'.format(timestamp))
            im = im.crop((left, top, right, bottom))
            time.sleep(3)
            # 保存验证码图片
            im.save('./im/wecode{0}.png'.format(timestamp))
            rc = RClient('xxxxxx', 'xxxxxx', 'xxxxxx', 'xxxxxx')
            im = open('./im/wecode{0}.png'.format(timestamp), 'rb').read()
            rk_ret = rc.rk_create(im, 3040)
            wecode = str(rk_ret["Result"])
            print("wecode{0}:".format(timestamp) + wecode)
            elem = driver.find_element_by_id("input")
            elem.clear()
            elem.send_keys(wecode)
            driver.find_element_by_id("bt").click()
    except Exception as e:
        print(e)

    time.sleep(6)
    print("未出现验证码")

    # driver.close()

if __name__ == '__main__':
    demo()
