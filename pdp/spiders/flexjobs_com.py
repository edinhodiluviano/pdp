import scrapy


class FlexjobsComSpider(scrapy.Spider):
    name = 'flexjobs.com'
    allowed_domains = ['flexjobs.com']
    start_urls = ['http://flexjobs.com/']

    def parse(self, response):
        pass
