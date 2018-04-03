import re
import scrapy
from scrapy.http import Request
from changzhiserver.items import ChangzhiserverSectionItem,ChangzhiserverPageItem,ChangzhiserverNews
from model.config import DBSession
from model.models import ChangzhiServerSection
from bs4 import BeautifulSoup
import re
from datetime import datetime
# 抓取分类 信息
class ChangzhiServer(scrapy.Spider):
    name = 'changzhiserver'
    custom_settings = {
        'ITEM_PIPELINES': {
            'changzhiserver.pipelines.ChangzhiserverPipeline': 1,
        }
    }
    allowed_domains = ['zwdt.changzhi.gov.cn']
    def start_requests(self):
        url = 'http://www.zwdt.changzhi.gov.cn:8989/system/web/fwxz.jsp'
        yield Request(url,self.parse)
    def parse(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        tables = soup.find_all('div',class_=re.compile("tab"))
        for table in tables:
            a_s = table.find_all('a')
            for a in a_s:
                item = ChangzhiserverSectionItem()
                href = a.attrs['href']
                href = href.replace('\r', '').replace('\n', '').replace('\t', '')
                text = a.get_text().replace(' ','')
                bastUrl = 'http://www.zwdt.changzhi.gov.cn:8989'
                fullUrl = bastUrl + href
                item['title'] = text
                item['url'] = fullUrl
                yield self.get_section(item)
    def get_section(self,section):
        return section

# 抓取分类信息中的内容
class ChangzhiServerPage(scrapy.Spider):
    name = 'changzhiServerPage'
    custom_settings = {
        'ITEM_PIPELINES': {
            'changzhiserver.pipelines.DuplicatesPipeline': 100,
            'changzhiserver.pipelines.ChangzhiserverPagePipeline':200,
        }
    }
    allowed_domains = ['zwdt.changzhi.gov.cn']
    def start_requests(self):
        db = DBSession()
        sections = db.query(ChangzhiServerSection).all()
        for section in sections:
            yield Request(section.url,self.parse,meta={'section_id':section.id})
    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        a_s = soup.find_all('a',class_='geren1')
        for a in a_s:
            item = ChangzhiserverPageItem()
            item['section_id'] = response.meta['section_id']
            title = a.get_text().replace(' ','')
            url = a.attrs['href']
            url = url.replace('\r', '').replace('\n', '').replace('\t', '')
            fullUrl = url.replace('./','http://www.zwdt.changzhi.gov.cn:8989/system/web/')
            item['title'] = title
            item['url'] = fullUrl
            yield Request(fullUrl,self.get_page,meta={'item':item})

    def get_page(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table',id='main')
        tableHtml = table.prettify().replace('\r', '').replace('\n', '').replace('\t', '')
        item = response.meta['item']
        item['content'] = tableHtml
        return item



class ChangzhiServerNews(scrapy.Spider):
    name = 'changzhiserverNews'
    custom_settings = {
        'ITEM_PIPELINES': {
            'changzhiserver.pipelines.ChangzhiserverNewsPipeline': 300,
        }
    }
    allowed_domains = ['changzhi.gov.cn']
    def start_requests(self):
        url = 'http://www.changzhi.gov.cn/xwzx/jrzz/'
        yield Request(url,self.parse)
    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        sections = soup.find_all('h3',class_='cond-menu-head current')
        baseUrl = 'http://www.changzhi.gov.cn/xwzx'
        for section in sections:
            a = section.find('a')
            section_name = a.get_text().replace(' ','')
            href = a.attrs['href'].replace('\r', '').replace('\n', '').replace('\t', '')
            page = 0
            page_str = 'index.shtml'

            fullUrl = href.replace('./',baseUrl) + page_str
            yield Request(fullUrl,self.get_page,meta={'section':section_name,'page':page})
    def get_page(self,response):
        soup = BeautifulSoup(response.text, 'lxml')
        ul = soup.find('ul',class_='chz-common-text-list-items')
        lis = ul.find_all('li')
        news_list = []
        for li in lis:
            date = li.find('span',class_='pubtime')
            date = date.get_text().replace(' ','')
            date = datetime.datetime.strptime(date,'%Y-%m-%d')
            now_date = datetime.now().date()
            if date >= now_date: # 如果是最新消息
                title = li.find('a').get_text().replace(' ','')
                href = li.find('a').attrs['href'].replace('\r', '').replace('\n', '').replace('\t', '')
                item = ChangzhiserverNews()
                item['section'] = response.meta['section']
                item['title'] = title
                item['date'] = str(date)
                item['url'] = href
                news_list.append(item)
                self.get_item(item)
        if len(news_list) == len(lis): #如果本页全部为最新新闻 翻页获取
            page = response.meta['page']
            page += 1
            pageStr = 'index_'+page+'.shtml'
            last_url = response.url.split('/')[-1]
            fullUrl = response.url.replace(last_url,pageStr)
            yield Request(fullUrl, self.get_page, meta={'section': response.meta['section'], 'page': page})

    def get_item(self,item):
        return item




