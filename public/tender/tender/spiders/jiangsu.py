# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pyquery import PyQuery as py
import datetime

class JiangsuSpider(CrawlSpider):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    name = 'jiangsu'
    allowed_domains = ['www.ccgp-jiangsu.gov.cn']
    start_urls = [
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cjgg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/cgyg/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/htgg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/htgg/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/xqyj/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/xqyj/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/gzgg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/gzgg/index_1.html',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/ysgg/',
        'http://www.ccgp-jiangsu.gov.cn/cgxx/ysgg/index_1.html',
        ]


    def parse(self, response):

        links = response.xpath('//div[@id="newsList"]//a')

        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response):

        time = response.css('.mid::text').extract_first()
        if time:
            time = time.split(':')[1].strip()
        if time == self.today:
            url = response.url
            title = response.css('.dtit h1::text').extract_first()
            content = py(py(response.text).find('.detail')[0]).html()
            content = ''.join(content).replace('\t','').replace('\n','').replace('\xa0','')
            if content:
                id = url.split('/')[-1].split('.')[0]

                yield{
                    'id': 'jiangsu_' + id,
                    'title': title.encode('utf-8').decode('unicode_escape'),
                    'content': content.encode('utf-8').decode('unicode_escape'),
                    'source_url': url,
                    'province': '江苏',
                }
    
