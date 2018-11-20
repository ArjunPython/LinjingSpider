# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests
import time
from PIL import Image
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.http import HtmlResponse
from .utils.rk import RClient


class WeixinSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class RandomUserAgentMiddlware(object):
    #随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())


class RandomProxyMiddleware(object):

    def process_request(self, request, spider):
        # ip_port = random.choice(PROXY)
        # print(ip_port)
        # request.meta["proxy"] = "https://" + ip_port
        request.meta["proxy"] = "https://223.243.202.234:4251"


class ProxyMiddleware(object):

    def __init__(self, proxy_url):
        self.proxy_url = proxy_url
    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        proxy = self.get_random_proxy()
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            print("*"*100)
            print('使用代理' + uri)
            print("*" * 100)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        spider.browser.get(request.url)
        time.sleep(8)
        content = spider.browser.page_source
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)


class JSPageMiddleware(object):
    @classmethod
    def process_request(self,request,spider):
        spider.browser.get(request.url)
        # spider.browser.execute_script("var q=document.documentElement.scrollTop=10000")
        time.sleep(random.randint(2, 6))
        print("访问：{0}".format(request.url))
        ct = time.time()
        data_head = time.strftime("%Y%m%d%H%M%S", time.localtime(ct))
        timestamp = "%s%05d" % (data_head, int(ct))
        try:
            verify_img = spider.browser.find_element_by_id('verify_img')
            if None != verify_img:
                print("Middleware 微信分析填入验证码!")
                # 截图
                spider.browser.get_screenshot_as_file('./image/wescreenshot{0}.png'.format(timestamp))
                # 获取指定元素位置
                element = spider.browser.find_element_by_id('verify_img')
                left = int(element.location['x'])
                top = int(element.location['y'])
                right = int(element.location['x'] + element.size['width'])
                bottom = int(element.location['y'] + element.size['height'])

                # 通过Image处理图像
                im = Image.open('./image/wescreenshot{0}.png'.format(timestamp))
                im = im.crop((left, top, right, bottom))
                # 保存验证码图片
                im.save('./image/wecode{0}.png'.format(timestamp))
                # 若快平台识别验证码
                rc = RClient('xxxxxx', 'xxxxxx', 'xxxxxx', 'xxxxxx')
                im = open('./image/wecode{0}.png'.format(timestamp), 'rb').read()
                rk_ret = rc.rk_create(im, 3040)
                wecode = str(rk_ret["Result"])
                print("./image/wecode{0}:".format(timestamp) + wecode)
                # 模拟输入验证码，并提交
                elem = spider.browser.find_element_by_id("input")
                elem.clear()
                elem.send_keys(wecode)
                spider.browser.find_element_by_id("bt").click()
                # 延时5秒，等待完成页面跳转
                time.sleep(5)
        except Exception as e:
            pass
            # print(e)

        time.sleep(random.randint(2, 5))
        content = spider.browser.page_source
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

