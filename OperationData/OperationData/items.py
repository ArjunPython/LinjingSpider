# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OperationdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PlatformTargetItem(scrapy.Item):
    pid = scrapy.Field()
    volume = scrapy.Field()
    inflow = scrapy.Field()
    remaining_balance = scrapy.Field()
    rate = scrapy.Field()
    average_loan_term = scrapy.Field()
    investment_number = scrapy.Field()
    per_capita_investment = scrapy.Field()
    number_of_borrowers = scrapy.Field()
    per_capita_loan_amount = scrapy.Field()
    createtime = scrapy.Field()
    loan_sign = scrapy.Field()
    b_href = scrapy.Field()
    r_invest_person = scrapy.Field()
    r_loan_person = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                insert into tp_platform_target (pid,average_income_rate,volume,average_loan_time
                ,invest_number,loan_number,income,remain_money,personal_invest,personal_loan
                ,loan_sign,createtime,r_invest_person,r_loan_person
                ) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s)

                     """
        params = (
            self["pid"],self["rate"],self["volume"]
            ,self["average_loan_term"],self["investment_number"],self["number_of_borrowers"]
            ,self["inflow"],self["remaining_balance"],self["per_capita_investment"]
            ,self["per_capita_loan_amount"],self["loan_sign"],self["createtime"],self["r_invest_person"],self["r_loan_person"]

        )
        return insert_sql, params
