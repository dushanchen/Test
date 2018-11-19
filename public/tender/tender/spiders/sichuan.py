# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from pyquery import PyQuery as py
from scrapy.http import FormRequest

class SichuanSpider(scrapy.Spider):
    name = 'sichuan'
    allowed_domains = ['www.ccgp-sichuan.gov.cn']
    url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?'
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    params = {
        'method':'search',
        'years':'',
        'chnlNames':'\u6240\u6709',
        'chnlCodes':'',
        'title':'',
        'tenderno':'',
        'agentname':'',
        'buyername':'',
        'startTime':today,
        'endTime':today,
        'distin_like':'',
        'city':'',
        'town':'',
        'cityText':'',
        'townText':'',
        'searchKey':'',
        'distin':'',
        'type':'',
        'beginDate':'',
        'endDate':'',
        'str1':'',
        'str2':'',
        'pageSize':'10',
        'curPage':'1',
        'searchResultForm':'search_result_anhui.ftl'
    }
    
    def start_requests(self):
        reqs = []
        for i in range(1,11):
            params = self.params
            params['curPage'] = str(i)
            req = scrapy.FormRequest(self.url,callback=self.parse,formdata=self.params)
            reqs.append(req)
        return reqs


    def parse(self, response):
        result = response.text
        self.log(response.url)
        links = py(result).find('.info a')
        for _ in links:
            href = py(_).attr('href')
            if href != 'javascript:void(0)':
                yield response.follow(href,callback=self.parse_item)


    def parse_item(self, response):
        result = response.text
        url = response.url
        self.log('url')
        id = url.split('.')[-2].split('/')[-1]
        title = py(py(result).find('.cont-info h1')[0]).text()
        content = py(py(result).find('#myPrintArea')).html()

        if content:
            yield{
                'id':'sichuan_' + id,
                'title':title,
                # 'publish_time':result['noticePubDate'],
                'content':content,
                'source_url':url,
                'province':'四川'
            }

