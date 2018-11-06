# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import requests

class TenderPipeline(object):

    def process_item(self, item, spider):
        headers = {'content-type': "application/json"}

        url = spider.settings['HTTP_CLIENT']
        requests.post(url,data=json.dumps(item),headers=headers)
        return item