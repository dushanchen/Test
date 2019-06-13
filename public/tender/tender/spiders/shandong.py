# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from pyquery import PyQuery as pq

import re
import requests

class ShandongSpider(scrapy.Spider):
    name = 'shandong'
    allowed_domains = ['www.ccgp-shandong.gov.cn']
    start_urls = ['http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp']


    def parse(self, response):
       
        doc = pq(response.text)

        links = doc.find('.BLink')
        reqs = []
        for i in links:
            link = pq(i).attr('href')
            code = re.findall(re.compile(r'[0-9]+'), link)
            if code:
                code = code[0]
                for j in range(2):
                    # a = requests.post('http://www.ccgp-shandong.gov.cn/sdgp2017/site/'+str(link),data={'curpage':j+1,'colcode':code})
                    # self.log(a.text)
                    req =  scrapy.FormRequest('http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp',
                        formdata={'curpage':str(j+1),'colcode':code},
                        callback=self.parse_item2
                    )
                    reqs.append(req)
        return reqs


    def parse_item2(self, response):

        links = response.css('.five')
        for link in links:
            yield response.follow(link, callback=self.parse_item3, meta={'title':link.css('::attr(title)').extract_first()})


    def parse_item3(self, response):

        id = re.search('id=(\d+)', response.url).group(1)
        self.log(response.meta)
        doc = pq(response.text)
        title = doc.find('div[align="center"]').html()
        content = doc.find('td[bgcolor="#FFFFFF"]:last').html()
        time = re.search('\d+年\d+月\d+日', doc.find('.Font9:last').html()).group(0)
        time = re.sub(r'年|月','-',time)
        time = re.sub(r'日','',time)


        yield{
            'id':'shandong_' + id,
            'title':response.meta['title'],
            'source_url':response.url,
            'content':content,
            'province':'山东',
            'publish_time':time,
        }


