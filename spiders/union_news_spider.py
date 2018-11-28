# -*- coding: utf-8 -*-
import scrapy
from union_news.items import UnionNewsItem
import datetime
import re


class UnionNewsSpiderSpider(scrapy.Spider):
    name = 'union_news_spider'
    allowed_domains = ['10.94.4.7']
    start_urls = [
        'http://10.94.4.7/news/more.asp?ttt=8&sss=%BF%C6%BC%BC%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=9&sss=%CC%E5%D3%FD%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=10&sss=%C9%E7%BB%E1%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=12&sss=%B9%FA%C4%DA%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=13&sss=%B9%FA%BC%CA%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=15&sss=%B2%C6%BE%AD%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]+\
        ['http://10.94.4.7/news/more.asp?ttt=16&sss=%BE%FC%CA%C2%D0%C2%CE%C5&mmm={}'.format(i) for i in range(3)]
    

    def parse(self, response):
        half_url = response.xpath('//td[@width="453"]/a/@href').extract()
        for i in [response.urljoin(url) for url in half_url]:
            print(response.url)
            yield scrapy.Request(i, callback = self.detail)
        
    def detail(self, response):
        item = UnionNewsItem()
        item['title'] = response.xpath('//font[@size="5"]/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('//div[@align="right"]/font/text()').extract()[0][5:]
        item['content'] = ''.join(response.xpath('//td/p/text()').extract()).replace('\u3000\u3000','').replace('\xa0','').strip()
        #对新闻进行日期筛选，获取最近7天更新的新闻内容
        x,y,z = re.findall('\d+',item['pub_time'])
        date = datetime.date(int(x),int(y),int(z))
        if date > datetime.date.today()-datetime.timedelta(days=7):
            yield item