import scrapy


class WosSpiderSpider(scrapy.Spider):
    name = 'wos_spider'
    allowed_domains = ['xxx']
    start_urls = ['http://xxx/']

    def parse(self, response):
        pass
