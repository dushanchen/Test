# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import re
import datetime
from pyquery import PyQuery as pq

class TianjinSpider(CrawlSpider):
    name = 'tianjin'
    allowed_domains = ['www.ccgp-tianjin.gov.cn']
    start_urls = ['http://www.ccgp-tianjin.gov.cn/portal/topicView.do']

    rules = (
        Rule(LinkExtractor(allow=r'portal/topicView\.do'), callback='parse_item'),
    )

    def parse_item(self, response):

        doc = pq(response.text)

        a = doc.find('.oneWrap')
        links = pq(a[1]).find('.twoWrap a')

        for i in links:
            href = pq(i).attr('href')

            id = re.findall(re.compile(r'id=[0-9]+'), href)
            if id:
                params = {
                    "method":"view",
                    "page":"2",
                    "id":"1663",
                    "step":"1",
                    "view":"Infor",
                    "st":"1",
                    "ldateQGE":"",  
                    "ldateQLE":""
                }

                params['id'] = id[0].replace('id=', '')

                for i in range(3):
                    params['page'] = str(i+1)
                    yield scrapy.FormRequest(
                        url='http://www.ccgp-tianjin.gov.cn/portal/topicView.do',
                        formdata=params, 
                        callback=self.ret
                    )


    def ret(self, response):
        self.log(response.url)
        a = response.css('.dataList a')
        for i in a:
            yield response.follow(i, self.ret2)


    def ret2(self, response):
        doc = response.text
        url = response.url
        id = re.findall(re.compile(r'id=[0-9]+'), url)
        if id:
            yield{
                'id': 'tianjin_' + id[0].replace('id=', ''),
                'content': pq(doc).find('td[valign="top"]').html(),
                'title': pq(doc).find('td[valign="top"] b').html(),
                'source_url': url,
                'province': '天津',
                'publish_time':datetime.datetime.now().strftime('%Y-%m-%s %H:%M:%S')
            }
            




