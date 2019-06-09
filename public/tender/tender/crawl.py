        
import sys
import time
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.system('scrapy crawl beijing')
time.sleep(30)

os.system('scrapy crawl shanghai')
time.sleep(30)

os.system('scrapy crawl chongqing')
time.sleep(30)

os.system('scrapy crawl fujian')
time.sleep(30)

os.system('scrapy crawl guangdong')
time.sleep(30)

os.system('scrapy crawl hunan')
time.sleep(30)

os.system('scrapy crawl shandong')
time.sleep(30)

os.system('scrapy crawl sichuan')
time.sleep(30)

os.system('scrapy crawl zhejiang')
time.sleep(30)

os.system('scrapy crawl tianjing')
time.sleep(30)

os.system('scrapy crawl jiangsu')
time.sleep(30)