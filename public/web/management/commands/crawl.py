from django.core.management import BaseCommand
 
import time


class Command(BaseCommand):


    def handle(self, **option):

        from scrapy import cmdline
        cmdline.execute('cd /Users/dsc/Githome/Test/public/tender/spider'.split())
        cmdline.execute('scrapy crawl beijing'.split())
        time.sleep(3)
        cmdline.execute('scrapy crawl shanghai'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl chongqing'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl fujian'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl guangdong'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl hunan'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl shandong'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl sichuan'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl zhejiang'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl tianjing'.split())
        time.sleep(3)

        cmdline.execute('scrapy crawl jiangsu'.split())
        time.sleep(3)