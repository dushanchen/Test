# -*- coding: utf-8 -*-
import scrapy


class ZhejiangSpider(scrapy.Spider):
    name = 'zhejiang'
  #   allowed_domains = ['zjzfcg.gov.cn']
  #   start_urls = ['http://zjzfcg.gov.cn/']

  #   headers = {
  #     'Accept':'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate',
        # 'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        # 'Connection':'keep-alive',
        # 'Host':'manager.zjzfcg.gov.cn',
        # 'Origin':'http://www.zjzfcg.gov.cn',
        # 'Referer':'http://www.zjzfcg.gov.cn/purchaseNotice/index.html',
        # 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
  #   }

  #   def parse(self, response):
  #       yield {
  #         'content':response.content
  #       }
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
            'publish_time':datetime.datetime.now().strftime('%Y-%m-%s %H:%M:%S')
        }

    