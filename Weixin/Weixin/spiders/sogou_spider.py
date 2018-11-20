# -*- coding: utf-8 -*-
import datetime as da
import json
import scrapy
from copy import deepcopy
import re
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..items import WeixinItem
from Weixin.utils.handle import datestamptrans,handle_tag
from datetime import datetime


class SogouSpiderSpider(scrapy.Spider):
    name = 'sogou_spider'
    allowed_domains = ['sogou.com',"mp.weixin.qq.com",'weixin.qq.com', 'qq.com']
    start_urls = [
                'https://weixin.sogou.com/weixin?type=1&s_from=input&query=p2p911',
                'https://weixin.sogou.com/weixin?type=1&s_from=input&query=p2p818',
                  'https://weixin.sogou.com/weixin?type=1&s_from=input&query=p2phj110',
                  ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        super(SogouSpiderSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("spider closed")
        self.browser.quit()

    def parse(self, response):
        li_list = response.xpath("//div[@class='news-box']/ul/li")
        for li in li_list:
            item = {}
            item["net_name"] = li.xpath(".//div[@class='txt-box']/p[@class='tit']/a//text()").extract()
            if len(item["net_name"]) > 0:
                item["net_name"] = "".join(item["net_name"])
            item["weixin_num"] = li.xpath(".//div[@class='txt-box']/p[@class='info']/label/text()").extract_first()
            item["weixin_href"] = li.xpath(".//div[@class='txt-box']/p[@class='tit']/a/@href").extract_first()
            if item["weixin_href"] is not None:
                yield scrapy.Request(item["weixin_href"],
                                     callback=self.parse_detail,
                                     meta={"item":deepcopy(item)})

    def parse_detail(self,response):
        item = deepcopy(response.meta["item"])
        # div_list = response.xpath("//div[@id='history']/div[@class='weui_msg_card']")

        date = datetime.now().timetuple()
        dateStr = str(date.tm_year) + '年' + str(date.tm_mon) + '月' + str(date.tm_mday) + '日'
        re_path = '//div[@id="history"]/div[@class="weui_msg_card"]/div[contains(./text(), "{0}")]/../div[@class="weui_msg_card_bd"]/div[@class="weui_media_box appmsg"]'.format(dateStr)
        div_list = response.xpath(re_path)
        if len(div_list) <= 0:
            print("<<"+item["net_name"]+">>"+"今日没有发布内容！")
            return
        # div_list = response.xpath("//div[@id='history']/div[@class='weui_msg_card']//div[@class='weui_media_box appmsg']")
        for div in div_list:
            href = div.xpath(
                "./div[@class='weui_media_bd']/h4[@class='weui_media_title']/@hrefs").extract_first()
            item["real_href"] = "https://mp.weixin.qq.com" + href
            # item["title"] = div.xpath(
            #     "./div[@class='weui_msg_card_bd']/div/div[@class='weui_media_bd']/h4[@class='weui_media_title']/text()").extract()
            # if len(item["title"]) > 0:
            #     item["title"] = "".join("".join(item["title"]).split())
            item["update_time"] = div.xpath(
                "./div[@class='weui_media_bd']/p[@class='weui_media_extra_info']/text()").extract_first()
            if item["real_href"] is not None:
                yield scrapy.Request(item["real_href"],
                                     callback=self.weixin_detail,
                                     meta={"item": deepcopy(item)})


    def weixin_detail(self,response):
        item = deepcopy(response.meta["item"])
        weixin_item = WeixinItem()
        weixin_item["update_date"] = str(da.date.today())
        weixin_item["update_time"] = item["update_time"]
        weixin_item["href"] = item["real_href"]
        weixin_item["platform"] = item["net_name"]
        weixin_item["news_time"] = datestamptrans(item["update_time"])
        title = response.xpath("//div[@id='page-content']//div[@id='img-content']/h2[@id='activity-name']/text()").extract_first()
        if title is not None:
            weixin_item["title"] = "".join(title.split())
            weixin_item["postive_score"] = handle_tag(weixin_item["title"])
        content = response.xpath('//div[@id="js_content"]/p//text()').extract()
        if content is not None:
            weixin_item["content"] = ''.join("".join(content).split())
            yield weixin_item
            # print(weixin_item)

        # content = response.text
        # print(content)
        # if "请输入验证码" in content:
        #     print("*%" * 100)
        # scriptText = response.xpath("/html/body/script[8]/text()").extract_first()
        # scriptText = "".join(scriptText.split())
        # con_json = re.findall(""".*varmsgList=(.*);seajs\.use\("sougou/profile\.js"\);""",scriptText)[0]
        # con_list = json.loads(con_json)["list"]
        # for con in con_list:
        #     print(con)

        # bizText = scriptText.split(";")[6]
        # print("*%" * 100)
        # print(bizText)
        # bizText = bizText.split('"')[1]
        # print("*%" * 100)
        # print(bizText)

