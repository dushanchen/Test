# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class JiangsuSpider(CrawlSpider):
    name = 'jiangsu'
    allowed_domains = ['www.ccgp-jiangsu.gov.cn']
    start_urls = ['http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/']

    rules = (
        Rule(LinkExtractor(allow=('\w.html'),restrict_xpaths='//div[@id="newsList"]//a'),callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="list_con"]//a'))
    )

    def parse_item(self, response):
        # title = response.css('.dtit h1::text').extract_first()
        # content = response.css('.detail').extract_unquoted()
        # content = ''.join(content).replace('\t','').replace('\n','').replace('\xa0','')
        # yield{
        #     'title':title
        # }
        # self.log(title)
        url = response.url
        yield{
            'url':url
        }
    
