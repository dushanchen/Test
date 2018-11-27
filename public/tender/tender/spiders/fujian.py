# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from pyquery import PyQuery as py


class FujianSpider(CrawlSpider):
    name = 'fujian'
    allowed_domains = ['qz.fjzfcg.gov.cn']
    start_urls = ['http://qz.fjzfcg.gov.cn/']

    rules = (
    		Rule(LinkExtractor(allow=(''), restrict_css='.tabsContainerWrap')),
    		Rule(LinkExtractor(allow=(r'.*/notice/.*/.*/')), callback='parse_item'),
    	)


    def parse_item(self, response):
        doc = response.text
        title = py(doc).find('.notice-hear h2').html()
        content = py(doc).find('.notice-con').html()

        if title and content:
        	yield{
        		'title':title,
        		'content':content,
        		'url':response.url,
        	}
