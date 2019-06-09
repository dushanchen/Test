# -*- coding': 'utf-8 -*-
import scrapy

import json
import requests
import datetime
from pyquery import PyQuery as p

class HunanSpider(scrapy.Spider):
    name = 'hunan'
    allowed_domains = ['www.ccgp-hunan.gov.cn']
    today = '2019-05-17'#datetime.date.today().strftime('%Y-%m-%d')


    headers = {
             
            'Host': 'www.ccgp-hunan.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.ccgp-hunan.gov.cn/page/notice/more.jsp?noticeTypeID=prcmNotices',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '117',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=S5bPl5hp2T-h8EgZUNCOlY3NWq3IiqNkNGjkuGnHAHQktvi_nJRa!-1587781876',
        }
    def start_requests(self):

        params = {
            'pType':'', 
            'prcmPrjName':'',   
            'prcmItemCode':'',      
            'prcmOrgName':'',       
            'startDate':self.today,  
            'endDate':self.today,
            'prcmPlanNo':'',    
            'pageSize':'100'
        }
        reqs = []

        for i in range(3):
            params['page'] = str(i+1)
            req = scrapy.FormRequest('http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
                callback=self.parse,formdata=params, headers=self.headers)
            reqs.append(req)
        return reqs

    def parse(self, response):
        
        url = 'http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId=%s&area_id='
        data = json.loads(response.text)
        rows = data['rows']
        for i in rows:
            id = i['NOTICE_ID']
            title = i['NOTICE_TITLE']

            resp = requests.get(url % (id))

            doc = p(resp.text)
            content = doc.find('table:eq(3)').html()

            yield{
                'id':'hunan_%s' % (id),
                'title':title,
                'content':content,
                'province':'湖南',
                'source_url': url % (id),
                'publish_time':self.today,
            }
        self.log(data)

