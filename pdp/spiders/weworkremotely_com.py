from urllib.parse import urljoin

import scrapy
from scrapy import Request


class WeworkremotelyComSpider(scrapy.Spider):
    name = "weworkremotely_com"
    allowed_domains = ["weworkremotely.com"]
    start_urls = [
        "https://weworkremotely.com"
        "/remote-jobs/search?"
        "term=&button=&categories%5B%5D=2&categories%5B%5D=6"
        "&region%5B%5D=Anywhere+%28100%25+Remote%29+Only"
    ]

    def parse(self, response):
        for link in response.css("div#job_list li>a"):
            if link.attrib["href"][:4] in {"/rem", "/lis"}:
                url = urljoin(response.url, link.attrib["href"])
                yield Request(url=url, callback=self.parse_job)

    def parse_job(self, response):
        item = {}
        item["url"] = response.url
        item["time"] = response.css("time").attrib["datetime"]
        item["title"] = response.css("h1::text").get().strip()
        item["company"] = (
            response.css("h2#mobile-company>a::text").get().strip()
        )
        item["tags"] = response.css("a>span.listing-tag::text").getall()
        item["description"] = " ".join(
            response.css("div#job-listing-show-container ::text").getall()
        )
        yield item
