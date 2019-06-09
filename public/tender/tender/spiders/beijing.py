# -*- coding: utf-8 -*-
import scrapy
import re
import datetime

class BeijingSpider(scrapy.Spider):
    name = 'beijing'
    allowed_domains = ['ccgp-beijing.gov.cn']
    start_urls = ['http://ccgp-beijing.gov.cn/xxgg/sjzfcggg/index.html',
                'http://ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_1.html',
                'http://ccgp-beijing.gov.cn/xxgg/sjzfcggg/index_2.html',
                'http://ccgp-beijing.gov.cn/xxgg/qjzfcggg/index.html',
                'http://ccgp-beijing.gov.cn/xxgg/qjzfcggg/index_1.html',
                'http://ccgp-beijing.gov.cn/xxgg/qjzfcggg/index_2.html',
    ]

    def parse(self, response):
        
        for a in response.css('.xinxi_ul a'):
            self.log(a.css('::attr(href)').extract_first())
            yield response.follow(a,self.parse_detail)

    def parse_detail(self,response):
        content = response.css('div[style*="padding-left:30px"]').extract_unquoted()
        publish_time = response.css('.datetime::text').extract_first()
        content = ''.join(content).replace('\t','').replace('\n','').replace('\xa0','')
        drop = '<a href=".(.*?)</a>'
        content = re.sub(drop,'',content)

        title = response.css('.div_hui + div span::text').extract_first()
        url = response.url
        p = re.compile('t\w*_\w*')
        id = p.findall(url)[0]
        yield {
            'title':title,
            'content':content,
            'province':'北京',
            'id':'beijing_' + id,
            'source_url':url,
            'publish_time':publish_time if publish_time else datetime.date.today().strftime('%Y-%m-%d')
        }
