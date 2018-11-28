# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
#from pymongo import MongoClient

#class MongoPipline(object):
#    def __init__(self.databaseIp = '127.0.0.1',databasePort = 27017):
#        client = MongoClient(databaseIp,databasePort)
#        self.db = client('ceshi')
        


class UnionNewsPipeline(object):
    def process_item(self, item, spider):
        if item:
            with open('d:/news.csv','a+',newline= '',encoding = 'gb18030')as f:
                writer = csv.writer(f)
                writer.writerow([item['title'], item['pub_time'], item['content']])
                print('写入完成')
        
        return item
