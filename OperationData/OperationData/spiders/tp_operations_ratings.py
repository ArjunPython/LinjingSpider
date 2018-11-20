# -*- coding: utf-8 -*-
import datetime
import scrapy

class TpOperationsRatingsSpider(scrapy.Spider):
    name = 'tp_operations_ratings'
    allowed_domains = ['wdzj.com']
    start_urls = ['https://www.wdzj.com/dangan/search?filter=e1&show=1&sort=3&currentPage=1']

    def parse(self, response):
        li_list = response.xpath("//div[@class='terraceCon']/ul/li")
        for li in li_list:
            item = {}
            item["name"] = li.xpath("./div[@class='itemTitle']/h2/a/text()").extract_first()
            item["rat_num"] = li.xpath("./div[@class='itemTitle']/div[1]/em/strong/text()").extract_first()
            item["creat_date"] = str(datetime.date.today())
            yield item
            # print(item)

        # pages = response.xpath(
        #     "//div[@class='pageList']/a[contains(text(),'尾页')]/@currentnum").extract_first()
        for page in range(2, 5):
            next_url = "https://www.wdzj.com/dangan/search?filter=e1&show=1&sort=3&currentPage={}"\
                .format(page)
            yield scrapy.Request(next_url, callback=self.parse)
