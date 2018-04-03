# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChangzhiserverSectionItem(scrapy.Item):
    # 事项名称
    title = scrapy.Field()
    url = scrapy.Field()

class ChangzhiserverPageItem(scrapy.Item):
    title = scrapy.Field()
    id = scrapy.Field()
    section_id = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()

class ChangzhiserverNews(scrapy.Item):
    section = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()