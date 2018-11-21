# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlatformtargetItem(scrapy.Item):
    # define the fields for your item here like:
    # name = .scrapy.Field()
    pass



class PlatformTargetItem(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    create_time = scrapy.Field()
    pid = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
                insert into tp_dai_rank (name,score,create_time,pid
                ) VALUES (%s, %s, %s, %s)

                     """
        params = (
            self["name"],self["score"],self["create_time"],self["pid"]

        )
        return insert_sql, params


class WangDaiTieItem(scrapy.Item):

    pass