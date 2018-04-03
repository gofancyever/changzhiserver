# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from model.models import ChangzhiServerSection,ChangzhiServerPage
from model.config import DBSession
from datetime import datetime
from scrapy.exceptions import DropItem
from model.config import Redis



class ChangzhiserverPipeline(object):
    def open_spider(self,spider):
        self.session = DBSession()

    def process_item(self, item, spider):

        a = ChangzhiServerSection(
                title = item['title'],
                url=item['url'],
                runningDate = datetime.now()
            )
        self.session.add(a)
        self.session.commit()
    def close_spider(self,spider):
        self.session.close()

# 去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('url:%s' % item['url']):
            raise DropItem("已存在 item: %s" % item['title'])
        else:
            print('新增 item:%s' % item['title'])
            Redis.set('url:%s' % item['url'],1)
            return item

class ChangzhiserverPagePipeline(object):
    def open_spider(self,spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        a = ChangzhiServerPage(
                title = item['title'],
                url=item['url'],
                section_id=item['section_id'],
                content=item['content'],
                runningDate=datetime.now()
            )
        self.session.add(a)
        self.session.commit()
    def close_spider(self,spider):
        self.session.close()

class ChangzhiserverNewsPipeline(object):
    def open_spider(self,spider):
        self.session = DBSession()
    def process_item(self,item,spider):
        pass

    def close_spider(self,spider):
        self.session.close()