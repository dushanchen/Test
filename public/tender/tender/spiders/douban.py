# -*- coding: utf-8 -*-
import scrapy

from pyquery import PyQuery as p

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        doc = response.text
        links = p(doc).find('.poster img')

        for link in links:
            yield{
                'url':p(link).attr('src'),
                'alt':p(link).attr('alt'),
            }
