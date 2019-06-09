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
        url = response.url

        id = url.split('/id/')
        if len(id) == 2:
            id = id[1].split('.html')
            if len(id) == 2:
                id = id[0]

                doc = response.text
                title = py(doc).find('.zw_c_c_title')
                content1 = py(doc).find('.zw_c_c_qx')
                content2 = py(doc).find('.zw_c_c_cont')
                time = py(doc).find('.zw_c_c_qx span:eq(3)').html()
                time = time[:10]
                
                yield{
                    'id':'guangdong_'+ id, 
                    'title':py(title[0]).html(),
                    'content':py(content1[0]).html() + py(content2[0]).html(),
                    'province':'福建',
                    'source_url':url,
                    'publish_time':time
                }        

