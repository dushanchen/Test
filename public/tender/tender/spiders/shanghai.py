# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from pyquery import PyQuery as p

import re
import requests
import datetime


class ShanghaiSpider(scrapy.Spider):
    name = 'shanghai'
    allowed_domains = ['www.zfcg.sh.gov.cn']
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }
    

    def start_requests(self):
        url = 'http://www.zfcg.sh.gov.cn/news.do'

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        params = {
            'bFlag': '00',
            'bulletininfotable_crd': '3',
            'bulletininfotable_efn': '',
            'bulletininfotable_p': '1',
            'bulletininfotable_pg': '1',
            'bulletininfotable_rd': '3',
            'bulletininfotable_s_beginday': '',
            'bulletininfotable_s_bulletintitle': '',
            'bulletininfotable_totalpages': '39',
            'bulletininfotable_totalrows': '383',
            'bulletininifotable_rd': '10',
            'ec_i': 'bulletininfotable',
            'findAjaxZoneAtClient': 'false',
            'flag': 'cggg',
            'method': 'purchasePracticeMore',
            'query_begindaybs': '',
            'query_begindayes': '',
            't_query_flag': '1',
            'treenum': '05'
        }
        
        types = [('05','cggg'),('14','dylygs'),('06','cjgg'),('05','qxgg'),('14','dylygs'),('06','cjgg')]
        # types = [('05','cggg')]

        requests = []
        for t in types:
            params['treenum'] = t[0]
            params['flag'] = t[1]

            req = scrapy.FormRequest(url,callback=self.parse_item,formdata=params,headers=self.headers)
            requests.append(req)
        return requests

    def parse_item(self, response):
        url_2 = 'http://www.zfcg.sh.gov.cn/emeb_bulletin.do?method=showbulletin&bulletin_id='
        result = response.text
        links = p(result).find('#bulletininfotable_table_body a')
        if len(links):
            for a in links:
                href = a.attrib['value']
                title = a.text
                # yield scrapy.Request(url_2+href,callback=self.parse_tender,headers=self.headers)

                resp = requests.get(url_2+href, headers=self.headers)
                content = resp.text
                if content:
                    c = p(resp.text).find('#templateContext')
                    e = p(resp.text).find('.newinfotr1')
                    drop = '<script(.*?)</script>|<textarea(.*?)>|</textarea>|<input(.*?)type="hidden"(.*?)>'

                    if c:
                        content = re.sub(drop,'',c.html())
                        
                    elif e:
                        content = '<table><tbody>'+''.join([_p(_).outerHtml() for _ in e])+'</tbody></table>'[:50]
                      
                    else:
                        content = ''
                    
                    yield{
                        'id':'shanghai_' + href,
                        'title':title,
                        'content':content,
                        'source_url':url_2+href,
                        'province':'上海',
                        'publish_time':datetime.date.today().strftime('%Y-%m-%d')
                    }

                # yield response.follow(url_2+href,callback=self.parse_tender,headers=self.headers)
        

    # def parse_tender(self,response):

    #     c = p(response.text).find('#templateContext')
    #     e = p(response.text).find('.newinfotr1')
    #     drop = '<script(.*?)</script>|<textarea(.*?)>|</textarea>|<input(.*?)type="hidden"(.*?)>'

    #     if c:
    #         content = re.sub(drop,'',c.html())
            
    #     elif e:
    #         content = '<table><tbody>'+''.join([_p(_).outerHtml() for _ in e])+'</tbody></table>'[:50]
          
    #     else:
    #         content = ''
        
    #     yield{
    #         'id':'shanghai_' + 
    #         'title':content,
    #         'content':content,
    #         'source_url':'',
    #         'area':'上海',
    #         'publish_time':datetime.date.today().strftime('%Y%m%d')
    #     }