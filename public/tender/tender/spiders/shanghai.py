# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor


class ShanghaiSpider(CrawlSpider):
    name = 'shanghai'
    allowed_domains = ['zfcg.sh.gov.cn']
    start_urls = ['http://www.zfcg.sh.gov.cn/login.do?method=beginloginnew']

    rules = (
        Rule(LinkExtractor(allow=('&bulletin_id=',)),callback='parse_item'),
        )

    def parse_item(self, response):
        result = response.text
        yield{
            'content':result
        }
        self.log(result)
