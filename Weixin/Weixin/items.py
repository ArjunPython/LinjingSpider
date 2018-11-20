# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    content = scrapy.Field()
    update_time = scrapy.Field()
    platform = scrapy.Field()
    href = scrapy.Field()
    postive_score = scrapy.Field()
    update_date = scrapy.Field()
    news_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                             insert into tp_news (title,content,update_time,platform,url,postive_score,update_date,news_time
                               ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

                         """
        params = (
            self["title"], self["content"], self["update_time"], self["platform"], self["href"], self["postive_score"]
            , self["update_date"], self["news_time"]
        )
        return insert_sql, params


