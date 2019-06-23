# -*- coding: utf-8 -*-
import re
import scrapy

from pyquery import PyQuery as p

class AnhuiSpider(scrapy.Spider):
    name = 'anhui'
    allowed_domains = ['www.ahzfcg.gov.cn']
    start_urls = []

    def start_requests(self):
        url = 'http://www.ahzfcg.gov.cn/cmsNewsController/getCgggNewsList.do?pageNum=%s&numPerPage=20&channelCode=%s&bid_type=%s&type=&dist_code=340000'
        types = [('sjcg_gzgg', '110'), ('sjcg_zbgg','108'), ('sjcg_cggg','011'),('sjcg_cjgg', '112'),('sjcg_dyly','115'), ('sjcg_htgg','99'), ('sjcg_zzgg','113')]


        for i in types:
            for page in range(1,5):

            yield scrapy.Request(url%(1, i[0], i[1]), callback=self.parse)


    def parse(self, response):
        
        result = response.text
        doc = p(result)
        a = p(doc.find('.zc_contract_top')[1]).find('td a')

        for i in a:
            s = 'http://www.ahzfcg.gov.cn'+p(i).attr('href')
            yield scrapy.Request(s, callback=self.parse_)


    def parse_(self, response):

        url = response.url
        id = url.split('newsId=')
        if id and len(id) == 2:
            id = id[1]

            result = response.text
            doc = p(result)

            title = doc.find('.frameNews h1').html()
            publish_time = doc.find('.source span').html().replace('发布日期：', '').split(' ')[0]

            content = doc.find('.frameNews').html()

            yield {
                'id':'anhui_' + id,
                'title':title,
                'content':content,
                'souce_url':url,
                'province':'安徽',
                'publish_time':publish_time
            }


