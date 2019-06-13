import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from pyquery import PyQuery as py

import json


class ChongqingSpider(CrawlSpider):
    name = 'chongqing'
    allowed_domains = ['cqgp.gov.cn']
    start_urls = [
        'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=1&ps=20&type=100,200,201,202,203,204,205,206,300,301,302,303,304,3041,305,400,401,4001&userType=41,42',
        'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=2&ps=20&type=100,200,201,202,203,204,205,206,300,301,302,303,304,3041,305,400,401,4001&userType=41,42',
        'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=3&ps=20&type=100,200,201,202,203,204,205,206,300,301,302,303,304,3041,305,400,401,4001&userType=41,42',
        'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=4&ps=20&type=100,200,201,202,203,204,205,206,300,301,302,303,304,3041,305,400,401,4001&userType=41,42',
        'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi=5&ps=20&type=100,200,201,202,203,204,205,206,300,301,302,303,304,3041,305,400,401,4001&userType=41,42',
    ]

    
    def parse(self, response):
        self.log(response.text)
        doc = response.text
        data = json.loads(doc)
        # url = 'https://www.cqgp.gov.cn/notices/detail/%s?title=%s'
        url = 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable/%s'

        for i in data['notices']:
            id = i['id']
            title = i['title']
            yield scrapy.Request(url % (id), callback=self.parse_, meta={'id':id})


    def parse_(self, response):
        data = json.loads(response.text)
        title = data['notice']['title']
        content = data['notice']['html']
        publish_time = data['notice']['issueTime'].split(' ')[0]
        # doc = response.text
        id = response.meta['id']
        # title = py(doc).find('#titlecandel').html()
        # publish_time = py(doc).find('#datecandel').html().replace('发布日期： ', '').replace('年','-').replace('月','-').replace('日','')

        # content = py(doc).find('#notice .wrap-post .wrap-post').html()

  
        yield {
            'id':'chongqing_' + id,
            'title':title,
            'content':content,
            'souce_url':response.url,
            'province':'重庆',
            'publish_time':publish_time
            }