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
            Rule(LinkExtractor(allow=(''), restrict_css='.diqu')),
            Rule(LinkExtractor(allow=(r'.*/notice/.*/.*/')), callback='parse_item'),
        )


    def parse_item(self, response):
        url = response.url
        doc = response.text
        title = py(doc).find('.notice-hear h2').html()
        content = py(doc).find('.notice-con').html()
        time = py(doc).find('.clearfix span:last').html().split('发布时间：')

        if len(time) == 2:
            time = time[1][:10]
        else:
            time = datetime.date.today().strftime('%Y%m%d')

        if title and content:
            id = url.split('notice/')
            if len(id) == 2:
                id = id[1]
            yield {
                'id':'fujian_' + id,
                'title':title,
                'content':content,
                'source_url':response.url,
                'province':'fujian',
                'publish_time':time,
            }
