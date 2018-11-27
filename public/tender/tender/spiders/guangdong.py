# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as py

class GuangdongSpider(scrapy.Spider):
    name = 'guangdong'
    allowed_domains = ['www.gdgpo.gov.cn']
    start_urls = ['http://www.gdgpo.gov.cn//']	

    def parse(self, response):
        doc = response.text
        links = py(doc).find('.c-m-n-cont a')
        for link in links:
            yield response.follow(py(link).attr('href'), callback=self.parse_item)

    def parse_item(self, response):
        doc = response.text
        title = py(doc).find('.zw_c_c_title')
        content = py(doc).find('.zw_c_c_cont')
        
        if title and content:
            yield{
                'title':py(title[0]).html(),
                'content':py(content[0]).html()
            }        

