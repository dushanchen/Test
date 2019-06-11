# -*- coding: utf-8 -*-
import scrapy
import re
from pyquery import PyQuery as pq


class HebeiSpider(scrapy.Spider):
    name = 'hebei'
    allowed_domains = ['www.ccgp-hebei.gov.cn']

    start_urls = [
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_zbfggg/',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_zbfggg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_zbfggg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_zbfggg/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/zhbfggg_fgw/',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/zhbfggg_fgw/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/zhbfggg_fgw/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/zhbfggg_fgw/index_3.html',

    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_gzfggg/',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_gzfggg/index_1.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_gzfggg/index_2.html',
    	'http://www.ccgp-hebei.gov.cn/province/fgw_annc/fgw_gzfggg/index_3.html',
    ]


    def parse(self, response):
        
        links = response.css('#moredingannctable .a3')

        for i in links:
        	yield response.follow(i, meta={'title':i.css('::text').extract_first()}, callback=self.parse_)

    
    def parse_(self, response):

    	content = pq(response.text).find('table[width="930"]').html()
    	title = response.meta['title']
    	source_url = response.url
    	id = re.findall(r't\d+_\d+', source_url)[0]
    	publish_time = pq(response.text).find('.txt7 span').html().strip()

    	yield{
            'id':id,
            'title':title,
            'source_url':source_url,
            'content':content,
            'province':'shandong',
            'publish_time':publish_time,
        }