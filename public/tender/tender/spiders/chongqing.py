import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from pyquery import PyQuery as py

class ChongqingSpider(CrawlSpider):
    name = 'chongqing'
    allowed_domains = ['cqgp.gov.cn']
    start_urls = ['https://www.cqgp.gov.cn/']

    rules = (
            Rule(LinkExtractor(allow=(''), restrict_css='.notice-list')),
            # Rule(LinkExtractor(allow=(''), restrict_css='.diqu')),
            Rule(LinkExtractor(allow=(r'.*/notices/.*')), callback='parse_item'),
        )

    def parse_item(self, response):
        self.log(response.text)
        url = response.url
        doc = response.text
        title = py(doc).find('.city-notice-block').html()
        # content = py(doc).find('.notice-con').html()
        # time = py(doc).find('.notice-list date').html().split('发布时间：')

        self.log(title)
        # self.log(content)
        # self.log(time)

        # if len(time) == 2:
        #     time = time[1][:10]
        # else:
        #     time = datetime.date.today().strftime('%Y%m%d')

        # if title and content:
        #     id = url.split('notice/')
        #     if len(id) == 2:
        #         id = id[1]
        #     yield {
        #         'id':'fujian_' + id,
        #         'title':title,
        #         'content':content,
        #         'url':response.url,
        #         'province':'chongqing',
        #         'publish_time':time
        #         }