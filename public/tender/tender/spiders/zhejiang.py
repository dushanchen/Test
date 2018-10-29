# -*- coding: utf-8 -*-
import scrapy
import json

class ZhejiangSpider(scrapy.Spider):
    name = 'zhejiang'
    allowed_domains = ['zjzfcg.gov.cn']
    start_urls = ['http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?pageSize=100&pageNo=1&noticeType=0&url=http://notice.zcy.gov.cn/new/noticeSearch']

    # headers = {
    #     'Accept':'application/json, text/javascript, */*; q=0.01',
    #     'Accept-Encoding':'gzip, deflate',
    #     'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    #     'Connection':'keep-alive',
    #     'Host':'manager.zjzfcg.gov.cn',
    #     'Origin':'http://www.zjzfcg.gov.cn',
    #     'Referer':'http://www.zjzfcg.gov.cn/purchaseNotice/index.html',
    #     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    # }

    def parse(self, response):
         
        results = response.text
        results = json.loads(results)
        
        detail_url = 'http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?noticeId=%s&url=http://notice.zcy.gov.cn/new/noticeDetail'
        if 'articles' in results:
            for a in results['articles']:
                id = a['id']
                url = detail_url % id
                yield response.follow(url,callback=self.parse_detail)


    def parse_detail(self,response):
        result = json.loads(response.text)
        yield {
            'id':'zhejiang_' + result['id'],
            'title':result['noticeTitle'],
            'publish_time':result['noticePubDate'],
            'content':result['noticeContent'],
            'source_url':response.url,
            'province':'浙江'
        }

